"""Koşu türü seviyesi: her tür (CINSDETAY, ör. 'KV-7', 'Handikap 16', 'ŞARTLI 4') için koşuların ortalama HP'si (veri/at_gecmisi, HP>0 ≥4 at). Çıktı: veri/tur_seviye.json"""
import os,glob,gzip,csv,io,collections,json
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R=collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','*','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
T=collections.defaultdict(list)
for A in R.values():
    hv=[float(a['hp']) for a in A if a['hp'] and float(a['hp'])>0]
    if len(hv)>=4: T[A[0]['tur']].append(sum(hv)/len(hv))
out={t:dict(seviye=round(sum(v)/len(v),1),kosu=len(v)) for t,v in T.items() if len(v)>=5}
json.dump(out,open(os.path.join(K,'veri','tur_seviye.json'),'w'),ensure_ascii=False,indent=1)
for t,v in sorted(out.items(),key=lambda kv:-kv[1]['seviye'])[:12]: print(t,v)
print(len(out),'tür')
