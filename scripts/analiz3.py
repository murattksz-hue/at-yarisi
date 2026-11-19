"""Günlük analiz (v5). Kullanım: analiz3.py program.html program.csv model.json profil.json hipodrom [idman.json] [kosu_jokey.json]
Olasılık = grup (ırk x zemin x mesafe) özel koşullu logit; galop küçük ek düzeltme (geri test edilmedi)."""
import sys,re,html,json,math,datetime
import numpy as np
ph,pc,mj,pj,HIP=sys.argv[1:6]; M=json.load(open(mj,encoding='utf-8'))
import os
MA=json.load(open(os.path.join(os.path.dirname(mj),'model_agfsiz.json'),encoding='utf-8')) if os.path.exists(os.path.join(os.path.dirname(mj),'model_agfsiz.json')) else None; PR=json.load(open(pj,encoding='utf-8'))
ID=json.load(open(sys.argv[6],encoding='utf-8')) if len(sys.argv)>6 else {}
_vd=os.path.dirname(os.path.abspath(mj))
HZ=json.load(open(os.path.join(_vd,'hiz_puani.json'),encoding='utf-8')) if os.path.exists(os.path.join(_vd,'hiz_puani.json')) else {}
_ot=json.load(open(os.path.join(_vd,'ozellik_test.json'),encoding='utf-8')) if os.path.exists(os.path.join(_vd,'ozellik_test.json')) else {}
_o2=json.load(open(os.path.join(_vd,'ozellik_test2.json'),encoding='utf-8')) if os.path.exists(os.path.join(_vd,'ozellik_test2.json')) else {}
GECMIS_W={k:v for k,v in zip(_o2.get('ozellikler',[]),_o2.get('agirlik',[])) if k!='son_fark_sn'}   # saniye farkı: birlikte ters işaret aldı, alınmadı
HZA=HZ.get('at',{}); HZS=HZ.get('sahip',{})
MD=json.load(open(os.path.join(_vd,'maiden_analiz.json'),encoding='utf-8')) if os.path.exists(os.path.join(_vd,'maiden_analiz.json')) else {}
KTA=json.load(open(os.path.join(_vd,'kosu_turu_analiz.json'),encoding='utf-8')) if os.path.exists(os.path.join(_vd,'kosu_turu_analiz.json')) else {}
def ince_tur(s):   # kosu_turu_analiz.py ile aynı sınıflama
    S=s.upper()
    for pat,f in [(r'\bG ?([123])\b',lambda m:'Grup '+m.group(1)),(r'KV-? ?(\d+)',lambda m:'KV-'+m.group(1)),(r'SATI',lambda m:'Satış'),
                  (r'MA[İI]DEN',lambda m:'Maiden'),(r'ŞARTLI ?-?(\d+)',lambda m:'Şartlı '+m.group(1)),(r'HAND[İI]KAP ?(\d+)',lambda m:'Handikap '+m.group(1)),(r'AÇIK|ACIK',lambda m:'Açık'),(r'\bLİSTE|LISTED',lambda m:'Listed')]:
        m=re.search(pat,S)
        if m: return f(m)
    return 'Diğer'
JT=json.load(open(os.path.join(_vd,'jokey_tablo.json'),encoding='utf-8'))['jokey'] if os.path.exists(os.path.join(_vd,'jokey_tablo.json')) else {}
def jmetin(j):
    d=JT.get(j)
    if not d: return f"{j[:12]} (veri az)"
    hp=d['hipodrom'].get(HIP,{'binis':0,'galibiyet':0})
    return (f"{j[:12]} %{d['yuzde']} ({d['binis']} biniş), 30g {d['son30_galibiyet']}/{d['son30_binis']}, {HIP} {hp['galibiyet']}/{hp['binis']}"
            +(f", favoride {d['favori_galibiyet']}/{d['favori_binis']}" if d['favori_binis'] else ''))
