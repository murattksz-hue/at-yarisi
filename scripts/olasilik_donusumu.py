"""Ganyandan olasılık: basit normalizasyon mu, Shin mi, güç dönüşümü mü? (veri/at_gecmisi 2024+, kesin ganyan)
Kullanım: olasilik_donusumu.py   (yalnızca ekrana yazar). Kurulum: pip install shin numpy (yalnızca elle).
Sonuç (25.11.2026, 17.855 koşu): SHIN kötü (kazananın log-olasılığı −1,8122; normalizasyon −1,7993; en küçük olasılıklarda A/E 1,68, aşırı düzeltiyor:
Shin sabit oranlı bahis bürosu modelidir, ganyan toplu havuzdur). GÜÇ dönüşümü p ∝ (1/g)^k, k=1,05 (ilk %60'ta öğrenildi): son %40'ta koşu başına
log-olabilirlik kazancı +0,0016 (%95 [+0,0007, +0,0025]); %2-4 aralığında A/E 0,84→0,96; %2 altı hâlâ 0,75."""
import glob,gzip,csv,io,collections,math,random,os
import numpy as np
K0=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
R=collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(K0,'veri','at_gecmisi','202[4-9]','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
races=[]
for k in sorted(R):
    rs=R[k]; g=[f(r['ganyan']) for r in rs]
    if any(v is None or v<=1 for v in g) or len(rs)<5: continue
    w=[r['sonuc'].strip()=='1' for r in rs]
    if sum(w)!=1: continue
    races.append((k[0],np.array(g),w.index(True)))
print('koşu',len(races))
# 1) Shin
try:
    import shin
    d=[]
    for _,g,i in races:
        pn=(1/g)/(1/g).sum(); ps=np.array(shin.calculate_implied_probabilities(list(g))); d.append(math.log(ps[i])-math.log(pn[i]))
    d=np.array(d); print(f'Shin − normalizasyon: kazananın log-olasılığı farkı {d.mean():+.4f} (negatif = Shin daha kötü)')
except ImportError: print('shin kurulu değil (pip install shin), atlandı')
# 2) Güç dönüşümü
cut=sorted({r[0] for r in races})[int(len({r[0] for r in races})*0.6)]
tr=[r for r in races if r[0]<cut]; te=[r for r in races if r[0]>=cut]
def ll(rs,k):
    o=[]
    for _,g,i in rs:
        u=k*np.log(1/g); m=u.max(); o.append(u[i]-(m+math.log(np.exp(u-m).sum())))
    return np.array(o)
best=max(np.linspace(0.8,1.4,25),key=lambda k:ll(tr,k).sum())
d=ll(te,best)-ll(te,1.0); rr=random.Random(1); bs=sorted(np.mean([d[rr.randrange(len(d))] for _ in range(len(d))]) for _ in range(1000))
print(f'güç dönüşümü: eğitimde en iyi üs k={best:.3f}; test ({len(te)} koşu) kazanç {d.mean():+.5f} %95 [{bs[25]:+.5f}, {bs[974]:+.5f}]')
