"""Her koşunun KAZANANINI her yönden kaydeder; sürpriz (kesin ganyan ≥10) olanları ayrıca işaretler. Sonra sürprizler favori kazananlarla kıyaslanır.
Kullanım: kazanan_profil.py YYYY-AA-GG Hipodrom KosuNo      → veri/kazanan_profil.csv'ye satır (tekrar yazmaz)
          kazanan_profil.py ozet                           → sürpriz vs diğer kazananlar karşılaştırması
Kaynaklar (hepsi gerçek): ebayi sonuç JSON (KGS, HP, start, jokey, son 6, ganyan), veri/para_takip.csv (AGF sabah/son, ganyan −60/−30/son, 💰/🤫),
veri/agf_kayit ILK ve görüntüler (AGF sırası), veri/tahminler (model sırası), veri/at_gecmisi (son koşusu: jokey/mesafe/pist/hipodrom değişimi, sırası)."""
import sys,os,glob,json,csv,gzip,io,re,urllib.request
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT=os.path.join(K,'veri','kazanan_profil.csv')
EBK={'Adana':'ADANA','İzmir':'IZMIR','İstanbul':'ISTANBUL','Bursa':'BURSA','Ankara':'ANKARA','Şanlıurfa':'SANLIURFA','Elazığ':'ELAZIG','Diyarbakır':'DIYARBAKIR','Kocaeli':'KOCAELI','Antalya':'ANTALYA'}
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
def sira(d,k):  # büyükten küçüğe sıra
    # eşitlikte sıra YOK: sonuç JSON'u bitiş sırasında olduğundan sıralı sort bağı kazananı öne alıyordu (26.11 düzeltme)
    return 1+sum(1 for x in d if (d[x] or 0)>(d.get(k) or 0)) if k in d else ''
