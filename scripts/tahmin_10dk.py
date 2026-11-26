"""Koşudan ~10 dk önce TAHMİN (tüm koşular için). Kullanım: tahmin_10dk.py <YYYY-AA-GG> <hipodrom> <koşu_no>   (agf_plan.py, −10 dk görüntüsünden sonra çağırır)
Kol: BİRLEŞİK_10 = −10 dk piyasa (AGF; yoksa ganyan^1,05) + b*baş-başa skoru (b=0,5), koşmaz atlar çıkarılır. Aynı kayıtta karşılaştırma kolları: piyasa_10 (yalnızca piyasa), v9 AGF'li, v9 AGF'siz (dondurulmuş sabah tahminleri).
Girdiler (yalnızca okur): son eBayi görüntüsü, veri/tahminler/<tarih>_<hip>[_agfsiz].json, veri/at_gecmisi (baş-başa, <tarih>'ten önce), veri/plan/<tarih>.json.
Çıktı: veri/tahminler_10dk/<tarih>.json içine bu koşu EKLENİR (bir koşu bir kez; üzerine yazılmaz) ve veri/tahminler_10dk/<tarih>.md. Puanlama: puan_10dk.py. Ağırlıklar ayarlanmadı (BİRLEŞİK testindeki gibi)."""
import os,sys,json,glob,gzip,csv,io,re,math,datetime,collections
import numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import kosu_tipi   # -I ile script dizini sys.path'te olmaz
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gun,hip,kno=sys.argv[1:4]; B_H2H=0.5; K_GANYAN=1.05
TR=datetime.timezone(datetime.timedelta(hours=3))
ak=lambda s:re.sub(r'\W','',str(s).upper())
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
def yukle(p):
    try: return json.load(open(p,encoding='utf-8'))
    except Exception: return None