KJ=json.load(open(sys.argv[7],encoding='utf-8')) if len(sys.argv)>7 else {'kosu_turu':{},'jokey':{}}
HAVA=json.load(open(sys.argv[8],encoding='utf-8')) if len(sys.argv)>8 else {}
HE=json.load(open(os.path.join(os.path.dirname(mj),'hava_etkisi.json'),encoding='utf-8')) if os.path.exists(os.path.join(os.path.dirname(mj),'hava_etkisi.json')) else {}
def aile(h):
    s=h.upper()
    for pat,ad in [(r'G ?[123]\b','Grup'),(r'KV','KV'),(r'SATI','Satış'),(r'MAIDEN|MAİDEN|ŞARTLI ?-?19','Maiden'),(r'ŞARTLI','Şartlı'),(r'HANDİKAP|HANDIKAP','Handikap')]:
        if re.search(pat,s): return ad
    return 'Diğer'
def tip(h):
    s=h.upper()
    for pat,ad in [(r'G ?1\b','G1'),(r'G ?2\b','G2'),(r'G ?3\b','G3'),(r'KV-? ?(\d+)','KV'),(r'SATI','Satış'),(r'MAIDEN|MAİDEN','Maiden'),(r'ŞARTLI ?-?(\d+)','Şartlı'),(r'HANDİKAP ?(\d+)|HANDIKAP ?(\d+)','Handikap')]:
        m=re.search(pat,s)
        if m:
            n=next((g for g in m.groups() if g),'') if m.groups() else ''
            return ad+(' '+n if n and ad in('KV','Şartlı','Handikap') else '')
    return 'Diğer'
def bant(m): return 'kisa' if m<=1400 else ('orta' if m<=1900 else 'uzun')
def kova(s): return '1-3' if s<=3 else '4-6' if s<=6 else '7-9' if s<=9 else '10+'
def txt(x): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',x))).strip()
def ae(D,k,pr=4): s=D.get(k,[0,0.0]); return (s[0]+pr)/(s[1]+pr)
t=open(ph,encoding='utf-8').read(); ped={}; ad=None
_pd=re.findall(r'(Kum|Çim|Sentetik)\s*:\s*([A-Za-zÇĞİÖŞÜçğıöşü ]+?)\s*(?:<|Hava|\n)',re.sub(r'<[^>]+>','\n',t)[:200000])
PIST={k:v.strip() for k,v in _pd}
_hv=re.search(r'Hava\s*:\s*([^<\n]+)',re.sub(r'<[^>]+>','\n',t)); TJKHAVA=html.unescape(_hv.group(1).strip()) if _hv else None
ISLAK_KEL=('ağır','ıslak','yumuşak','sulu','çamur','islak','agir','yumusak')
def islak_mi(pist):
    d=PIST.get(pist,'').lower()
    if any(k in d for k in ISLAK_KEL): return True,f"TJK pist: {PIST.get(pist)}"
    i=HAVA.get('islaklik')
    if i is not None: return i>=5,f"tahmini ıslaklık {i} mm ({HAVA.get('kategori')})"
    return False,'hava bilgisi yok'
print(f"HAVA: TJK pist durumu {PIST or 'henüz yok'} | TJK hava: {TJKHAVA or 'henüz yok'} | tahmin: "+(f"yağış {HAVA.get('yagis')} mm, önceki gün {HAVA.get('onceki_gun')} mm, {HAVA.get('sicaklik')}°C, nem %{HAVA.get('nem')}, rüzgar {HAVA.get('ruzgar')} km/s ({HAVA.get('kaynak')})" if HAVA else 'yok'))
for k,v in re.findall(r'gunluk-GunlukYarisProgrami-(AtAdi|Baba)"[^>]*>(.*?)</td>',t,flags=re.S):
    if k=='AtAdi':
        m=re.search(r'>\s*([^<]+?)\s*<span',v) or re.search(r'>\s*([^<]+?)\s*</a>',v); ad=m.group(1).strip() if m else txt(v).split('(')[0].strip()
        b=re.search(r'koşuyu (\d+)\. olarak',v); ped[ad]={'bitis':int(b.group(1)) if b else None}
    elif ad:
        m=re.match(r'(.+?)\s+-\s+(.+?)\s+/\s+(.+)',txt(v))
        if m: ped[ad]['kb']=m.group(3)
