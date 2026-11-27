"""Koşu riski modeli: koşunun kazananının gözden kaçan kazanan (ganyan >=10) olma olasılığı. Kullanım: kosu_riski_modeli.py [YYYY-AA-GG] -> veri/kosu_riski.md
Özellikler: piyasada p<%10 atların payı (ps), at sayısı, favori payı, hipodrom, çeşit ailesi, ırk, mesafe bandı, zemin. Eğitim: at_gecmisi 2022+ (kapanış ganyanı); canlı: son AGF görüntüsü (yaklaşık).
Irk: grup kodu 'A' ile bitiyorsa Arap, aksi halde İngiliz (27.11'de ilk sürümde tümü İngiliz sayılıp Arap koşuları bozulmuştu, düzeltildi). Test: 2025-07 sonrası ayrılmış küme AUC.
Yalnızca okur; yazar: veri/kosu_riski.md"""
import gzip,glob,csv,collections,re,sys,io,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));import kosu_tipi as K
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score,log_loss
import os
D=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
GUN=sys.argv[1] if len(sys.argv)>1 else __import__('datetime').date.today().isoformat()
def fl(x):
    try: return float(str(x).replace(',','.'))
    except: return None
def irk_of(grup,tur):
    g=(grup or '').strip()
    if g.endswith('A') or 'rap' in (g+(tur or '')): return 'Arap'
    return 'İng'
rows=[]
for p in sorted(glob.glob(D+'veri/at_gecmisi/202[2-6]/*.csv.gz')):
    R=collections.defaultdict(list)
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(p),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
    for k,rs in R.items():
        g=[fl(r['ganyan']) for r in rs]
        if len(rs)<5 or any(x is None or x<=1 for x in g) or sum(r['sonuc']=='1' for r in rs)!=1: continue
        s=sum(1/x for x in g);pp=[1/x/s for x in g];ps=sum(q for q in pp if q<.10)
        w=[x for r,x in zip(rs,g) if r['sonuc']=='1'][0]
        t=K.tur(rs[0]['tur'] or '')
        rows.append(dict(t=k[0],ps=ps,n=len(rs),fav=max(pp),hip=rs[0]['hip'],aile=K.aile(t),irk=irk_of(rs[0]['grup'],rs[0]['tur']),mb=K.mesafe_band(rs[0]['mesafe']),pist=(rs[0]['pist'] or '').strip(),y=int(w>=10)))
cnt=collections.Counter(r['irk'] for r in rows);print('irk',cnt)
cat=lambda key:sorted({r[key] for r in rows})
C={k:cat(k) for k in('hip','aile','irk','mb','pist')}
def X(d):
    v=[d['ps'],d['n'],d['fav']]
    for key in C: v+=[int(d[key]==c) for c in C[key]]
    return v
tr=[r for r in rows if r['t']<'2025-07-01'];te=[r for r in rows if r['t']>='2025-07-01']
m=LogisticRegression(C=1.0,max_iter=3000).fit(np.array([X(r) for r in tr]),[r['y'] for r in tr])
m0=LogisticRegression(max_iter=3000).fit(np.array([[r['ps'],r['n']] for r in tr]),[r['y'] for r in tr])
yt=[r['y'] for r in te]
print('test',len(te),'AUC tam',round(roc_auc_score(yt,m.predict_proba(np.array([X(r) for r in te]))[:,1]),3),'AUC ps+n',round(roc_auc_score(yt,m0.predict_proba(np.array([[r['ps'],r['n']] for r in te]))[:,1]),3))
for key in('irk',):
    for c in C[key]:
        sub=[r for r in rows if r[key]==c];print(c,len(sub),'%.1f%%'%(100*np.mean([r['y'] for r in sub])))
mf=LogisticRegression(C=1.0,max_iter=3000).fit(np.array([X(r) for r in rows]),[r['y'] for r in rows])
out=[]
for hip in('Bursa','İzmir'):
    f=sorted(glob.glob(D+'veri/agf_kayit/'+GUN+f'/{hip}_[0-9][0-9][0-9][0-9]UTC.csv'))[-1]
    t=open(f,encoding='utf-8-sig').read().splitlines();race=None;R={};H={}
    for l in t:
        mm=re.match(r'(\d+)\. Kosu\s*:\s*([\d.]+);(.*)',l)
        if mm: race=int(mm.group(1));R[race]=[];H[race]=(mm.group(2),mm.group(3));continue
        c=l.split(';')
        if race and c[0].isdigit() and len(c)>10:
            a=re.search(r'%?([\d.]+)\(',c[10]);R[race].append(float(a.group(1)) if a else 0)
    for r,v in R.items():
        s=sum(v)
        if s<=0: continue
        p=[x/s for x in v];ps=sum(q for q in p if q<.10)
        head=H[r][1];sn=K.sinif(head.replace(';',' '))
        d=dict(ps=ps,n=len(v),fav=max(p),hip=hip,aile=sn['aile'],irk=('Arap' if 'Arap' in head else 'İng'),mb=sn['mesafe_band'],pist=sn['pist'])
        out.append((mf.predict_proba([X(d)])[0][1],hip,r,H[r][0],len(v),round(ps,2),round(max(p),2),sn['aile'],d['irk'],sn['mesafe'],sn['pist']))
for o in sorted(out): print('%.0f%%'%(100*o[0]),*o[1:])

L=['# Koşu riski modeli — '+GUN,'',f'Test (2025-07 sonrası, n={len(te)}): AUC {roc_auc_score(yt,m.predict_proba(np.array([X(r) for r in te]))[:,1]):.3f}. Olasılık = kazananın ganyan>=10 olma ihtimali (taban oran %{100*np.mean([r["y"] for r in rows]):.1f}). Canlı girdi son AGF görüntüsü (yaklaşık).','','| Olasılık | Hip | Koşu | Saat | At | Risk (p<%10 payı) | Favori | Çeşit | Irk | Mesafe | Zemin |','|---|---|---|---|---|---|---|---|---|---|---|']
for o in sorted(out): L.append(f'| %{100*o[0]:.0f} | {o[1]} | {o[2]} | {o[3]} | {o[4]} | %{100*o[5]:.0f} | %{100*o[6]:.0f} | {o[7]} | {o[8]} | {o[9]} | {o[10]} |')
open(D+'veri/kosu_riski.md','w',encoding='utf-8').write('\n'.join(L)+'\n')
