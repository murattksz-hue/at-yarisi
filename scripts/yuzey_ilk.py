"""Pist YÜZEYİ (Kum/Çim/Sentetik) etkileri: at bu yüzeyde İLK KEZ mi koşuyor? Önceki koşusuna göre yüzey değişti mi? (veri/at_gecmisi 2024+, kronolojik)
Kullanım: yuzey_ilk.py   (yalnızca ekrana yazar). Beklenen = piyasa (kesin ganyandan normalize); A/E, z, getiri.
Not: geçmiş yalnızca 2024'ten başlar; 2024-07-01 öncesi değerlendirmeye alınmaz ve en az 2 önceki koşusu olan atlar sayılır ("ilk kez" bazı atlarda yanlış olabilir)."""
import os
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import glob,gzip,csv,io,collections,math
import numpy as np
D=os.path.join(K,'veri','at_gecmisi')
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
R=collections.defaultdict(list)
for fn in sorted(glob.glob(D+'/202[4-9]/*.csv.gz')):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
H=collections.defaultdict(list)   # at kodu -> [(yüzey, hip)]
rows=[]
for key in sorted(R):
    rs=R[key]; g=[f(r['ganyan']) for r in rs]
    ok=not(any(v is None or v<=1 for v in g) or len(rs)<5)
    win=[r['sonuc'].strip()=='1' for r in rs]
    if ok and sum(win)==1 and key[0]>='2024-07-01':
        inv=np.array([1/v for v in g]); p=inv/inv.sum()
        for i,r in enumerate(rs):
            h=H[r['kod']]
            if len(h)<2: continue
            y=r['pist']; gecmis=[a for a,_ in h]; son=gecmis[-1]
            rows.append(dict(t=key[0],y=y,w=win[i],p=p[i],g=g[i],
                             ilk=(y not in gecmis),degisti=(y!=son),n_y=gecmis.count(y),n=len(gecmis),son=son))
    for r in rs: H[r['kod']].append((r['pist'],r['hip']))
print('at-koşu',len(rows))
def blok(x,ad):
    if len(x)<80: return
    O=sum(r['w'] for r in x); E=sum(r['p'] for r in x); V=sum(r['p']*(1-r['p']) for r in x)
    roi=np.mean([(r['g'] if r['w'] else 0)-1 for r in x])
    print(f'{ad:50s} n={len(x):6d}  kazandı {O/len(x):.4f} beklenen {E/len(x):.4f}  A/E {O/E:5.2f}  z {(O-E)/math.sqrt(V):+5.1f}  getiri {roi:+.2f}')
ts=sorted({r['t'] for r in rows}); cut=ts[len(ts)//2]
print('\n== BU YÜZEYDE İLK KEZ mi? (atın en az 2 önceki koşusu var)')
blok([r for r in rows if r['ilk']],'İLK KEZ bu yüzeyde (başka yüzeyde koşmuş)')
blok([r for r in rows if not r['ilk']],'bu yüzeyde daha önce koşmuş')
blok([r for r in rows if r['ilk'] and r['g']>=10],'  ilk kez | ganyan>=10')
blok([r for r in rows if not r['ilk'] and r['g']>=10],'  daha önce | ganyan>=10')
blok([r for r in rows if r['ilk'] and r['t']<cut],'  ilk kez | ilk yarı'); blok([r for r in rows if r['ilk'] and r['t']>=cut],'  ilk kez | ikinci yarı')
print('\n== YÜZEYE GÖRE İLK KEZ')
for y in ('Kum','Çim','Sentetik'):
    blok([r for r in rows if r['y']==y and r['ilk']],f'{y}: İLK KEZ'); blok([r for r in rows if r['y']==y and not r['ilk']],f'{y}: daha önce koşmuş')
print('\n== SON KOŞUYA GÖRE YÜZEY DEĞİŞTİ Mİ?')
blok([r for r in rows if r['degisti']],'önceki koşusundan FARKLI yüzey'); blok([r for r in rows if not r['degisti']],'önceki koşusuyla AYNI yüzey')
for a in ('Kum','Çim','Sentetik'):
    for b in ('Kum','Çim','Sentetik'):
        if a!=b: blok([r for r in rows if r['son']==a and r['y']==b],f'  {a} -> {b}')
print('\n== O YÜZEYDE KAÇ KOŞUSU VAR (deneyim)')
for ad,fn in (('0 (ilk kez)',lambda r:r['n_y']==0),('1-2',lambda r:1<=r['n_y']<=2),('3-9',lambda r:3<=r['n_y']<=9),('10+',lambda r:r['n_y']>=10)):
    blok([r for r in rows if fn(r)],f'o yüzeyde {ad} koşu')
