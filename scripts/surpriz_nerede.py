"""Sürprizler (kazananın kesin ganyanı >=10) nerede çıkıyor, piyasanın beklediğinden fazla mı? (veri/at_gecmisi, 2024+)
Kullanım: surpriz_nerede.py   (yalnızca ekrana yazar)
Beklenen = piyasa (kesin ganyandan normalize olasılık) o koşuda ganyanı >=10 olan atlardan birinin kazanma olasılığı.
A/E = gerçek sürpriz / beklenen. z = (G-B)/sqrt(sum b(1-b)). |z|>=3 '*' (çok segment denendiği için sıkı eşik).
Segmentler: favori-ikinci fark, at sayısı, hipodrom, koşu türü, pist, mesafe, ay, at sayısı x fark, iki yarı (kararlılık)."""
import os
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import glob,gzip,csv,io,collections,math,re
import numpy as np
D=os.path.join(K,'veri','at_gecmisi')
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
R=collections.defaultdict(list)
for fn in sorted(glob.glob(D+'/202[4-9]/*.csv.gz')):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
rows=[]
for key in sorted(R):
    rs=R[key]; g=np.array([f(r['ganyan']) for r in rs],dtype=object)
    if any(v is None or v<=1 for v in g) or len(rs)<5: continue
    g=g.astype(float); win=[r['sonuc'].strip()=='1' for r in rs]
    if sum(win)!=1: continue
    inv=1/g; p=inv/inv.sum(); o=np.argsort(g)
    obs=float(g[win.index(True)]>=10); exp=float(p[g>=10].sum())
    r0=rs[0]; tur=re.match(r'\W*([A-Za-zÇĞİÖŞÜçğıöşü]+)',r0['tur']); tur=tur.group(1).upper() if tur else '?'
    m=f(r0['mesafe']) or 0
    rows.append(dict(t=key[0],hip=key[1],n=len(rs),d=g[o[1]]-g[o[0]],obs=obs,exp=exp,tur=tur,pist=r0['pist'],
                     mes='<1200' if m<1200 else '1200-1600' if m<1600 else '1600-2000' if m<2000 else '2000+',
                     ay=key[0][5:7]))
print('koşu',len(rows),'| gerçek sürpriz oranı %.3f | piyasanın beklediği %.3f | A/E %.2f'%(np.mean([r['obs'] for r in rows]),np.mean([r['exp'] for r in rows]),np.mean([r['obs'] for r in rows])/np.mean([r['exp'] for r in rows])))
def seg(rs,keyf,baslik,minn=150,hepsi=True):
    G=collections.defaultdict(list)
    for r in rs: G[keyf(r)].append(r)
    out=[]
    for k,x in G.items():
        if len(x)<minn: continue
        O=sum(r['obs'] for r in x); E=sum(r['exp'] for r in x); V=sum(r['exp']*(1-r['exp']) for r in x)
        out.append((k,len(x),O/len(x),E/len(x),O/E,(O-E)/math.sqrt(V)))
    print('\n'+baslik); print('segment                  n    gerçek  beklenen  A/E     z')
    for k,n,o,e,ae,z in sorted(out,key=lambda a:str(a[0]) if hepsi else -abs(a[5])):
        print(f'{str(k):20s}{n:7d}   {o:.3f}   {e:.3f}   {ae:5.2f}  {z:+5.1f}'+('  *' if abs(z)>=3 else ''))
db=lambda d:'<0.5' if d<0.5 else '0.5-1' if d<1 else '1-2' if d<2 else '2-4' if d<4 else '4+'
nb=lambda n:'5-8' if n<=8 else '9-11' if n<=11 else '12-14' if n<=14 else '15+'
seg(rows,lambda r:db(r['d']),'FAVORİ–İKİNCİ FARKI (d)')
seg(rows,lambda r:nb(r['n']),'AT SAYISI')
seg(rows,lambda r:r['hip'],'HİPODROM')
seg(rows,lambda r:r['tur'],'KOŞU TÜRÜ (ilk kelime)',minn=300)
seg(rows,lambda r:r['pist'],'PİST')
seg(rows,lambda r:r['mes'],'MESAFE')
seg(rows,lambda r:r['ay'],'AY',minn=300)
seg(rows,lambda r:(nb(r['n']),db(r['d'])),'AT SAYISI x FARK (yalnızca |z|>=3 göster)',minn=150,hepsi=False)
# kararlılık: yarılar
ts=sorted({r['t'] for r in rows}); cut=ts[len(ts)//2]
for ad,s in (('İLK YARI',[r for r in rows if r['t']<cut]),('İKİNCİ YARI',[r for r in rows if r['t']>=cut])):
    seg(s,lambda r:r['hip'],ad+' hipodrom',minn=300)