od=os.path.join(K,'veri','tahminler_10dk'); os.makedirs(od,exist_ok=True); yol=os.path.join(od,f'{gun}.json')
D=yukle(yol) or {'tarih':gun,'surum':'tahmin_10dk_v1','ayarlar':{'b_h2h':B_H2H,'k_ganyan':K_GANYAN},'kosular':{}}
anah=f'{hip}|{kno}'
if anah in D['kosular']: sys.exit('bu koşu için tahmin zaten kayıtlı')
plan=yukle(os.path.join(K,'veri','plan',f'{gun}.json')) or {'kosular':{}}
saat=plan['kosular'].get(hip,{}).get(kno)
eb=sorted(glob.glob(os.path.join(K,'veri','agf_kayit',gun,f'{hip}_[0-9][0-9][0-9][0-9]UTC_ebayi.json')))
if not saat or not eb: sys.exit('koşu saati ya da eBayi görüntüsü yok')
E=yukle(eb[-1]).get(kno) or {}
if not E: sys.exit('bu koşu için eBayi verisi yok')
b=os.path.basename(eb[-1])[len(hip)+1:len(hip)+5]; gor=datetime.datetime.fromisoformat(gun).replace(hour=int(b[:2]),minute=int(b[2:]),tzinfo=datetime.timezone.utc)
kos=datetime.datetime.fromisoformat(gun).replace(hour=int(saat[:2]),minute=int(saat[3:]),tzinfo=TR); once=int((kos-gor).total_seconds()//60)
atlar=[a for a,v in E.items() if not v[3]]
if len(atlar)<2: sys.exit('at sayısı yetersiz')
agf=[];gan=[]
for a in atlar:
    v=E[a]; x=[y for y in (f(v[0]),f(v[1])) if y is not None and y>0]; agf.append(sum(x)/len(x) if x else 0.0); gan.append(f(v[2]))
def softmax(u):
    u=np.array(u,float); u=u-u.max(); e=np.exp(u); return e/e.sum()
if sum(agf)>0 and sum(1 for x in agf if x>0)>=0.7*len(agf): pm=softmax(np.log(np.maximum(agf,0.05))); kaynak='AGF'
else:
    g=[x if (x and 1<x<500) else 500.0 for x in gan]; pm=softmax(K_GANYAN*np.log(1/np.array(g))); kaynak='ganyan'
# baş-başa (gün'den önceki geçmiş)
H=collections.defaultdict(lambda:[0,0]); R=collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','202[4-9]','*.csv.gz'))):
    if os.path.basename(fn)[:10]>=gun: continue
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
for key in R:
    pos={ak(r['at']):int(r['sonuc']) for r in R[key] if r['sonuc'].strip().isdigit()}; ks=list(pos)
    for a in ks:
        for c in ks:
            if a!=c: H[(a,c)][1]+=1; H[(a,c)][0]+=pos[a]<pos[c]
# --- koşul tercihleri: atın kendisi ve babası (yavruları) hangi mesafe/pist/çeşitte iyi (kapanış ganyanına göre piyasa-düzeltmeli A/E)
def _band(m):
    try: m=int(m)
    except Exception: return '?'
    return '≤1200' if m<=1200 else '1300-1400' if m<=1400 else '1500-1700' if m<=1700 else '1800-2100' if m<=2100 else '2200+'
HS=collections.defaultdict(lambda:[0,0,0]); SS=collections.defaultdict(lambda:[0,0.0,0,0.0]); BABA={}
for key,rs0 in R.items():
    gg=[f(r['ganyan']) for r in rs0]; ok=len(rs0)>=5 and not any(x is None or x<=1 for x in gg) and sum(r['sonuc'].strip()=='1' for r in rs0)==1
    if ok: iv=[1/x for x in gg]; sv=sum(iv)
    for i,r in enumerate(rs0):
        hk=ak(r['at']); bb=(r['baba'] or '').upper().strip()
        if bb: BABA[hk]=bb
        if not r['sonuc'].strip().isdigit(): continue
        dims=(('mesafe',_band(r['mesafe'])),('pist',r['pist'] or '?'),('aile',kosu_tipi.aile(kosu_tipi.tur(r['tur'] or ''))),('hip',r['hip']))
        pos=int(r['sonuc'])
        for d in dims:
            h=HS[(hk,)+d]; h[0]+=1; h[1]+=pos==1; h[2]+=pos<=3
            if ok and bb:
                p=iv[i]/sv; t=SS[(bb,)+d]; t[0]+=1; t[1]+=p; t[2]+=pos==1; t[3]+=p*(1-p)
_bk=None
for _k in (yukle(os.path.join(K,'veri','tahminler',f'{gun}_{hip}.json')) or []):
    if str(_k['kosu'])==kno: _bk=_k.get('baslik','')
_ti=kosu_tipi.sinif(_bk) if _bk else {}
_dd=(('mesafe',_band(_ti.get('mesafe',''))),('pist',_ti.get('pist','?')),('aile',_ti.get('aile','?')),('hip',hip))
def tercih(ad):
    hk=ak(ad); bb=BABA.get(hk); o={'baba':bb}
    for d,v in _dd:
        h=HS.get((hk,d,v)); o['kendi_'+d]={'n':h[0],'birinci':h[1],'ilk3':h[2]} if h else {'n':0}
        t=SS.get((bb,d,v)) if bb else None
        if t and t[0]>=30: o['baba_'+d]={'n':t[0],'birinci':t[2],'ae':round(t[2]/max(t[1],1e-9),2),'z':round((t[2]-t[1])/max(t[3],1e-9)**0.5,1)}
    # tüm mesafe bantları: atın kendisi ve babası hangi mesafeyi seviyor
    B5=('≤1200','1300-1400','1500-1700','1800-2100','2200+'); kh={}; bh={}
    for b in B5:
        h=HS.get((hk,'mesafe',b)); kh[b]=[h[0],h[1],h[2]] if h else [0,0,0]
        t=SS.get((bb,'mesafe',b)) if bb else None
        if t and t[0]>=30: bh[b]=[t[0],t[2],round(t[2]/max(t[1],1e-9),2),round((t[2]-t[1])/max(t[3],1e-9)**0.5,1)]
    o['kendi_mesafe_hepsi']=kh; o['baba_mesafe_hepsi']=bh
    # 🎯 işareti (bilgi amaçlı; mesafe_profil_testi.py ile aynı tanım): atın bu bantta ≥4 koşusu, ilk-3 oranı ≥%50 ve genel orandan ≥15 puan iyi (uyumlu), babası bu bantta büzülmüş log(A/E) ≥ +0,05
    n_all=sum(v[0] for v in kh.values()); t_all=sum(v[2] for v in kh.values()); nb,wb,tb=kh.get(_dd[0][1],[0,0,0])
    uy=None
    if n_all>=4 and nb>=4:
        ra=t_all/n_all; uy='uyumlu' if (tb/nb>=0.5 and tb/nb-ra>=0.15) else ('uyumsuz' if tb==0 else None)
    tt=SS.get((bb,'mesafe',_dd[0][1])) if bb else None
    la=math.log((tt[2]+5)/(tt[1]+5)) if tt and tt[0]>=30 else None
    o['mesafe_uyum']=uy; o['baba_log_ae']=None if la is None else round(la,3); o['hedef']=bool(uy=='uyumlu' and la is not None and la>=0.05)
    o['baslik']=dict(_dd); return o
ks=[ak(a) for a in atlar]; sk=[]
for i,a in enumerate(ks):
    t=0.0
    for j,c in enumerate(ks):
        if i!=j:
            w,m=H[(a,c)]
            if m>0: t+=(2*w-m)/(m+1)
    sk.append(t/max(len(ks)-1,1))
sk=np.array(sk); pc=softmax(np.log(pm)+B_H2H*sk)
def kol(p):
    A=yukle(p)
    if not A: return None
    for k in A:
        if str(k['kosu'])==kno:
            d={ak(a['ad']):a['p'] for a in k['atlar']}; v=np.array([d.get(x,0.0) for x in ks],float); return v/v.sum() if v.sum()>0 else None
    return None
p9=kol(os.path.join(K,'veri','tahminler',f'{gun}_{hip}.json')); p9s=kol(os.path.join(K,'veri','tahminler',f'{gun}_{hip}_agfsiz.json'))
sira=np.argsort(-pc)
# sürpriz riski: piyasada %10 altı atların toplam payı. Terzil eşikleri 17.873 geçmiş koşudan (2024+, kapanış ganyanı): <=0,198 düşük, <=0,31 orta, üstü yüksek.
# Geçmişte kazananın ilk K piyasa atında olma oranı: düşük risk K3 %77, orta K4 %81, yüksek K5 %76 (K3 yalnızca %60) -> liste uzunluğu 3/4/5 (iki yarıda tutarlı: yüksek riskte K5 %76 / %76).
p_sur=float(pm[pm<0.10].sum()); risk='yüksek' if p_sur>0.31 else 'orta' if p_sur>0.198 else 'düşük'; KL={'düşük':3,'orta':4,'yüksek':5}[risk]; KL=min(KL,len(atlar))
_b=''
for _k in (yukle(os.path.join(K,'veri','tahminler',f'{gun}_{hip}.json')) or []):
    if str(_k['kosu'])==kno: _b=_k.get('baslik','')
D['kosular'][anah]={'tip':kosu_tipi.sinif(_b) if _b else None,'hip':hip,'kosu':int(kno),'saat':saat,'olusturma_tr':datetime.datetime.now(TR).isoformat(timespec='seconds'),'goruntu_utc':b,'goruntu_koşuya_dk':once,'piyasa_kaynak':kaynak,
  'secim_1':atlar[sira[0]],'secim_ilk3':[atlar[i] for i in sira[:3]],'surpriz_riski':risk,'surpriz_p':round(p_sur,3),'liste_uzunlugu':KL,'secim_liste':[atlar[i] for i in sira[:KL]],'guven':'net' if pc.max()>=0.40 else 'orta' if pc.max()>=0.28 else 'düşük',
  'atlar':[{'ad':atlar[i],'p_birlesik10':round(float(pc[i]),4),'p_piyasa10':round(float(pm[i]),4),'p_v9_agfli':None if p9 is None else round(float(p9[i]),4),'p_v9_agfsiz':None if p9s is None else round(float(p9s[i]),4),'h2h':round(float(sk[i]),3),'tercih':tercih(atlar[i])} for i in range(len(atlar))]}
json.dump(D,open(yol,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
L=[f'# −10 dk tahminleri — {gun}','','| Koşu | Saat | Liste (BİRLEŞİK_10; sürpriz riskine göre 3/4/5 at) | Risk | Güven | Piyasa favorisi | Görüntü (koşuya dk) |','|---|---|---|---|---|---|---|']
for k,v in sorted(D['kosular'].items(),key=lambda kv:(kv[1]['saat'],kv[1]['hip'])):
    pf=max(v['atlar'],key=lambda a:a['p_piyasa10'])['ad']
    L.append(f"| {v['hip']} {v['kosu']} | {v['saat']} | {' · '.join(x[:14] for x in v['secim_liste'])} | {v['surpriz_riski']} (%{100*v['surpriz_p']:.0f}) | {v['guven']} | {pf[:14]} | {v['goruntu_koşuya_dk']} |")
open(os.path.join(od,f'{gun}.md'),'w',encoding='utf-8').write('\n'.join(L)+'\n'); print(anah,'→',atlar[sira[0]],f'%{100*pc[sira[0]]:.0f}',kaynak,f'(görüntü koşuya {once} dk)')
