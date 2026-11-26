"""SHAP ile sürprizler: piyasasız (ganyan/AGF kullanmayan) gradient boosting modeli + sürpriz kazananlar (ganyan>=10) için özellik katkıları.
Kullanım: shap_surpriz.py   (yalnızca ekrana yazar; veri/at_gecmisi 2024-07+). Kurulum (yalnızca elle): pip install scikit-learn shap lightgbm
DÜZELTME (25.11): yaş sütunu = '<yaş>y <RENK> <CİNSİYET>': 2. harf renk (d doru, a alazan, k kır, ...), 3. harf cinsiyet (e genç erkek, a aygır, d genç dişi, k kısrak, g iğdiş;
yaşla doğrulandı: e/d %100 2-3 yaş, a/k %100 4+). İlk taslakta 2. harf yanlışlıkla 'cinsiyet' alınmıştı (renk = ırk vekili) ve SHAP'ı yanıltmıştı.
Kategorikler sıralı tam sayı kodlanır (hash değil; sklearn'ün categorical_features seçeneği SHAP toplamsallık kontrolünü bozduğu için kullanılmadı). Yöntem: ilk %60 zaman sırasıyla eğitim, son %40 test; test log-olabilirlik karşılaştırması (piyasa, model), kazananın model sırası."""
import os,glob,gzip,csv,io,re,math,collections,random,warnings
import numpy as np
warnings.filterwarnings('ignore')
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
R=collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','202[4-9]','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
CAT=collections.defaultdict(dict)
def kod(alan,deger):
    d=CAT[alan]
    if deger not in d and len(d)<250: d[deger]=len(d)
    return d.get(deger,0)
CINS={'e':0,'a':1,'d':2,'k':3,'g':4}
JW=collections.defaultdict(lambda:[0,0]); AW=collections.defaultdict(lambda:[0,0]); H2=collections.defaultdict(lambda:[0,0])
X=[];meta=[]
NAMES=['hp','hp_fark','hp_sira','start','yas','cinsiyet','renk','irk','kilo','kilo_fark','mesafe','kosan','jokey_oran','jokey_n','antrenor_oran','antrenor_n','pist','tur','hipodrom','bas_basa']
CATIDX=[NAMES.index(x) for x in ('cinsiyet','renk','irk','pist','tur','hipodrom')]
for key in sorted(R):
    rs=R[key]; g=[f(r['ganyan']) for r in rs]
    ok=not(any(v is None or v<=1 for v in g)) and len(rs)>=5 and sum(1 for r in rs if r['sonuc'].strip()=='1')==1
    pos={r['kod']:int(r['sonuc']) for r in rs if r['sonuc'].strip().isdigit()}
    if ok and key[0]>='2024-07-01':
        n=len(rs); hp=[f(r['hp']) or 0 for r in rs]; kl=[f(r['kilo']) or 0 for r in rs]; hm=np.mean(hp); km=np.mean(kl)
        hr=(lambda h:1+(h[None,:]>h[:,None]).sum(1))(np.array(hp,float)); inv=np.array([1/v for v in g]); pm=inv/inv.sum(); w=[r['sonuc'].strip()=='1' for r in rs].index(True)
        kods=[r['kod'] for r in rs]
        for i,r in enumerate(rs):
            t=r['yas'].split(); ym=re.match(r'(\d+)y',t[0]) if t else None
            yas=int(ym.group(1)) if ym else 0; renk=kod('renk',t[1]) if len(t)>2 else 0; cins=CINS.get(t[2],5) if len(t)>2 else 5
            irk=kod('irk',(r['grup'] or '?')[-1:]); jn,jw=JW[r['jokey']]; an,aw=AW[r['antrenor']]
            bb=0.0
            for j,b in enumerate(kods):
                if j!=i:
                    ww,m=H2[(kods[i],b)]
                    if m>0: bb+=(2*ww-m)/(m+1)
            X.append([hp[i],hp[i]-hm,hr[i],f(r['start']) or 0,yas,cins,renk,irk,kl[i],kl[i]-km,f(r['mesafe']) or 0,n,(jw+0.1)/(jn+1),jn,(aw+0.1)/(an+1),an,
                      kod('pist',r['pist']),kod('tur',(re.match(r'\W*(\w+)',r['tur'] or '') or [None,'?'])[1].upper() if r['tur'] else '?'),kod('hip',key[1]),bb/max(n-1,1)])
            meta.append((key,i,i==w,pm[i],g[i],r['at']))
    for r in rs:
        win=r['sonuc'].strip()=='1'; JW[r['jokey']][0]+=1; JW[r['jokey']][1]+=win; AW[r['antrenor']][0]+=1; AW[r['antrenor']][1]+=win
    ks=list(pos)
    for a in ks:
        for b in ks:
            if a!=b:
                H2[(a,b)][1]+=1
                if pos[a]<pos[b]: H2[(a,b)][0]+=1
