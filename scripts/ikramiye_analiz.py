"""Koşu ikramiyesi (1. ödülü) ile sonuç ilişkisi. Kullanım: ikramiye_analiz.py   (yalnızca ekrana yazar; veri/sonuc/2024+)
Kaynak: sonuç CSV başlığı '1.)490.000 TL;2.)...' satırı + at tablosundaki ganyan sütunu. Ölçütler: ganyan favorisi kazandı mı, kazanan ganyan >=10 (sürpriz), at sayısı.
Not: ikramiye koşu sınıfıyla (şartlı/handikap/grup) birlikte değişir; sınıf zaten piyasaya yansır, burada yalnızca betimleyici bakılır."""
import os,glob,re,math,collections,random
import numpy as np
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def num(s): return float(s.replace('.','').replace(',','.'))
rows=[]
for fn in sorted(glob.glob(os.path.join(K,'veri','sonuc','202[4-9]-*.csv'))):
    t=open(fn,encoding='utf-8-sig',errors='replace').read()
    for b in re.split(r'\n(?=\d+\. Kosu :)',t)[1:]:
        m=re.search(r'1\.\)([\d\.]+) TL',b)
        if not m: continue
        pr=num(m.group(1)); L=b.split('\n'); G=[];win=None
        for l in L:
            p=l.split(';')
            if len(p)>13 and p[0].strip().isdigit() and p[13].strip():
                try: g=num(p[13])
                except Exception: continue
                G.append(g)
                if win is None: win=g          # tablo bitiş sırasıyla: ilk satır kazanan
        if len(G)>=5 and win and win>1: rows.append((os.path.basename(fn)[:10],pr,len(G),win,win<=min(G)+1e-9,win>=10))
print('koşu',len(rows))
pr=np.array([r[1] for r in rows]); q=np.quantile(pr,[0,.25,.5,.75,1])
d=sorted({r[0] for r in rows}); h=d[len(d)//2]
def blok(sel,ad):
    n=len(sel); f=sum(r[4] for r in sel); s=sum(r[5] for r in sel); a=np.mean([r[2] for r in sel])
    pf=f/n; ps=s/n; return f'{ad:34s} n={n:5d} ort.at={a:4.1f} favori kazandı %{100*pf:4.1f} (±{196*math.sqrt(pf*(1-pf)/n):.1f}) | sürpriz(g>=10) %{100*ps:4.1f} (±{196*math.sqrt(ps*(1-ps)/n):.1f})'
for i in range(4):
    lo,hi=q[i],q[i+1]
    sel=[r for r in rows if lo<=r[1]<=hi if (r[1]<hi or i==3)]
    print(blok(sel,f'ikramiye {lo:,.0f}-{hi:,.0f} TL'))
print('\nİKİ YARI (en düşük %25 / en yüksek %25 ikramiye):')
for ad,yar in (('ilk yarı',lambda r:r[0]<h),('ikinci yarı',lambda r:r[0]>=h)):
    print(blok([r for r in rows if yar(r) and r[1]<=q[1]],ad+' düşük'),'\n'+blok([r for r in rows if yar(r) and r[1]>=q[3]],ad+' yüksek'))
print('\nAt sayısı kontrollü (9-11 at):')
for i in (0,3):
    sel=[r for r in rows if 9<=r[2]<=11 and ((r[1]<=q[1]) if i==0 else (r[1]>=q[3]))]; print(blok(sel,'düşük' if i==0 else 'yüksek'))
