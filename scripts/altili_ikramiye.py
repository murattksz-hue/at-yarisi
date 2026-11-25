"""Altılı ganyan ikramiyesi ve sürpriz sayısı (fizibilite testi). Kullanım: altili_ikramiye.py   (yalnızca ekrana yazar; veri/sonuc/*.csv, 2024+)
Sonuç dosyalarında altılının yalnızca ÖDEMESİ (1 TL'ye) var; havuz ve devir bilgisi YOK. Bu yüzden devir etkisi test edilemez; yalnızca ödeme ~ altı ayaktaki sürpriz sayısı (ganyan>=10) ilişkisine bakılır.
Altılı ayakları: ikramiyenin yazıldığı koşu ve ondan önceki 5 koşu (aynı dosya)."""
import os,glob,re,math,collections,random
import numpy as np
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def num(s): return float(s.replace('.','').replace(',','.'))
rows=[]
for fn in sorted(glob.glob(os.path.join(K,'veri','sonuc','202[4-9]-*.csv'))):
    t=open(fn,encoding='utf-8-sig',errors='replace').read()
    bl=re.split(r'\n(?=\d+\. Kosu :)',t)[1:]
    gan=[]
    for b in bl:
        m=re.search(r"(?<![\w'])GANYAN\(\d+\) :([\d\.,]+) TL",b); gan.append(num(m.group(1)) if m else None)
    for i,b in enumerate(bl):
        for m in re.finditer(r"\d\. 6'LI GANYAN\([^)]*\) :([\d\.,]+) TL",b):
            if i>=5 and all(g is not None for g in gan[i-5:i+1]):
                g=gan[i-5:i+1]; rows.append((os.path.basename(fn)[:10],num(m.group(1)),sum(x>=10 for x in g),float(np.prod(g))))
print('altılı sayısı',len(rows))
if rows:
    y=np.log([r[1] for r in rows]); lp=np.log([r[3] for r in rows]); s=np.array([r[2] for r in rows])
    print('log ödeme ~ log(ganyan çarpımı): r = %.3f'%np.corrcoef(y,lp)[0,1])
    for k in range(0,5):
        sel=[r[1] for r in rows if (r[2]==k if k<4 else r[2]>=4)]
        if sel: print(f"sürpriz ayak {k}{'+' if k==4 else ''}: {len(sel)} altılı, ortanca ödeme {np.median(sel):,.0f} TL")
    d=sorted({r[0] for r in rows}); h=d[len(d)//2]
    for ad,sel in (('ilk yarı',[r for r in rows if r[0]<h]),('ikinci yarı',[r for r in rows if r[0]>=h])):
        yy=np.log([r[1] for r in sel]); ll=np.log([r[3] for r in sel]); print(ad,len(sel),'r = %.3f'%np.corrcoef(yy,ll)[0,1])
