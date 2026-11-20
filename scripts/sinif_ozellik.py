"""Model özelliği: sınıf farkı = atın son 3 koşusundaki rakiplerin ortalama HP'si − bugünkü koşunun ortalama HP'si (veri/at_gecmisi, kronolojik).
Kullanım: sinif_ozellik.py cikti.json → {'YYYY-AA-GG_Hipodrom|koşuNo|AT ADI': sinif_fark}"""
import os,glob,gzip,csv,io,collections,json,sys
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
R=collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','*','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
GEC=collections.defaultdict(list); OUT={}
for key in sorted(R,key=lambda k:(k[0],k[1],int(k[2] or 0))):
    A=R[key]; hv=[f(a['hp']) for a in A if (f(a['hp']) or 0)>0]; kal=sum(hv)/len(hv) if len(hv)>=4 else None
    if kal:
        for a in A:
            P=[p for p in GEC[a['kod']][-3:] if p]
            if P: OUT[f"{key[0]}_{key[1]}|{key[2]}|{a['at']}"]=round(sum(P)/len(P)-kal,2)
    for a in A: GEC[a['kod']].append(kal)
json.dump(OUT,open(sys.argv[1],'w'),ensure_ascii=False); print(len(OUT),'kayıt')