EKURI=[[re.sub(r'\s+',' ',a).strip() for a in re.findall(r'\(\d+\)([^,\]]+)',html.unescape(re.sub(r'<[^>]+>','',m)))] for m in re.findall(r'<span class="tablo-ekuri">(.*?)</span>\s*<div class="bahisTipi',t,flags=re.S)]
SUR=json.load(open(os.path.join(os.path.dirname(os.path.abspath(mj)),'surpriz.json'),encoding='utf-8'))['gruplar'] if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(mj)),'surpriz.json')) else {}
GNY={}
for _a,_g in zip(re.findall(r'gunluk-GunlukYarisProgrami-AtAdi"[^>]*>(.*?)</td>',t,flags=re.S),re.findall(r'gunluk-GunlukYarisProgrami-Gny"[^>]*>(.*?)</td>',t,flags=re.S)):
    _m=re.search(r'>\s*([^<]+?)\s*<span',_a) or re.search(r'>\s*([^<]+?)\s*</a>',_a); _v=re.sub(r'<[^>]+>','',_g).strip().replace(',','.')
    try: GNY[_m.group(1).strip()]=float(_v)
    except Exception: pass
PC={'K':'Kum','Ç':'Çim','S':'Sentetik'}; races=[];cur=None;gun=None
for l in open(pc,encoding='utf-8-sig').read().splitlines():
    c=l.split(';')
    if gun is None:
        m0=re.search(r'(\d\d)/(\d\d)/(\d{4})',l); gun=datetime.date(int(m0.group(3)),int(m0.group(2)),int(m0.group(1))) if m0 else datetime.date.today()
    if re.match(r'^\d+\. Kosu',c[0]):
        m=re.search(r'(\d{3,4})m',l); pist=next((p for p in ('Kum','Çim','Sentetik') if p in l),'?')
        cur=dict(disi_kosu='Dişi' in c[1],aile=aile(c[1]),tip=tip(c[1]),bas=' '.join(x.strip() for x in c[:6] if x.strip()),irk='Arap' if 'Arap' in l else 'İngiliz',pist=pist,bant=bant(int(m.group(1))),m=int(m.group(1)),h=[]);races.append(cur);continue
    _m=re.search(r"(\d)'L[İIÜU] GANYAN Bu koşudan başlar",l)
    if cur and _m: cur.setdefault('coklu',[]).append(int(_m.group(1)))
    if cur and c[0].isdigit() and len(c)>14 and 'Koşmaz' not in c[1]:
        ag=re.match(r'%([\d.]+)',c[10]); y=re.match(r'(\d+)y',c[2]); kg=re.match(r'([\d,]+)',c[5]); st=re.match(r'(\d+)',c[9])
        isim=c[1]; a=next((k for k in sorted(ped,key=len,reverse=True) if isim.startswith(k)),isim)
        cur['h'].append(dict(no=c[0],ad=a,baba=c[3].strip(),hp=int(c[11]) if c[11].isdigit() else 0,son6=c[12],kgs=int(c[13]) if c[13].isdigit() else 0,
            s20=int(c[14]) if c[14].isdigit() else 0,agf=float(ag.group(1)) if ag else 0.5,yas=int(y.group(1)) if y else 4,kg=float(kg.group(1).replace(',','.')) if kg else 57,
            dis=(c[2].split() or ['?'])[-1] in ('d','k'),sah=c[7].strip(),ap=' AP' in c[6],st=int(st.group(1)) if st else 0,jok=c[6].replace(' AP','').strip(),kb=ped.get(a,{}).get('kb','?'),bitis=ped.get(a,{}).get('bitis')))
