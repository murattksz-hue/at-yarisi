"""Kan analizi: baba, anne babası (kısrak babası) ve baba hattı (babanın babası) — ırk x mesafe bandı.
Veri: veri/at_gecmisi (tüm yıllar, gerçek sonuçlar). Babanın babası: at_gecmisi'nde babanın kendi koşu kaydı (BABA alanı) ya da veri/aygir_katalog_2026.json.
Ölçü: kazanma %, ilk 3 %, A/E (alan büyüklüğüne göre 1/n) ve piyasa A/E (ganyandan). En az 60 koşu. Çıktı: veri/kan_hatti.json"""
import os,glob,gzip,csv,io,collections,json
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
def bant(m): return 'kısa' if m<=1400 else 'orta' if m<=1900 else 'uzun'
def ad(s): return (s or '').upper().split(' (')[0].strip()
R=collections.defaultdict(list); BB={}
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','*','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')):
        R[(r['tarih'],r['hip'],r['kosu'])].append(r); BB.setdefault(ad(r['at']),ad(r['baba']))
kat=os.path.join(K,'veri','aygir_katalog_2026.json')
if os.path.exists(kat):
    for k,v in json.load(open(kat,encoding='utf-8')).items():
        if v.get('baba') and v['baba']!='None': BB.setdefault(ad(k),ad(v['baba']))
S={t:collections.defaultdict(lambda:[0,0,0,0.0,0.0,0]) for t in ('baba','annebaba','baba_hatti')}
for k,A in R.items():
    n=len(A); G=[f(a['ganyan']) for a in A]; okp=all(g and g>1 for g in G)
    if okp: q=[1/g for g in G]; s=sum(q); q=[x/s for x in q]
    for i,a in enumerate(A):
        g=a['grup'] or ''; irk='Arap' if g.endswith('A') else 'İngiliz' if g.endswith('İ') else None
        if not irk: continue
        b=bant(f(a['mesafe']) or 0); w=a['sonuc']=='1'
        for t,v in (('baba',ad(a['baba'])),('annebaba',ad(a['annebaba'])),('baba_hatti',BB.get(ad(a['baba'])))):
            if not v: continue
            x=S[t][(irk,b,v)]; x[0]+=1; x[1]+=w; x[2]+=a['sonuc'] in ('1','2','3'); x[3]+=1/n
            if okp: x[4]+=q[i]; x[5]+=w
out={}
for t,D in S.items():
    o=collections.defaultdict(dict)
    for (irk,b,v),(n,w,i3,e,pe,pw) in D.items():
        if n>=60: o[f"{irk}|{b}"][v]=dict(kosu=n,birinci=w,kazanma=round(100*w/n,1),ilk3=round(100*i3/n,1),ae_alan=round(w/e,2),ae_piyasa=round(pw/pe,2) if pe else None)
    out[t]=o
out['baba_babasi']={k:v for k,v in BB.items() if v}
json.dump(out,open(os.path.join(K,'veri','kan_hatti.json'),'w'),ensure_ascii=False,indent=1)
for t in ('baba_hatti','annebaba'):
    print(f"######## {t.upper()} (≥60 koşu; A/E alan, piyasa)")
    for grp in sorted(out[t]):
        L=sorted(out[t][grp].items(),key=lambda kv:-kv[1]['ae_alan'])
        print(f"== {grp} ({len(L)}): "+' | '.join(f"{v[:16]} {d['kosu']}k %{d['kazanma']} A/E {d['ae_alan']}/{d['ae_piyasa']}" for v,d in L[:5]))
