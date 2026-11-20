"""Hangi soy (baba) hangi mesafede iyi? Irk x mesafe bandı (kısa ≤1400 / orta 1401-1900 / uzun ≥2000) x baba.
Veri: veri/at_gecmisi (tüm yıllar, gerçek sonuçlar). Kazanma %, ilk 3 %, beklenen (alan büyüklüğüne göre 1/n) ve piyasa A/E (ganyandan).
Çıktı: veri/soy_mesafe.json (en az 40 koşu)."""
import os,glob,gzip,csv,io,collections,json,math
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
def bant(m): return 'kısa' if m<=1400 else 'orta' if m<=1900 else 'uzun'
R=collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','*','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
S=collections.defaultdict(lambda:[0,0,0,0.0,0.0,0.0])   # koşu, birinci, ilk3, beklenen(1/n), piyasa beklenen, piyasa birinci
for k,A in R.items():
    n=len(A); G=[f(a['ganyan']) for a in A]; okp=all(g and g>1 for g in G)
    if okp: q=[1/g for g in G]; s=sum(q); q=[x/s for x in q]
    for i,a in enumerate(A):
        g=a['grup'] or ''; irk='Arap' if g.endswith('A') else 'İngiliz' if g.endswith('İ') else None
        if not irk or not a['baba']: continue
        x=S[(irk,bant(f(a['mesafe']) or 0),a['baba'])]; w=a['sonuc']=='1'
        x[0]+=1; x[1]+=w; x[2]+=a['sonuc'] in ('1','2','3'); x[3]+=1/n
        if okp: x[4]+=q[i]; x[5]+=w
out=collections.defaultdict(dict)
for (irk,b,baba),(n,w,i3,e,pe,pw) in S.items():
    if n<40: continue
    out[f"{irk}|{b}"][baba]=dict(kosu=n,birinci=w,kazanma=round(100*w/n,1),ilk3=round(100*i3/n,1),ae_alan=round(w/e,2),ae_piyasa=round(pw/pe,2) if pe else None)
json.dump(out,open(os.path.join(K,'veri','soy_mesafe.json'),'w'),ensure_ascii=False,indent=1)
for grp in sorted(out):
    L=sorted(out[grp].items(),key=lambda kv:-kv[1]['ae_alan'])
    print(f"== {grp}: {len(L)} baba (≥40 koşu)")
    for baba,v in L[:6]: print(f"   {baba[:26]:26} {v['kosu']:5} koşu  kazanma %{v['kazanma']:4}  ilk3 %{v['ilk3']:4}  A/E(alan) {v['ae_alan']}  A/E(piyasa) {v['ae_piyasa']}")