def profil(T,H,NO):
    J=json.loads(urllib.request.urlopen(urllib.request.Request(f"https://ebayi.org/s/d/sonuclar/{T.replace('-','')}/full/{EBK[H]}.json",headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read())
    k=next((k for k in J.get('kosular',[]) if str(k.get('NO'))==NO),None)
    A=[a for a in (k or {}).get('atlar',[]) if not a.get('KOSMAZ') and str(a.get('SONUC') or '').isdigit()]
    if not A: return None
    w=next(a for a in A if a['SONUC']=='1'); G={a['NO']:f(a['GANYAN']) for a in A}; HP={a['NO']:f(a.get('HANDIKAP')) for a in A}
    r=dict(tarih=T,hip=H,kosu=NO,tur=k.get('CINSDETAY_TR'),mesafe=k.get('MESAFE'),pist=k.get('PISTADI_TR'),kosan=len(A),no=w['NO'],at=w['AD'],
           kesin=G[w['NO']],surpriz=int((G[w['NO']] or 0)>=10),ganyan_sira=sorted(G,key=lambda x:G[x] or 999).index(w['NO'])+1,
           hp=HP[w['NO']],hp_sira=sira(HP,w['NO']),kgs=w.get('KGS'),start=w.get('START'),jokey=w.get('JOKEYADI'),kilo=w.get('KILO'),son6=w.get('SON6'),yas=w.get('YAS'))
    # model sırası (sabah dondurulmuş)
    for m,suf in (('agfli',''),('agfsiz','_agfsiz')):
        tf=os.path.join(K,'veri','tahminler',f"{T}_{H}{suf}.json")
        if os.path.exists(tf):
            R=next((x for x in json.load(open(tf,encoding='utf-8')) if x['kosu']==NO),None)
            if R:
                P={x['no']:x['p'] for x in R['atlar']}; r[f'model_{m}_sira']=sira(P,w['NO']); r[f'model_{m}_p']=round(P.get(w['NO'],0),3)
                if m=='agfli': r['aday_sayisi']=R.get('oneri_at','')
    # AGF sırası: sabah ilk ve koşu öncesi son
    def agf(fn):
        D={};kk=None
        for l in open(fn,encoding='utf-8-sig').read().splitlines():
            c=l.split(';'); m=re.match(r'^(\d+)\. Kosu',c[0])
            if m: kk=m.group(1); continue
            if kk==NO and c[0].isdigit() and len(c)>10:
                a=re.match(r'%([\d.]+)',c[10]); D[c[0]]=float(a.group(1)) if a else None
        return D
    kd=os.path.join(K,'veri','agf_kayit',T); ilk=os.path.join(kd,f"TAM_{H}.csv")   # sabah AGF: TAM (dolu) görüntü; yoksa ILK (25.11.2026'dan beri; öncesi ILK)
    if not os.path.exists(ilk): ilk=os.path.join(kd,f"ILK_{H}.csv")
    if os.path.exists(ilk):
        I=agf(ilk)
        if any(I.values()): r['agf_sabah']=I.get(w['NO']); r['agf_sabah_sira']=sira(I,w['NO'])
    pf=os.path.join(K,'veri','plan',f'{T}.json')
    if os.path.exists(pf):
        s=json.load(open(pf,encoding='utf-8'))['kosular'][H][NO]; bas=int(s[:2])*60+int(s[3:]); C=[]
        for fn in glob.glob(os.path.join(kd,f"{H}_*UTC.csv")):
            hm=os.path.basename(fn)[len(H)+1:len(H)+5]; mm=((int(hm[:2])+3)%24)*60+int(hm[2:])
            if mm<bas: C.append((mm,fn))
        if C:
            L=agf(sorted(C)[-1][1])
            if any(L.values()):
                r['agf_son']=L.get(w['NO']); r['agf_son_sira']=sira(L,w['NO'])
                if r.get('agf_sabah') is not None and r['agf_son'] is not None:
                    ch={n:(L.get(n) or 0)-(I.get(n) or 0) for n in L}; r['agf_fark']=round(r['agf_son']-r['agf_sabah'],2); r['agf_artis_sira']=sira(ch,w['NO'])
    # para takibi satırı
    pt=os.path.join(K,'veri','para_takip.csv')
    if os.path.exists(pt):
        x=next((x for x in csv.DictReader(open(pt,encoding='utf-8')) if x['tarih']==T and x['hip']==H and x['kosu']==NO and x['at']==w['AD']),None)
        if x: r.update(g60=x['g60'],g30=x['g30'],g_son=x['g_son'],para=x['para'],sessiz=x.get('sessiz',''))
    # son koşusu (at geçmişi, bu günden önce)
    son=None
    for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','*','*.csv.gz')),reverse=True):
        if os.path.basename(fn)[:10]>=T: continue
        son=next((x for x in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')) if x['kod']==w['KOD']),None)
        if son: break
    if son:
        r.update(onceki_tarih=son['tarih'],onceki_sira=son['sonuc'],onceki_kosan=son['kosan'],onceki_ganyan=son['ganyan'],
                 jokey_degisti=int(son['jokey']!=w.get('JOKEYADI')),mesafe_fark=int(f(k.get('MESAFE')) or 0)-int(f(son['mesafe']) or 0),
                 pist_degisti=int(son['pist']!=k.get('PISTADI_TR')),hip_degisti=int(son['hip']!=H),tur_onceki=son['tur'])
    else: r['onceki_tarih']='ilk koşu/kayıt yok'
    try:
        sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import at_notlari as AN
        global _ATG
        if '_ATG' not in globals() or _ATG[0]!=T: _ATG=(T,)+AN.gecmis(T)
        hv=[x for x in HP.values() if x]; irk='Arap' if (k.get('GRUPKISA') or '').endswith('A') else 'İngiliz'
        v=AN.ek_vektor(_ATG[1].get(w['AD'].upper(),[]),_ATG[2],H,f(k.get('MESAFE')),sum(hv)/len(hv) if len(hv)>=4 else None,w.get('BABA'),irk)
        for a,x in zip(['sinif_fark','ilk_kez_hip','ilk_kez_mesafe','en_uzun','en_kisa','mesafe_degisim','soy_bant','iyi_yeni_mes'],v): r[a]='' if x is None else round(x,2)
        r['irk']=irk
    except Exception as e: print('ek alanlar hesaplanamadı:',e)
    if os.path.exists(pt):
        x=next((x for x in csv.DictReader(open(pt,encoding='utf-8')) if x['tarih']==T and x['hip']==H and x['kosu']==NO and x['at']==w['AD']),None)
        if x: r['sinyal']=x.get('sinyal','')
    return r
ALAN=['tarih','hip','kosu','tur','mesafe','pist','kosan','no','at','kesin','surpriz','ganyan_sira','model_agfli_sira','model_agfli_p','model_agfsiz_sira','model_agfsiz_p','aday_sayisi',
      'agf_sabah','agf_sabah_sira','agf_son','agf_son_sira','agf_fark','agf_artis_sira','g60','g30','g_son','para','sessiz','hp','hp_sira','kgs','start','jokey','kilo','yas','son6',
      'onceki_tarih','onceki_sira','onceki_kosan','onceki_ganyan','jokey_degisti','mesafe_fark','pist_degisti','hip_degisti','tur_onceki',
      'irk','sinif_fark','ilk_kez_hip','ilk_kez_mesafe','en_uzun','en_kisa','mesafe_degisim','soy_bant','iyi_yeni_mes','sinyal']
if sys.argv[1]=='ozet':
    R=list(csv.DictReader(open(OUT,encoding='utf-8')))
    def ort(L,a):
        v=[f(x[a]) for x in L if f(x.get(a)) is not None]; return f"{sum(v)/len(v):.2f} (n={len(v)})" if v else '-'
    def oran(L,a,kosul):
        v=[x for x in L if x.get(a) not in ('',None)]; return f"%{100*sum(kosul(x[a]) for x in v)/len(v):.0f} ({sum(kosul(x[a]) for x in v)}/{len(v)})" if v else '-'
    for ad,L in (('SÜRPRİZ (gny≥10)',[x for x in R if x['surpriz']=='1']),('diğer kazananlar',[x for x in R if x['surpriz']=='0'])):
        print(f"== {ad}: {len(L)} koşu")
        for a in ('kesin','model_agfli_sira','model_agfsiz_sira','agf_sabah_sira','agf_son_sira','agf_fark','agf_artis_sira','hp_sira','kgs','onceki_sira'): print(f"   ort {a:18} {ort(L,a)}")
        print(f"   💰 para girişi {oran(L,'para',lambda v:v=='1')} | 🤫 sessiz AGF {oran(L,'sessiz',lambda v:v=='1')} | AGF düştü {oran(L,'agf_fark',lambda v:f(v)<-1)} | AGF arttı {oran(L,'agf_fark',lambda v:f(v)>1)}")
        print(f"   jokey değişti {oran(L,'jokey_degisti',lambda v:v=='1')} | pist değişti {oran(L,'pist_degisti',lambda v:v=='1')} | hipodrom değişti {oran(L,'hip_degisti',lambda v:v=='1')} | mesafe değişti {oran(L,'mesafe_fark',lambda v:v!='0')}")
        print(f"   ganyan son 60 dk'da düştü (g60>kesin) {oran([x for x in L if f(x.get('g60'))],'g60',lambda v:True) and oran([x for x in L if f(x.get('g60'))],'kesin',lambda v:True) and ''}"+(f"{sum(f(x['g60'])>f(x['kesin']) for x in L if f(x.get('g60')))}/{sum(1 for x in L if f(x.get('g60')))}"))
    sys.exit()
if sys.argv[1]=='guncelle':
    R=list(csv.DictReader(open(OUT,encoding='utf-8'))) if os.path.exists(OUT) else []
    G=set(sys.argv[2:]); yeni=[]
    for x in R:
        if x['tarih'] in G:
            try:
                y=profil(x['tarih'],x['hip'],x['kosu']); yeni.append(y or x)
            except Exception as e: print('hata',x['tarih'],x['hip'],x['kosu'],e); yeni.append(x)
        else: yeni.append(x)
    w=csv.DictWriter(open(OUT,'w',encoding='utf-8',newline=''),fieldnames=ALAN,extrasaction='ignore'); w.writeheader(); w.writerows(yeni)
    print(len([x for x in R if x['tarih'] in G]),'satır güncellendi'); sys.exit()
if sys.argv[1]=='goster':   # dosyaya yazmadan
    r=profil(*sys.argv[2:5]); print(' | '.join(f"{a}={r.get(a,'')}" for a in ALAN[3:] if r and r.get(a) not in ('',None))); sys.exit()
T,H,NO=sys.argv[1:4]; r=profil(T,H,NO)
if not r: sys.exit('sonuç yok')
var=set()
if os.path.exists(OUT): var={(x['tarih'],x['hip'],x['kosu']) for x in csv.DictReader(open(OUT,encoding='utf-8'))}
if (T,H,NO) not in var:
    if os.path.exists(OUT):
        eski=list(csv.DictReader(open(OUT,encoding='utf-8')))
        if eski and list(eski[0])!=ALAN:
            w=csv.DictWriter(open(OUT,'w',encoding='utf-8',newline=''),fieldnames=ALAN,extrasaction='ignore'); w.writeheader(); w.writerows(eski)
    yeni=not os.path.exists(OUT); w=csv.DictWriter(open(OUT,'a',encoding='utf-8',newline=''),fieldnames=ALAN,extrasaction='ignore')
    if yeni: w.writeheader()
    w.writerow(r)
print(('⚡ SÜRPRİZ ' if r['surpriz'] else '')+' | '.join(f"{a}={r.get(a,'')}" for a in ALAN[3:] if r.get(a) not in ('',None)))
