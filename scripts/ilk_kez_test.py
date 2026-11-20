"""'İlk kez' etkileri: at bu hipodromda İLK KEZ mi koşuyor (başka yerde koşmuş)? İlk kez bu mesafede/daha uzunda mı? (veri/at_gecmisi 2024+, kronolojik)
Beklenen = piyasa (kesin ganyandan normalize). A/E, z, getiri; iki dönem. Çıktı: veri/ilk_kez_test.json"""
import os,glob,gzip,csv,io,collections,math,json
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
R=collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','*','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
GEC=collections.defaultdict(list); S=collections.defaultdict(lambda:[0.0,0.0,0,0.0,0.0,0.0,0.0,0.0])
for key in sorted(R,key=lambda k:(k[0],k[1],int(k[2] or 0))):
    A=R[key]; G=[f(a['ganyan']) for a in A]
    if key[0]>='2024' and all(g and g>1 for g in G) and sum(a['sonuc']=='1' for a in A)==1:
        q=[1/g for g in G]; s=sum(q); q=[x/s for x in q]
        for i,a in enumerate(A):
            P=GEC[a['kod']]
            if len(P)<2: continue   # en az 2 önceki koşu (ilk koşanlar ayrı konu)
            hipler={p['hip'] for p in P}; mes=[f(p['mesafe']) or 0 for p in P]; m=f(a['mesafe']) or 0
            iyi=sum(1 for p in P[-3:] if (f(p['sonuc']) or 99)<=3)>=2
            B=[('hipodrom: İLK KEZ burada' if a['hip'] not in hipler else 'hipodrom: daha önce koştu'),
               ('mesafe: en uzun (+100 üstü)' if m>max(mes)+100 else 'mesafe: daha önce koştu/kısa')]
            B+=[f"{b} | son3'te ≥2 ilk3" for b in B if iyi]
            B+=[f"{b} | gny≥10" for b in B[:2] if G[i]>=10]
            w=float(a['sonuc']=='1'); ilk=key[0]<'2025-07'
            for b in B:
                x=S[b]; x[0]+=w; x[1]+=q[i]; x[2]+=1; x[3]+=G[i]*w
                if ilk: x[4]+=w; x[5]+=q[i]
                else: x[6]+=w; x[7]+=q[i]
    for a in A: GEC[a['kod']].append(a)
out={}
print(f"{'grup':52} {'at':>7} {'kazandı':>7} {'A/E':>5} {'z':>5} {'getiri':>6} | ilk/son dönem")
for b in sorted(S):
    W,E,n,ret,W1,E1,W2,E2=S[b]; z=(W-E)/math.sqrt(E)
    out[b]=dict(at=n,kazandi=int(W),ae=round(W/E,2),z=round(z,1),getiri=round(100*ret/n),ae_ilk=round(W1/E1,2),ae_son=round(W2/E2,2))
    print(f"{b:52} {n:7} {int(W):7} {W/E:5.2f} {z:5.1f} {100*ret/n:5.0f}% | {W1/E1:.2f} / {W2/E2:.2f}")
json.dump(out,open(os.path.join(K,'veri','ilk_kez_test.json'),'w'),ensure_ascii=False,indent=1)
