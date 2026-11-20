"""Sınıf düşüşü: atın önceki koşularındaki rakiplerin kalitesi (koşunun ortalama HP'si) bugünkü rakiplerden yüksekse, kötü dereceleri yanıltıcı olabilir.
Veri: veri/at_gecmisi 2024+ (gerçek). Koşu kalitesi = HP>0 atların ortalama HP'si (en az 4 at). Önceki = son 3 koşunun ortalaması (kronolojik, sızıntısız).
Beklenen = piyasa (kesin ganyandan normalize). Ölçü: A/E ve 1 TL ganyan getirisi. Gruplar: tüm atlar ve ganyanı ≥10 olanlar; kötü form (son 3 ort. sıra ≥6) ayrıca."""
import os,glob,gzip,csv,io,collections,math,json
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
R=collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','202[4-9]','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
GEC=collections.defaultdict(list); S=collections.defaultdict(lambda:[0.0,0.0,0,0.0,0.0,0.0,0.0,0.0])
for key in sorted(R,key=lambda k:(k[0],k[1],int(k[2] or 0))):
    A=R[key]; G=[f(a['ganyan']) for a in A]; HP=[f(a['hp']) or 0 for a in A]; hv=[h for h in HP if h>0]
    kal=sum(hv)/len(hv) if len(hv)>=4 else None
    if kal and all(g and g>1 for g in G) and sum(a['sonuc']=='1' for a in A)==1:
        q=[1/g for g in G]; s=sum(q); q=[x/s for x in q]
        for i,a in enumerate(A):
            P=[p for p in GEC[a['kod']][-3:] if p[0]]
            if not P: continue
            fark=sum(p[0] for p in P)/len(P)-kal; form=sum(p[1] for p in P)/len(P)
            b=('düşüş ≥10' if fark>=10 else 'düşüş 5-10' if fark>=5 else 'aynı ±5' if fark>-5 else 'yükseliş ≥5')
            w=float(a['sonuc']=='1'); ilk=key[0]<'2025-07'
            for grp in (f"tüm atlar | {b}",f"gny≥10 | {b}")+((f"gny≥10 + kötü form (son3 ort ≥6) | {b}",) if form>=6 else ()):
                if grp.startswith('gny') and G[i]<10: continue
                x=S[grp]; x[0]+=w; x[1]+=q[i]; x[2]+=1; x[3]+=G[i]*w
                if ilk: x[4]+=w; x[5]+=q[i]
                else: x[6]+=w; x[7]+=q[i]
    for i,a in enumerate(A): GEC[a['kod']].append((kal,f(a['sonuc']) or 99))
out={}
print(f"{'grup':52} {'at':>7} {'kazandı':>7} {'A/E':>5} {'z':>5} {'getiri':>6} | ilk/son dönem A/E")
for g in sorted(S):
    W,E,n,ret,W1,E1,W2,E2=S[g]
    if n<200: continue
    z=(W-E)/math.sqrt(E); out[g]=dict(at=n,kazandi=int(W),ae=round(W/E,2),z=round(z,1),getiri=round(100*ret/n),ae_ilk=round(W1/E1,2) if E1 else None,ae_son=round(W2/E2,2) if E2 else None)
    print(f"{g:52} {n:7} {int(W):7} {W/E:5.2f} {z:5.1f} {100*ret/n:5.0f}% | {W1/E1 if E1 else 0:.2f} / {W2/E2 if E2 else 0:.2f}")
json.dump(out,open(os.path.join(K,'veri','sinif_dusus.json'),'w'),ensure_ascii=False,indent=1)
