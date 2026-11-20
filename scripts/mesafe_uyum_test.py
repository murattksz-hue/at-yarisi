"""Atın mesafe uyumu: kısa (≤1400) / orta (1401-1900) / uzun (≥2000). Atın o banttaki geçmiş performansı (sıra yüzdeliği: 1=birinci, 0=sonuncu)
genel ortalamasından iyi mi kötü mü? En az 2 koşu bugünkü bantta + 2 koşu başka bantta. (veri/at_gecmisi 2024+, kronolojik; beklenen = piyasa)"""
import os,glob,gzip,csv,io,collections,math,json
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
def bant(m): return 'kısa' if m<=1400 else 'orta' if m<=1900 else 'uzun'
R=collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','*','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
GEC=collections.defaultdict(list); S=collections.defaultdict(lambda:[0.0,0.0,0,0.0,0.0,0.0,0.0,0.0])
for key in sorted(R,key=lambda k:(k[0],k[1],int(k[2] or 0))):
    A=R[key]; G=[f(a['ganyan']) for a in A]; n=len(A)
    if key[0]>='2024' and all(g and g>1 for g in G) and sum(a['sonuc']=='1' for a in A)==1:
        q=[1/g for g in G]; s=sum(q); q=[x/s for x in q]
        for i,a in enumerate(A):
            b=bant(f(a['mesafe']) or 0); P=GEC[a['kod']]; ib=[y for bb,y in P if bb==b]; db=[y for bb,y in P if bb!=b]
            if len(ib)<2 or len(db)<2: continue
            fark=sum(ib)/len(ib)-sum(db)/len(db)
            g=('bu mesafede belirgin İYİ (+0,15)' if fark>=0.15 else 'bu mesafede biraz iyi' if fark>=0.05 else 'bu mesafede belirgin KÖTÜ (−0,15)' if fark<=-0.15 else 'bu mesafede biraz kötü' if fark<=-0.05 else 'fark yok')
            w=float(a['sonuc']=='1'); ilk=key[0]<'2025-07'
            for grp in (g,f"{g} | gny≥10" if G[i]>=10 else None):
                if not grp: continue
                x=S[grp]; x[0]+=w; x[1]+=q[i]; x[2]+=1; x[3]+=G[i]*w
                if ilk: x[4]+=w; x[5]+=q[i]
                else: x[6]+=w; x[7]+=q[i]
    for a in A:
        so=f(a['sonuc'])
        if so and n>1: GEC[a['kod']].append((bant(f(a['mesafe']) or 0),1-(so-1)/(n-1)))
out={}
print(f"{'grup':45} {'at':>7} {'kazandı':>7} {'A/E':>5} {'z':>5} {'getiri':>6} | ilk/son dönem")
for g in sorted(S):
    W,E,n,ret,W1,E1,W2,E2=S[g]; z=(W-E)/math.sqrt(E)
    out[g]=dict(at=n,kazandi=int(W),ae=round(W/E,2),z=round(z,1),getiri=round(100*ret/n),ae_ilk=round(W1/E1,2),ae_son=round(W2/E2,2))
    print(f"{g:45} {n:7} {int(W):7} {W/E:5.2f} {z:5.1f} {100*ret/n:5.0f}% | {W1/E1:.2f} / {W2/E2:.2f}")
json.dump(out,open(os.path.join(K,'veri','mesafe_uyum_test.json'),'w'),ensure_ascii=False,indent=1)
