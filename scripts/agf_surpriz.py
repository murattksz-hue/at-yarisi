"""AGF'ye göre sürpriz tanımı: kazananın AGF yüzdesi eşiğin altında mı / AGF sırasında ilk k içinde mi? (veri/at_gecmisi 2024+, kapanış AGF)
Kullanım: agf_surpriz.py   (yalnızca ekrana yazar). Yalnızca tüm atlarında AGF dolu, AGF toplamı ~%100 olan (altılıya giren) koşular.
Beklenen = AGF'den normalize olasılık; A/E = gerçek/beklenen; z = (G-B)/sqrt(sum b(1-b)). Getiri = eşik altındaki tüm atlara düz oyunun kesin ganyan getirisi."""
import os
K0=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import glob,gzip,csv,io,collections,math
import numpy as np
D=os.path.join(K0,'veri','at_gecmisi')
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
R=collections.defaultdict(list)
for fn in sorted(glob.glob(D+'/202[4-9]/*.csv.gz')):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
K=[]   # koşu kayıtları
for key in sorted(R):
    rs=R[key]; a=[f(r['agf']) for r in rs]
    if any(x is None for x in a) or len(rs)<5: continue
    win=[r['sonuc'].strip()=='1' for r in rs]
    if sum(win)!=1: continue
    a=np.array(a); s=a.sum()
    if not (94<=s<=106): continue
    g=[f(r['ganyan']) for r in rs]; gok=not any(v is None or v<=1 for v in g)
    p=a/s; o=np.argsort(-a,kind='stable'); rank=np.empty(len(a),int); rank[o]=np.arange(1,len(a)+1)
    w=win.index(True)
    K.append(dict(t=key[0],n=len(rs),a=a,p=p,rank=rank,w=w,wa=a[w],wr=rank[w],g=np.array(g,float) if gok else None,gok=gok))
print('koşu (AGF tam, tek kazananlı):',len(K))
nb=lambda n:'5-8' if n<=8 else '9-11' if n<=11 else '12-14' if n<=14 else '15+'
bins=['5-8','9-11','12-14','15+']
print('at sayısı dağılımı:',{b:sum(nb(k['n'])==b for k in K) for b in bins})

print('\n== 1) AGF SIRASINA GÖRE ORTALAMA % (koşudaki at sayısı grubuna göre)')
print('sıra:      '+'  '.join(f'{i:>5d}' for i in range(1,9))+'   ilk3   ilk4   ilk5')
for b in ['hepsi']+bins:
    x=[k for k in K if b=='hepsi' or nb(k['n'])==b]
    M=np.zeros(8); C=np.zeros(8)
    for k in x:
        s=np.sort(k['a'])[::-1]
        for i in range(min(8,len(s))): M[i]+=s[i]; C[i]+=1
    M=M/np.maximum(C,1)
    print(f'{b:10s}'+'  '.join(f'{m:5.1f}' for m in M)+f'  {M[:3].sum():5.1f}  {M[:4].sum():5.1f}  {M[:5].sum():5.1f}   (n={len(x)})')

print('\n== 2) KAZANAN AGF SIRASI: ilk k içinden çıkmayan = sürpriz (gerçek oran, AGF\'nin beklediği oran, A/E)')
print('grup   k    gerçek  beklenen  A/E     z')
for b in ['hepsi']+bins:
    x=[k for k in K if b=='hepsi' or nb(k['n'])==b]
    for kk in (3,4,5,6):
        O=sum(k['wr']>kk for k in x); E=sum(k['p'][k['rank']>kk].sum() for k in x); V=sum(q*(1-q) for q in [k['p'][k['rank']>kk].sum() for k in x])
        if E<5: continue
        print(f'{b:6s} >{kk}  {O/len(x):7.3f}  {E/len(x):7.3f}  {O/E:5.2f}  {(O-E)/math.sqrt(V):+5.1f}')

print('\n== 3) KAZANANIN AGF %\'SI: eşiğin ALTINDA = sürpriz (gerçek, beklenen, A/E, getiri = bu atlara düz oyunun ganyan getirisi)')
print('eşik   n_koşu   gerçek  beklenen  A/E     z    getiri(%)  | ilk yarı A/E  ikinci yarı A/E')
ts=sorted({k['t'] for k in K}); cut=ts[len(ts)//2]
def eşik(x,e):
    O=sum(k['wa']<e for k in x); Ex=[k['p'][k['a']<e].sum() for k in x]; E=sum(Ex); V=sum(q*(1-q) for q in Ex)
    return O,E,V
for e in (3,5,7.5,10,12.5,15,20):
    O,E,V=eşik(K,e)
    ret=[];
    for k in K:
        if not k['gok']: continue
        m=k['a']<e; ret.append(((k['g'][k['w']] if k['wa']<e else 0)-m.sum())/max(m.sum(),1)*m.sum()) # toplam geri dönüş-maliyet
    maliyet=sum((k['a']<e).sum() for k in K if k['gok']); geri=sum((k['g'][k['w']] if k['wa']<e else 0) for k in K if k['gok'])
    a1=eşik([k for k in K if k['t']<cut],e); a2=eşik([k for k in K if k['t']>=cut],e)
    print(f'<{e:<5}{len(K):7d}  {O/len(K):7.3f}  {E/len(K):7.3f}  {O/E:5.2f}  {(O-E)/math.sqrt(V):+5.1f}   {100*geri/maliyet:6.1f}    | {a1[0]/a1[1]:5.2f}          {a2[0]/a2[1]:5.2f}')

print('\n== 4) AYNI % EŞİĞİ at sayısına göre: kazananın AGF < eşik oranı (gerçek / beklenen)')
for e in (10,15):
    print(f' eşik <{e}%:')
    for b in bins:
        x=[k for k in K if nb(k['n'])==b]; O,E,V=eşik(x,e)
        print(f'   {b:6s} n={len(x):5d}  gerçek {O/len(x):.3f}  beklenen {E/len(x):.3f}  A/E {O/E:5.2f}  (bu eşiğin altındaki ort at sayısı {np.mean([(k["a"]<e).sum() for k in x]):.1f}/{np.mean([k["n"] for k in x]):.1f})')

print('\n== 5) ÖLÇÜTLER ARASI ÖRTÜŞME (kesin ganyan>=10 olan kazanan ile)')
G=[k for k in K if k['gok']]
gs=np.array([k['g'][k['w']]>=10 for k in G])
for ad,fn in (('AGF<10%',lambda k:k['wa']<10),('AGF<12.5%',lambda k:k['wa']<12.5),('AGF<15%',lambda k:k['wa']<15),('AGF sırası >4',lambda k:k['wr']>4),('AGF sırası >5',lambda k:k['wr']>5)):
    d=np.array([fn(k) for k in G])
    print(f'  {ad:14s} sürpriz {d.mean():.3f} | ganyan>=10 ile {gs.mean():.3f} | ikisi birden {np.mean(d&gs):.3f} | yalnız bu ölçüt {np.mean(d&~gs):.3f}')