def galop(ad):
    d=ID.get(ad)
    if not d: return None,None,'idman yok',None,None
    try: fk=(gun-datetime.datetime.strptime(d['tarih'],'%d.%m.%Y').date()).days
    except: fk=99
    z={int(k):v for k,v in d['zaman'].items()}; t4=z.get(400) or (z[200]*2.05 if 200 in z else None)
    L=d.get('idmanlar')
    if L:   # pegadrom: geçmiş idmanlar
        tg=lambda i:(gun-datetime.datetime.strptime(i['tarih'],'%d.%m.%Y').date()).days
        d30=[i for i in L if 0<tg(i)<=30]; b4=[i['split'].get('400') for i in d30 if i['split'].get('400')]
        t4=min(b4) if b4 else t4; n30=len(d30); ef=d.get('efor') or '?'
        uyari=(' ↑çok idman' if n30>=3 else '')+(' ⚠zorlanarak' if ef=='Çalışarak' else '')
        metin=f"30g {n30} idman"+(f", en iyi 400m {t4:.1f}" if t4 else '')+f", son {fk}g {ef}{uyari}"
        return t4,fk,metin,n30,ef
    return t4,fk,f"{d['tur']} {d['pist']} {fk}g"+(f" 400m {t4:.1f}" if t4 else ''),None,None
