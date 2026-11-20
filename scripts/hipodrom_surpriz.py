"""Hangi hipodromda koşular daha sürprizli bitiyor? (veri/at_gecmisi, 2024+ gerçek sonuçlar)
Favori = en düşük kesin ganyan. Beklenen = ganyandan (eküri dahil normalize) olasılık. Sürpriz = kazananın ganyanı ≥10.
Kalıcılık kontrolü: 2024-01..2025-06 ile 2025-07..sonrası ayrı ayrı. Çıktı: veri/hipodrom_surpriz.json"""
import os,glob,gzip,csv,io,json,collections,math
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
R=collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','202[4-9]','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
S={}
def ekle(d,h,A):
    G=[f(a['ganyan']) for a in A]
    if not all(g and g>1 for g in G) or sum(a['sonuc']=='1' for a in A)!=1: return
    q=[1/g for g in G]; t=sum(q); q=[x/t for x in q]; w=next(i for i,a in enumerate(A) if a['sonuc']=='1'); fi=min(range(len(G)),key=lambda i:G[i])
    s=S.setdefault((d,h),collections.Counter()); s['n']+=1; s['fav']+=w==fi; s['fav_bek']+=q[fi]
    s['s10']+=G[w]>=10; s['s10_bek']+=sum(q[i] for i in range(len(G)) if G[i]>=10); s['alan']+=len(A); s['ll']+=math.log(q[w])
for (t,h,k),A in R.items():
    d='1_ilk' if t<'2025-07' else '2_son'
    ekle(d,h,A); ekle('tum',h,A); ekle(d,'TÜMÜ',A); ekle('tum','TÜMÜ',A)
out={}
print(f"{'hipodrom':11} {'koşu':>5} {'alan':>5} {'fav%':>5} {'bek':>5} | {'gny10+%':>7} {'bek':>5} {'z':>5} | ilk dönem fark / son dönem fark")
for h in sorted({h for _,h in S},key=lambda h:-S[('tum',h)]['n']):
    s=S[('tum',h)]; n=s['n']; o={}
    for d in ('1_ilk','2_son'):
        x=S.get((d,h),collections.Counter()); o[d]=round(100*(x['s10']-x['s10_bek'])/max(1,x['n']),1)
    p=s['s10_bek']/n; z=(s['s10']-s['s10_bek'])/math.sqrt(n*p*(1-p))
    out[h]=dict(kosu=n,alan=round(s['alan']/n,1),fav=round(100*s['fav']/n,1),fav_bek=round(100*s['fav_bek']/n,1),s10=round(100*s['s10']/n,1),s10_bek=round(100*p,1),z=round(z,2),ilk_fark=o['1_ilk'],son_fark=o['2_son'])
    print(f"{h:11} {n:5} {out[h]['alan']:5} {out[h]['fav']:5} {out[h]['fav_bek']:5} | {out[h]['s10']:7} {out[h]['s10_bek']:5} {z:5.1f} | {o['1_ilk']:+5.1f} / {o['2_son']:+5.1f}")
json.dump(out,open(os.path.join(K,'veri','hipodrom_surpriz.json'),'w'),ensure_ascii=False,indent=1)
