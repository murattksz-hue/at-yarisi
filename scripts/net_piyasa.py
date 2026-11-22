"""Net piyasa testi: favori ile ikinci arasındaki kesin ganyan farkına (d) göre favorinin isabeti, piyasa beklentisi (A/E), ilk 3 ve düz oyun getirisi.
Kullanım: net_piyasa.py (yalnızca ekrana yazar; veri/at_gecmisi 2024+). Not: KESİN ganyan kullanır; koşudan önceki oranla tekrar edilmeli (YAPILACAK_TESTLER.md)."""
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
rows=[]
for key in sorted(R):
    rs=R[key]; g=[f(r['ganyan']) for r in rs]
    if any(v is None or v<=1 for v in g) or len(rs)<5: continue
    win=[r['sonuc'].strip()=='1' for r in rs]
    if sum(win)!=1: continue
    o=np.argsort(g); g1,g2=g[o[0]],g[o[1]]
    inv=np.array([1/v for v in g]); p1=(1/g1)/inv.sum()
    pos=[int(r['sonuc']) if r['sonuc'].strip().isdigit() else 99 for r in rs]
    rows.append(dict(t=key[0],n=len(rs),d=g2-g1,g1=g1,p1=p1,w=win[o[0]],top3=pos[o[0]]<=3,roi=(g1 if win[o[0]] else 0)-1))
print('koşu',len(rows),'| favori isabeti %.3f | ort piyasa p %.3f'%(np.mean([r['w'] for r in rows]),np.mean([r['p1'] for r in rows])))
def tablo(rs,baslik,keyf,edges):
    print('\n'+baslik); print('aralık        n   favori kazandı  piyasa p   A/E   ilk3   ROI(favoriye düz oyun)   %95 ROI aralığı')
    for a,b in zip(edges[:-1],edges[1:]):
        x=[r for r in rs if a<=keyf(r)<b]
        if len(x)<30: continue
        w=np.array([r['w'] for r in x],float); p=np.mean([r['p1'] for r in x]); roi=np.array([r['roi'] for r in x])
        se=math.sqrt(w.mean()*(1-w.mean())/len(x)); rr=random.Random(1)
        bs=sorted(np.mean([roi[rr.randrange(len(x))] for _ in range(len(x))]) for _ in range(400))
        print(f'{a:4.1f}-{b:<5.1f}{len(x):7d}  {w.mean():6.3f}±{1.96*se:.3f}   {p:7.3f}  {w.mean()/p:5.2f}  {np.mean([r["top3"] for r in x]):.3f}   {roi.mean():+.3f}                  [{bs[10]:+.3f}, {bs[389]:+.3f}]')
E=[0,0.5,1,2,3,5,10,1e9]
tablo(rows,'TÜM DÖNEM: favori–ikinci ganyan farkına göre (d)',lambda r:r['d'],E)
ts=sorted({r['t'] for r in rows}); cut=ts[len(ts)//2]
tablo([r for r in rows if r['t']<cut],'İLK YARI (%s öncesi)'%cut,lambda r:r['d'],E)
tablo([r for r in rows if r['t']>=cut],'İKİNCİ YARI (%s ve sonrası)'%cut,lambda r:r['d'],E)
# gerçekten ek bilgi var mı? aynı piyasa olasılığındaki favorileri farka göre ayır
print('\nAYNI piyasa p içinde: fark yüksek mi düşük mü? (ek bilgi testi, medyan farkın altı/üstü)')
for a,b in [(0.2,0.3),(0.3,0.4),(0.4,1.0)]:
    x=[r for r in rows if a<=r['p1']<b]; m=np.median([r['d'] for r in x])
    for ad,s in (('fark düşük',[r for r in x if r['d']<m]),('fark yüksek',[r for r in x if r['d']>=m])):
        w=np.mean([r['w'] for r in s]); p=np.mean([r['p1'] for r in s]); print(f'  p1 {a:.1f}-{b:.1f} {ad:12s} n={len(s):5d} kazandı {w:.3f} piyasa p {p:.3f}  A/E {w/p:.2f}')
