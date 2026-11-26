"""Baba (yavruları) koşul tercih tablosu. Kullanım: soy_tercih.py   (gün sonu agf_plan.py çağırır; elle de çalışır)
Kaynak: veri/at_gecmisi (2020–2021 + 2024+), kapanış ganyanından normalize piyasa olasılığına göre A/E (>1: piyasadan iyi). Boyutlar: mesafe bandı, pist, koşu türü (aile), hipodrom.
Çıktı: veri/soy_tercih.csv (baba, boyut, değer, n, birinci, beklenen, A/E, z; n>=60) ve veri/soy_tercih.md (|z|>=2,5 ve n>=150 olanlar: baba × koşul). Çoklu karşılaştırma uyarısı: binlerce hücre bakıldığı için |z|>=2,5 olanların bir kısmı şans olabilir; ikinci yarıda tutarlılık sütunu eklendi."""
import os,sys,glob,gzip,csv,io,collections,math
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(K,'scripts')); import kosu_tipi
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
def band(m):
    try: m=int(m)
    except Exception: return '?'
    return '≤1200' if m<=1200 else '1300-1400' if m<=1400 else '1500-1700' if m<=1700 else '1800-2100' if m<=2100 else '2200+'
R=collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','*','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
tarihler=sorted({k[0] for k in R}); orta=tarihler[len(tarihler)//2]
S=collections.defaultdict(lambda:[0,0.0,0,0.0,0,0.0]); n_s=0
for k,rs in R.items():
    g=[f(r['ganyan']) for r in rs]
    if len(rs)<5 or any(x is None or x<=1 for x in g) or sum(r['sonuc'].strip()=='1' for r in rs)!=1: continue
    iv=[1/x for x in g]; sv=sum(iv)
    for i,r in enumerate(rs):
        bb=(r['baba'] or '').upper().strip()
        if not bb: continue
        p=iv[i]/sv; w=r['sonuc'].strip()=='1'; ikinci=k[0]>=orta
        for d,v in (('mesafe',band(r['mesafe'])),('pist',r['pist'] or '?'),('aile',kosu_tipi.aile(kosu_tipi.tur(r['tur'] or ''))),('hip',r['hip'])):
            t=S[(bb,d,v)]; t[0]+=1; t[1]+=p; t[2]+=w; t[3]+=p*(1-p)
            if ikinci: t[4]+=w; t[5]+=p
rows=[]
for (bb,d,v),t in S.items():
    if t[0]<60: continue
    z=(t[2]-t[1])/math.sqrt(t[3]) if t[3]>0 else 0; ae=t[2]/t[1] if t[1]>0 else 0
    ae2=t[4]/t[5] if t[5]>0 else None
    rows.append((bb,d,v,t[0],t[2],round(t[1],1),round(ae,2),round(z,1),None if ae2 is None else round(ae2,2)))
rows.sort(key=lambda r:(r[0],r[1],r[2]))
with open(os.path.join(K,'veri','soy_tercih.csv'),'w',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh); w.writerow(['baba','boyut','deger','n','birinci','beklenen','ae','z','ae_ikinci_yari']); w.writerows(rows)
sig=[r for r in rows if abs(r[7])>=2.5 and r[3]>=150]; sig.sort(key=lambda r:-abs(r[7]))
L=['# Baba × koşul tercihleri (piyasa-düzeltmeli)','',f'Kaynak: at_gecmisi ({tarihler[0]} – {tarihler[-1]}); n>=150 ve |z|>=2,5; {len(rows)} hücreden {len(sig)} tanesi. A/E>1: yavrular o koşulda piyasadan iyi. Son sütun: yalnızca ikinci yarıdaki A/E (kalıcılık). Çok hücre bakıldığı için bir kısmı şans olabilir.','',
   '| Baba | Boyut | Değer | n | Birinci | Beklenen | A/E | z | A/E (2. yarı) |','|---|---|---|---|---|---|---|---|---|']
for r in sig[:60]: L.append('| '+' | '.join('—' if x is None else str(x) for x in r)+' |')
open(os.path.join(K,'veri','soy_tercih.md'),'w',encoding='utf-8').write('\n'.join(L)+'\n'); print(len(rows),'hücre,',len(sig),'anlamlı (|z|>=2,5, n>=150)')
