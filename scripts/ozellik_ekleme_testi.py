"""Özellik ekleme testi (kosai makalesindeki fikirler, kendi verimizle SIFIRDAN): piyasaya (kesin ganyan, normalize) eklenince katkı.
Kullanım: ozellik_ekleme_testi.py   (yalnızca ekrana yazar; veri/at_gecmisi 2024-07+, kronolojik, sızıntısız)
Özellikler (koşu içinde ortalamaya göre merkezlenir): tabela (son 8 koşunun bitiş ortalaması, düşük iyi), aynı_jokey (önceki koşuyla aynı jokey),
kilo_fark (kilo - koşu ortalaması), orta_kilo (-|kilo - medyan|), uzmanlik (aynı hipodrom/mesafe bandı/tür geçmiş top-3 oranı >=%50 olanların sayısı, >=2 geçmiş koşu), bas_basa (h2h skoru).
Yöntem: koşullu logit u = log(p_piyasa) + b*özellik; b ilk %60'ta (zaman sırasıyla) öğrenilir, son %40'ta koşu başına log-olabilirlik kazancı + koşu-eşli bootstrap %95 aralık."""
import os,glob,gzip,csv,io,collections,math,random,re
import numpy as np
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
def band(m): return '<1200' if m<1200 else '1200-1600' if m<1600 else '1600-2000' if m<2000 else '2000+'
def tur(s):
    m=re.match(r'\W*([A-Za-zÇĞİÖŞÜçğıöşü]+)',s or ''); return m.group(1).upper() if m else '?'
R=collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','202[4-9]','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
HIST=collections.defaultdict(list)   # kod -> [(poz,jokey,hip,band,tur)]
H2=collections.defaultdict(lambda:[0,0])
races=[]
def z(x):
    x=np.array(x,float); s=x.std(); return (x-x.mean())/s if s>1e-9 else x*0
for key in sorted(R):
    rs=R[key]; g=[f(r['ganyan']) for r in rs]
    ok=not(any(v is None or v<=1 for v in g)) and len(rs)>=5 and sum(1 for r in rs if r['sonuc'].strip()=='1')==1
    if ok and key[0]>='2024-07-01':
        n=len(rs); inv=np.array([1/v for v in g]); p=inv/inv.sum(); w=[r['sonuc'].strip()=='1' for r in rs].index(True)
        mes=f(rs[0]['mesafe']) or 0; b0=band(mes); t0=tur(rs[0]['tur']); hip=key[1]
        tab=[];sj=[];up=[];kl=[f(r['kilo']) or 0 for r in rs]
        for r in rs:
            h=HIST[r['kod']]
            ps=[x[0] for x in h[-8:]]
            tab.append(-np.mean(ps) if len(ps)>=3 else np.nan)
            sj.append(1.0 if (h and h[-1][1]==r['jokey']) else 0.0)
            u=0
            for idx,val in ((2,hip),(3,b0),(4,t0)):
                s=[x for x in h if x[idx]==val]
                if len(s)>=2 and sum(1 for x in s if x[0]<=3)/len(s)>=0.5: u+=1
            up.append(float(u))
        tab=np.array(tab); tab=np.where(np.isnan(tab),np.nanmean(tab) if not np.all(np.isnan(tab)) else 0,tab)
        med=np.median(kl)
        kad=[r['at'] for r in rs]; kods=[r['kod'] for r in rs]
        bb=np.zeros(n)
        for i,a in enumerate(kods):
            t=0.0
            for j,b in enumerate(kods):
                if i!=j:
                    ww,m=H2[(a,b)]
                    if m>0: t+=(2*ww-m)/(m+1)
            bb[i]=t/max(n-1,1)
        races.append(dict(t=key[0],L=np.log(p),w=w,F={'tabela':z(tab),'aynı_jokey':z(sj),'kilo_fark':z(np.array(kl)-np.mean(kl)),'orta_kilo':z(-np.abs(np.array(kl)-med)),'uzmanlık':z(up),'baş_başa':z(bb)}))
    pos={}
    for r in rs:
        s=r['sonuc'].strip()
        if s.isdigit(): pos[r['kod']]=int(s)
    for r in rs:
        s=r['sonuc'].strip()
        if s.isdigit(): HIST[r['kod']].append((int(s),r['jokey'],key[1],band(f(rs[0]['mesafe']) or 0),tur(rs[0]['tur'])))
    ks=list(pos)
    for a in ks:
        for b in ks:
            if a!=b:
                H2[(a,b)][1]+=1
                if pos[a]<pos[b]: H2[(a,b)][0]+=1
print('koşu',len(races))
cut=sorted({r['t'] for r in races})[int(len({r['t'] for r in races})*0.6)]
tr=[r for r in races if r['t']<cut]; te=[r for r in races if r['t']>=cut]
def ll(rs,bs,names):
    out=[]
    for r in rs:
        u=r['L'].copy()
        for b,nm in zip(bs,names): u=u+b*r['F'][nm]
        m=u.max(); out.append(u[r['w']]-(m+math.log(np.exp(u-m).sum())))
    return np.array(out)
def fit(names):
    best=np.zeros(len(names))
    for _ in range(3):   # koordinat arama
        for i in range(len(names)):
            cand=np.linspace(-1,1.5,26); sc=[]
            for c in cand:
                b=best.copy(); b[i]=c; sc.append(ll(tr,b,names).sum())
            best[i]=cand[int(np.argmax(sc))]
    return best
rr=random.Random(1)
def rapor(ad,names):
    b=fit(names); g=ll(te,b,names)-ll(te,np.zeros(len(names)),names)
    bs=sorted(np.mean([g[rr.randrange(len(g))] for _ in range(len(g))]) for _ in range(600))
    isr='ANLAMLI +' if bs[15]>0 else ('ANLAMLI -' if bs[584]<0 else 'anlamsız')
    print(f'{ad:34s} b={np.round(b,2)}  kazanç/koşu {g.mean():+.5f}  %95 [{bs[15]:+.5f}, {bs[584]:+.5f}]  {isr}')
print('\nTEK TEK (piyasaya eklenince, son %40, '+str(len(te))+' koşu):')
for nm in ('tabela','aynı_jokey','kilo_fark','orta_kilo','uzmanlık','baş_başa'): rapor(nm,[nm])
print('\nBİRLİKTE:')
rapor('tabela+uzmanlık+aynı_jokey+orta_kilo',['tabela','uzmanlık','aynı_jokey','orta_kilo'])
rapor('hepsi (baş_başa dahil)',['tabela','aynı_jokey','kilo_fark','orta_kilo','uzmanlık','baş_başa'])
rapor('baş_başa + tabela',['baş_başa','tabela'])