not_=lambda x:'A' if x>=1.3 else 'B' if x>=1.05 else 'C' if x>=0.85 else 'D'
sk=[0,0,0]; JSONOUT=[]
for ri,r in enumerate(races):
    h=r['h']
    if len(h)<2: continue
    seg=f"{r['irk']}|{r['pist']}|{r['bant']}"; mseg=f"{r['irk']}|{r['aile']}" if M.get('segmod')=='tur' else seg
    qq=np.array([x['agf'] for x in h]); agf_gercek_yok=qq.std()<1e-6; agf_yok=agf_gercek_yok or os.environ.get('AGFSIZ_ZORLA')=='1'
    MM=MA if (agf_yok and MA) else M
    W=np.array(MM['grup'].get(mseg,MM['genel'])); wet,wnot=islak_mi(r['pist'])
    X=[]
    for x in h:
        fm=re.findall(r'([KÇS])(\d)',x['son6']); pts=[(10-int(q)) if q!='0' else 0 for _,q in fm]
        pp=[(10-int(q)) if q!='0' else 0 for y,q in fm if PC[y]==r['pist']]
        form=sum(pts)/len(pts) if pts else 3; pf=sum(pp)/len(pp) if pp else form*0.8
        x['bae']=ae(M['aygir'],f"{r['irk']}|{x['baba']}|{r['pist']}_{r['bant']}"); x['bg']=ae(M['aygir'],f"{r['irk']}|{x['baba']}|genel"); x['kbg']=ae(M['aygir'],f"{r['irk']}|{x['kb']}|genel")
        x['ku']=ae(M['kulvar'],f"{HIP}|{r['pist']}|{r['bant']}|{kova(x['st'])}",pr=10)
        x['jae']=ae(M.get('jokey',{}),f"{r['irk']}|{x['jok']}",pr=10)
        bw=math.log(ae(MM.get('aygir_islak',{}),f"{r['irk']}|{x['baba']}|ıslak",pr=3)/ae(MM.get('aygir_islak',{}),f"{r['irk']}|{x['baba']}|kuru",pr=3)) if wet else 0.0
        x['bw']=bw
        X.append([x['hp'],x['s20'],form,pf,math.log(x['bae']),math.log(x['ku']),math.log(max(x['agf'],0.3)),float(x['kgs']>60),float(x['ap']),x['yas'],x['kg']]+([math.log(x['jae'])] if len(W)>=12 else [])+([0,0,bw] if len(W)>=15 else []))
    X=np.array(X,float); sd=X.std(0); sd[sd==0]=1; Z=np.clip((X-X.mean(0))/sd,-2.5,2.5); Z[:,6]=X[:,6]-X[:,6].mean()
    if agf_yok: Z[:,6]=0
    if len(W)>=15:
        Z[:,12]=Z[:,0] if wet else 0; Z[:,13]=Z[:,6] if wet else 0; Z[:,14]=X[:,14]-X[:,14].mean()
    u=Z@W[:Z.shape[1]]
    g=[galop(x['ad']) for x in h]; t4=[a[0] for a in g if a[0]]; best=min(t4) if t4 else None
    GW=json.load(open(os.path.join(os.path.dirname(mj),'galop_agirlik.json')))['agirlik'] if os.path.exists(os.path.join(os.path.dirname(mj),'galop_agirlik.json')) else [1,0,0,0,0,0]
    v=np.array([a[0] if a[0] else np.nan for a in g]); vm=np.nanmean(v) if np.isfinite(v).any() else 0; vs=np.nanstd(v) if np.isfinite(v).sum()>1 else 1
    GF=np.array([[max(min(-(a[0]-vm)/(vs or 1),2.5),-2.5) if a[0] else 0.0, float(a[1] is None), float(a[1] is not None and a[1]<=7),
                  min(a[3] or 0,5)/5 if a[3] is not None else 0.0, float(a[4]=='Çalışarak')] for a in g])
    gk=GF@np.array(GW[1:6]); u=u+(gk-gk.mean())   # galop: 420 koşuda (30 gün) piyasaya katkısı doğrulandı
    # geçmiş performans (veri/ozellik_test2.json: 1.850 koşuda piyasaya katkısı doğrulandı)
    def zf(v):
        v=np.array(v,float); ok=np.isfinite(v); z=np.zeros(len(v))
        if ok.sum()>1 and v[ok].std()>0: z[ok]=np.clip((v[ok]-v[ok].mean())/v[ok].std(),-2.5,2.5)
        return z
    HH=[HZA.get(f"{r['irk']}|{x['ad']}",{}) for x in h]
    for x,H_ in zip(h,HH):
        sp=[y['puan'] for y in H_.get('son',[])]; x['hiz']=max(sp) if sp else np.nan; x['hiz_son']=sp[-1] if sp else np.nan
        G_=H_.get('galibiyetler',[]); x['pmg']=any(y['hipodrom']==HIP and y['pist']==r['pist'] and abs(y['mesafe']-r['m'])<=100 for y in G_); x['pg']=any(y['pist']==r['pist'] for y in G_)
        x['say']=H_.get('sayi',0); sh=HZS.get(x.get('sah',''),[0,0.0]); x['sah_ae']=(sh[0]+3)/(sh[1]+3)
    F={'hiz_en_iyi3':zf([x['hiz'] for x in h]),'hiz_son':zf([x['hiz_son'] for x in h]),'pist_mesafe_galibi':np.array([float(x['pmg']) for x in h]),
       'pist_galibi':np.array([float(x['pg']) for x in h]),'deneyim':zf([math.log(1+x['say']) for x in h]),'sahip':zf([math.log(x['sah_ae']) for x in h])}
    if len(W)>=21:   # v8: geçmiş etkenleri AGF ile birlikte eğitildi; ağırlıklar modelin kendisinden
        GW8=dict(zip(['hiz_en_iyi3','hiz_son','pist_mesafe_galibi','pist_galibi','deneyim','sahip'],W[15:21]))
        ek_u=sum(GW8[k]*v for k,v in F.items())
    else: ek_u=sum(GECMIS_W.get(k,0)*v for k,v in F.items())
    u=u+ek_u-ek_u.mean()
    if len(W)>=27:   # v9: karma koşuda dişi (halk sistematik fazla oynuyor; iki dönemde de piyasa A/E 0,78-0,84)
        dk=np.array([float(x.get('dis',False) and not r.get('disi_kosu',False)) for x in h]); u=u+W[26]*(dk-dk.mean())
    p=np.exp(u-u.max()); p/=p.sum(); q=np.array([x['agf'] for x in h]); q=q/q.sum()
    pro=PR['segment'].get(seg,{}); a_=pro.get('ae',{}); ic=a_.get('start 1-3',{}).get('piyasa_ae')
    print(f"\n=== {r['bas']}  [{seg}]"+("  (AGF henüz oluşmadı: AGF'siz model, değer işareti yok)" if agf_yok else ""))
    ek=EKURI[ri] if ri<len(EKURI) else []
    n_birim=len(h)-max(0,sum(1 for x in h if x['ad'] in ek)-1) if ek else len(h)
    alan='≤7' if n_birim<=7 else '8-10' if n_birim<=10 else '11-13' if n_birim<=13 else '14+'
    sa=SUR.get(f"alan (bahis birimi): {alan}",{}); st_=SUR.get(f"koşu türü: {r['irk']} {r['aile']}",{})
    print(f"    Sürpriz riski (geçmiş): {n_birim} bahis birimi → favori %{sa.get('favori','?')}, ganyan≥10 kazanan %{sa.get('surpriz','?')}; {r['irk']} {r['aile']}: favori %{st_.get('favori','?')}, sürpriz %{st_.get('surpriz','?')}")
    it=ince_tur(r['bas'].split(':',1)[-1]); kd=KTA.get(f"{r['irk']} {it}") or {}
    if kd.get('kosu',0)>=30:
        print(f"    KOŞU TÜRÜ {r['irk']} {it} ({kd['kosu']} geçmiş koşu, ort. {kd['alan']} birim): ganyan favorisi %{kd['favori']} kazandı (piyasa beklentisi %{kd['fav_bek']}), AGF favorisi %{kd['agf1']}, HP lideri %{kd['hp1']}; ilk 3 favoriden biri %{kd['fav_ilk3']}; ganyan≥10 kazanan %{kd['s10']} (piyasa beklentisi %{kd['s10_bek']}), medyan kazanan ganyanı {kd['medyan']}")
    elif kd: print(f"    KOŞU TÜRÜ {r['irk']} {it}: yalnızca {kd['kosu']} geçmiş koşu, istatistik güvenilmez")
    MAI=r['aile']=='Maiden'
    if MAI and MD:
        mk=MD['kosu'].get('Maiden+Ş19 hepsi',{}); kz=MD['kosu'].get('Kazanmış atların koşuları',{}); ik=MD['ae'].get('önceki koşu (veride): 0 = ilk koşu',{})
        print(f"    MAİDEN/ŞARTLI 19 (koşu kazanmamış atlar): alanlar kalabalık, ganyan≥20 kazanan %{mk.get('s20')} (kazanmış atların koşularında %{kz.get('s20')}) ama piyasanın beklediğinden FAZLA sürpriz yok; ilk kez koşanlar piyasa A/E {ik.get('ae')}")
    ekp=sum(p[i] for i,x in enumerate(h) if x['ad'] in ek)
    if ek: print(f"    EKÜRİ: {' + '.join(ek)} → biri kazanırsa ganyan kazanır; birlikte olasılık %{100*ekp:.1f} (adil oran {1/ekp if ekp else 0:.1f})")
    kt=KJ['kosu_turu'].get(f"{r['irk']}|{r['tip']}",{})
    print(f"    Zemin/mesafe profili: favori %{pro.get('favori_kazanma','?')} kazanıyor, ort. {pro.get('ort_alan','?')} at; iç kulvar (1-3) piyasaya göre {ic}")
    he=HE.get(f"{r['irk']}|{r['pist']}|{'ıslak' if wet else 'kuru'}",{})
    print(f"    Hava/pist: {'ISLAK' if wet else 'kuru'} ({wnot})"+(f"; bu koşullarda favori %{he.get('favori')}, HP lideri %{he.get('hp_lideri')} kazanıyor ({he.get('kosu')} koşu)" if he else ''))
    if kt: print(f"    Koşu türü ({r['tip']}): {kt['kosu']} koşu örneği, favori %{kt['favori']}, HP lideri %{kt['hp_lideri']}, tipik HP {kt['hp_p10']}-{kt['hp_p90']}")
    srt=np.argsort(-p)
    # güven düzeyi (v9 testi, 542 görülmemiş koşu; yalnızca AGF'li model için geçerli)
    pm=float(p[srt[0]])
    if not agf_yok:
        if pm>=0.60: print(f"    ★★★ ÇOK YÜKSEK GÜVEN (1. aday %{100*pm:.0f}): geçmişte bu düzeyde 1. aday %77 kazandı, ilk 2'de %89 (koşuların %6'sı)")
        elif pm>=0.50: print(f"    ★★ YÜKSEK GÜVEN (1. aday %{100*pm:.0f}): geçmişte bu düzeyde 1. aday %69 kazandı, ilk 2'de %83 (koşuların %13'ü)")
        elif pm>=0.45: print(f"    ★ GÜVEN (1. aday %{100*pm:.0f}): geçmişte bu düzeyde 1. aday %54 kazandı, ilk 2'de %72 (koşuların %20'si)")
        else: print(f"    Güven düşük (1. aday %{100*pm:.0f}): bu düzeyde 1. aday ~%25-45 kazanıyor; atlamayı düşün")
    KA=int(kd.get('oneri_at',5)) if kd.get('kosu',0)>=30 else 5; ik_=(kd.get('ilk_k') or {}).get(str(KA))
    print(f"    ► ÖNERİLEN ADAY SAYISI: {KA} at"+(f" (bu türde geçmişte kazanan, sıralamanın ilk {KA} atı içinden %{ik_} çıktı; ilk 3'ten %{kd['ilk_k']['3']})" if ik_ else '')+": "+', '.join(f"#{h[i]['no']} {h[i]['ad']}" for i in srt[:KA]))
    for i in srt[:max(5,KA)]:
        x=h[i]; deger=p[i]/q[i] if q[i] else 0; isaret=' ★DEĞER' if deger>=1.5 and p[i]>=0.05 and not agf_yok else ''
        bt=(f" → {x['bitis']}." if x['bitis'] else '')+(' [EKÜRİ]' if x['ad'] in ek else '')
        gy=GNY.get(x['ad']); pe=ekp if x['ad'] in ek else p[i]
        _U={('ek' if y['ad'] in ek else y['ad']):GNY[y['ad']] for y in h if GNY.get(y['ad'],0)>1}; _top=sum(1/v for v in _U.values()) if _U else 0
        gtxt=(f" | ganyan {gy:.2f}"+(' ★GANYAN' if 1.15<=_top<=1.6 and gy>=1.5/pe and pe>=0.05 else ('' if 1.15<=_top<=1.6 else ' (piyasa oturmamış)'))) if gy and gy>1 else ''
        print(f"  #{x['no']:>2} {x['ad'][:16]:16} olasılık %{100*p[i]:4.1f} (adil oran {1/p[i]:5.1f}, değer için ganyan ≥{1.5/p[i]:.1f}){'' if agf_yok else f' AGF %{100*q[i]:4.1f}'}{isaret}{gtxt} HP{x['hp']}{'' if not np.isfinite(x.get('hiz',np.nan)) else ' hız '+format(x['hiz'],'.0f')}{' ★pist-mesafe galibi' if x.get('pmg') else (' pist galibi' if x.get('pg') else '')} {x.get('say',0)} koşu{' (İLK KOŞU: maidende piyasa fazla oynuyor)' if MAI and not x.get('say',0) else ''} | baba {x['baba'][:13]} {not_(x['bg'])}/{x['bae']:.2f} KB {x['kb'][:11]} {not_(x['kbg'])} | {jmetin(x['jok'])} | st {x['st']} | {g[i][2]}{bt}")
    JSONOUT.append(dict(kosu=r['bas'].split(' Kosu')[0].strip().rstrip('.'), baslik=r['bas'], coklu_ganyan_baslar=r.get('coklu',[]), agf_yok=bool(agf_gercek_yok),oneri_at=KA,model='agfsiz' if agf_yok else 'agfli',
        atlar=[dict(no=x['no'],ad=x['ad'],p=round(float(p[i]),4),agf=round(float(q[i]),4),ekuri=x['ad'] in ek,ganyan=GNY.get(x['ad'])) for i,x in enumerate(h)]))
    kaz=[i for i,x in enumerate(h) if x['bitis']==1]
    if kaz: sk[2]+=1; sk[0]+=srt[0]==kaz[0]; sk[1]+=kaz[0] in srt[:3]
if os.environ.get('ANALIZ_JSON'): json.dump(JSONOUT,open(os.environ['ANALIZ_JSON'],'w'),ensure_ascii=False,indent=0)
if sk[2]: print(f"\nBugün biten koşular: {sk[2]} | 1. seçim kazandı {sk[0]} | kazanan ilk 3'te {sk[1]}")
