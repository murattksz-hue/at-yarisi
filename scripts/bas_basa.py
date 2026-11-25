"""Baş-başa (head-to-head) testi: bugünkü atın, aynı koşudaki rakiplerini DAHA ÖNCE yenip yenmediği (veri/at_gecmisi 2024-07+, kronolojik, sızıntısız).
Kullanım: bas_basa.py   (yalnızca ekrana yazar). Skor = sum_j (galibiyet-yenilgi)/(karşılaşma+1) / (at sayısı-1), yalnızca daha önce karşılaşılan rakipler.
Piyasa = kesin ganyandan normalize olasılık. 1) piyasa+b*skor koşullu logit, b ilk %60'ta öğrenilir, son %40'ta log-olabilirlik kazancı + bootstrap %95.
2) Baş-başa lideri (>=2 karşılaşmalı rakibi olan en yüksek skorlu at): gerçek/beklenen (A/E), dönemlere göre, düz oyun getirisi.
Fikir kaynağı: yenibeygir.com /karsilastirma sayfasının konsepti (veri kullanılmadı; kendi geçmiş verimizden hesaplandı)."""
import os
K0=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import glob,gzip,csv,io,collections,math,random
import numpy as np
D=os.path.join(K0,'veri','at_gecmisi')
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
R=collections.defaultdict(list)
for fn in sorted(glob.glob(D+'/202[4-9]/*.csv.gz')):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
H=collections.defaultdict(lambda:[0,0])      # (a,b) -> [a'nın b'yi geçtiği, karşılaşma]
races=[]
for key in sorted(R):
    rs=R[key]
    pos={}
    for r in rs:
        s=r['sonuc'].strip()
        if s.isdigit(): pos[r['kod']]=int(s)
    g=[f(r['ganyan']) for r in rs]
    ok=not(any(v is None or v<=1 for v in g)) and len(rs)>=5 and sum(1 for r in rs if r['sonuc'].strip()=='1')==1
    if ok and key[0]>='2024-07-01':
        kods=[r['kod'] for r in rs]; n=len(kods)
        sc=np.zeros(n); cov=np.zeros(n)
        for i,a in enumerate(kods):
            tot=0.0;c=0
            for j,b in enumerate(kods):
                if i==j: continue
                w,m=H[(a,b)]
                if m>0: tot+=(2*w-m)/(m+1); c+=1       # (galibiyet-yenilgi)/(karşılaşma+1), küçük örnekte kendini sönümler
            sc[i]=tot/(n-1); cov[i]=c
        inv=np.array([1/v for v in g]); p=inv/inv.sum()
        win=[r['sonuc'].strip()=='1' for r in rs].index(True)
        races.append(dict(t=key[0],n=n,sc=sc,cov=cov,p=p,w=win,L=np.log(p),g=np.array(g,float)))
    # sonuçtan SONRA güncelle (sızıntı yok)
    ks=[k for k in pos]
    for a in ks:
        for b in ks:
            if a!=b:
                H[(a,b)][1]+=1
                if pos[a]<pos[b]: H[(a,b)][0]+=1
print('koşu',len(races),'| ort. karşılaşmalı rakip/at: %.2f'%np.mean([r['cov'].mean() for r in races]))
cut=sorted({r['t'] for r in races})[int(len({r['t'] for r in races})*0.6)]
tr=[r for r in races if r['t']<cut]; te=[r for r in races if r['t']>=cut]
def ll(rs,b):
    out=[]
    for r in rs:
        u=r['L']+b*r['sc']; m=u.max(); out.append(u[r['w']]-(m+math.log(np.exp(u-m).sum())))
    return np.array(out)
grid=np.linspace(-1,4,51); best=max(grid,key=lambda b:ll(tr,b).sum())
print('eğitim (ilk %%60, %d koşu): en iyi ağırlık b = %.2f'%(len(tr),best))
g=ll(te,best)-ll(te,0); rr=random.Random(1)
bs=sorted(np.mean([g[rr.randrange(len(g))] for _ in range(len(g))]) for _ in range(1000))
print('TEST (son %%40, %d koşu): koşu başına log-olabilirlik kazancı %+.5f  %%95 aralık [%+.5f, %+.5f]'%(len(te),g.mean(),bs[25],bs[974]))
# ayrı ayrı: karşılaşma yoğunluğuna göre

print('\n== Baş-başa lideri (>=2 karşılaşmalı rakibi olan, koşuda >=3 böyle at): dönemlere ve getiriye göre')
def lider(rs,ad):
    O=E=V=0;n=0;ret=0.0;fav=0
    for r in rs:
        if (r['cov']>=2).sum()<3: continue
        i=int(np.argmax(r['sc']))
        if r['cov'][i]<2: continue
        n+=1; O+=r['w']==i; E+=r['p'][i]; V+=r['p'][i]*(1-r['p'][i]); ret+=(r['g'][i] if r['w']==i else 0)-1
        fav+= int(np.argmax(r['p']))==i
    print(f'{ad:22s} koşu {n:5d} | kazandı {O/n:.3f} | beklenen {E/n:.3f} | A/E {O/E:.2f} z {(O-E)/math.sqrt(V):+.1f} | düz oyun getirisi {100*ret/n:+.1f}% | piyasa favorisi aynı atsa {100*fav/n:.0f}%')
ts=sorted({r['t'] for r in races}); a,b=ts[len(ts)//3],ts[2*len(ts)//3]
lider([r for r in races if r['t']<a],'1. üçte bir'); lider([r for r in races if a<=r['t']<b],'2. üçte bir'); lider([r for r in races if r['t']>=b],'3. üçte bir'); lider(races,'hepsi')
# favori olmayan baş-başa liderleri
def lider_fav_degil(rs):
    O=E=0;n=0;ret=0.0
    for r in rs:
        if (r['cov']>=2).sum()<3: continue
        i=int(np.argmax(r['sc']))
        if r['cov'][i]<2 or int(np.argmax(r['p']))==i: continue
        n+=1;O+=r['w']==i;E+=r['p'][i];ret+=(r['g'][i] if r['w']==i else 0)-1
    print(f'favori OLMAYAN lider      koşu {n:5d} | kazandı {O/n:.3f} | beklenen {E/n:.3f} | A/E {O/E:.2f} | getiri {100*ret/n:+.1f}%')
lider_fav_degil(races)