X=np.array(X,float); y=np.array([m[2] for m in meta],int); pm=np.array([m[3] for m in meta]); gn=np.array([m[4] for m in meta]); keys=[m[0] for m in meta]
print('at',len(y),'koşu',len({k for k in keys}))
dates=np.array([k[0] for k in keys]); cut=np.sort(np.unique(dates))[int(len(np.unique(dates))*0.6)]; tr=dates<cut; te=~tr
import lightgbm as lgb   # sklearn HistGradientBoosting SHAP toplamsallık kontrolünü bozdu; LightGBM SHAP'ı yerel destekler
clf=lgb.LGBMClassifier(n_estimators=250,learning_rate=0.05,num_leaves=15,min_child_samples=60,reg_lambda=1.0,random_state=0,verbose=-1).fit(X[tr],y[tr])
raw=clf.predict_proba(X[te])[:,1]; kte=[k for k,t in zip(keys,te) if t]
S=collections.defaultdict(float)
for v,k in zip(raw,kte): S[k]+=v
pmod=np.array([v/S[k] for v,k in zip(raw,kte)])
def ll(p,ks,yy):
    return float(np.mean([math.log(max(pp,1e-9)) for pp,yv in zip(p,yy) if yv==1]))
print(f"TEST ({len(set(kte))} koşu): kazananın ort. log-olasılığı  model {ll(pmod,kte,y[te]):.4f} | piyasa {ll(pm[te],kte,y[te]):.4f}")
# kazananın model sırası; sürpriz kazananlar
G=collections.defaultdict(list)
for idx,(p,k) in enumerate(zip(pmod,kte)): G[k].append((p,y[te][idx],gn[te][idx],meta[np.where(te)[0][idx]][5],np.where(te)[0][idx]))
mr=[];sur=[]
for k,L in G.items():
    wi=[j for j,t in enumerate(L) if t[1]==1][0]; rank=1+sum(t[0]>L[wi][0] for t in L); mr.append(rank)
    if L[wi][2]>=10: sur.append((k,L[wi],rank))
print(f"kazananı 1. sıraya koyma: model %{100*np.mean([r==1 for r in mr]):.1f} | ilk 3: %{100*np.mean([r<=3 for r in mr]):.1f} | test sürpriz kazanan (ganyan>=10): {len(sur)} koşu, ort. model sırası {np.mean([s[2] for s in sur]):.1f} (tüm kazananlar {np.mean(mr):.1f})")
import shap
rng=np.random.RandomState(0); bg=X[tr][rng.choice(tr.sum(),500,replace=False)]
ex=shap.TreeExplainer(clf)
sidx=[s[1][4] for s in sur]; _sv=lambda A:(lambda o:o[1] if isinstance(o,list) else o)(ex.shap_values(A))
sv=_sv(X[sidx]); allsv=_sv(X[rng.choice(np.where(te)[0],2000,replace=False)])
print('\nSürpriz kazananlarda özellik katkısı (log-odds; + = model "bu at kazanabilir" dedi) | ortalama |katkı| tüm atlarda | sürprizde işareti pozitif olan oran')
for j in np.argsort(-np.abs(sv.mean(0)))[:10]:
    print(f'  {NAMES[j]:14s} ort katkı {sv[:,j].mean():+.3f} | tüm atlarda ort |katkı| {np.abs(allsv[:,j]).mean():.3f} | pozitif %{100*np.mean(sv[:,j]>0):.0f}')
print('\nEn büyük |ortalama katkı| (uzun at genelinden farkı için sürprizde / tüm uzun atlarda karşılaştırma):')
uz=np.where(te&(gn>=10))[0]; uzsv=_sv(X[rng.choice(uz,min(1500,len(uz)),replace=False)])
for j in np.argsort(-np.abs(sv.mean(0)-uzsv.mean(0)))[:6]:
    print(f'  {NAMES[j]:14s} sürprizde {sv[:,j].mean():+.3f} | tüm uzun atlarda {uzsv[:,j].mean():+.3f}')
