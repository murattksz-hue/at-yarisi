"""TASLAK (yalnızca elle, bilgisayarda çalıştırılır; Actions'ta KURULU DEĞİL: pip install scikit-learn shap).
1) Piyasa (kesin ganyan) kalibrasyonu: olasılık aralığına göre gerçek/beklenen, izotonik düzeltme testi (scikit-learn).
2) Piyasasız hızlı model (HistGradientBoosting) + sürpriz kazananlar için SHAP.
UYARI: 'cinsiyet' özelliği yaş sütunundaki ikinci harften türetildi, anlamı DOĞRULANMADI (cinsiyet mi renk mi?); SHAP yorumları buna bağlı olduğu için güvenilir DEĞİL.
Ayrıca kategorik özellikler hash ile kodlandı (kaba). Düzeltme: YAPILACAK_TESTLER.md madde 3."""
import os
K0=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import glob,gzip,csv,io,re,collections,math,sys,warnings
import numpy as np
warnings.filterwarnings('ignore')
D=os.path.join(K0,'veri','at_gecmisi')
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
rows=[]
for fn in sorted(glob.glob(D+'/202[4-9]/*.csv.gz')):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): rows.append(r)
print('satır',len(rows))
R=collections.defaultdict(list)
for r in rows: R[(r['tarih'],r['hip'],r['kosu'])].append(r)
# geçerli koşular: tüm atlarda ganyan var, tek kazanan
X=[];meta=[]
JW=collections.defaultdict(lambda:[0,0]);AW=collections.defaultdict(lambda:[0,0])
for key in sorted(R):
    rs=R[key]
    g=[f(r['ganyan']) for r in rs]
    if any(v is None or v<=1 for v in g) or len(rs)<5: continue
    win=[r['sonuc'].strip()=='1' for r in rs]
    if sum(win)!=1: continue
    inv=np.array([1/v for v in g]); pm=inv/inv.sum()
    hp=[f(r['hp']) or 0 for r in rs]; st=[f(r['start']) or 0 for r in rs]; kl=[f(r['kilo']) or 0 for r in rs]
    hpm=np.mean(hp); klm=np.mean(kl)
    hp_rank=(-np.array(hp)).argsort().argsort()+1
    for i,r in enumerate(rs):
        y=re.match(r'(\d+)y',r['yas']); age=int(y.group(1)) if y else 0
        sx=r['yas'].split()[1] if len(r['yas'].split())>1 else ''
        jk,an=r['jokey'],r['antrenor']
        jn,jw=JW[jk][0],JW[jk][1]; an_,aw=AW[an][0],AW[an][1]
        X.append([hp[i],hp[i]-hpm,hp_rank[i],st[i],age,{'k':0,'d':1,'e':2}.get(sx,3),kl[i],kl[i]-klm,f(r['mesafe']) or 0,len(rs),
                  (jw+0.1)/(jn+1),jn,(aw+0.1)/(an_+1),an_,
                  hash(r['pist'])%97,hash(r['tur'])%997,hash(r['hip'])%97])
        meta.append((key,i,win[i],pm[i],g[i],r['at'],jk))
    for i,r in enumerate(rs):   # kronolojik: koşudan SONRA güncelle
        JW[r['jokey']][0]+=1;JW[r['jokey']][1]+=win[i]; AW[r['antrenor']][0]+=1;AW[r['antrenor']][1]+=win[i]
X=np.array(X,float); y=np.array([m[2] for m in meta],int); pm=np.array([m[3] for m in meta]); gn=np.array([m[4] for m in meta])
print('geçerli at',len(y),'koşu',len({m[0] for m in meta}),'kazanan oranı %.4f'%y.mean())
names=['hp','hp_fark','hp_sira','start','yas','cinsiyet','kilo','kilo_fark','mesafe','kosan','jokey_oran','jokey_n','antrenor_oran','antrenor_n','pist','tur','hipodrom']
from sklearn.metrics import brier_score_loss,log_loss
from sklearn.calibration import calibration_curve
from sklearn.isotonic import IsotonicRegression
# ---------- 1) PİYASA KALİBRASYONU
print('\n== 1) PİYASA (kesin ganyan) KALİBRASYONU, tüm atlar ==')
print('Brier %.5f  logloss %.5f'%(brier_score_loss(y,pm),log_loss(y,np.clip(pm,1e-6,1-1e-6))))
edges=[0,0.02,0.04,0.06,0.08,0.10,0.15,0.20,0.30,0.50,1.0]
print('piyasa p aralığı     n      beklenen  gerçek   A/E')
for a,b in zip(edges[:-1],edges[1:]):
    m=(pm>=a)&(pm<b)
    if m.sum(): print(f'{a:.2f}-{b:.2f}  {m.sum():8d}  {pm[m].mean():8.4f} {y[m].mean():8.4f}  {y[m].mean()/pm[m].mean():5.2f}')
print('\nganyan>=10 (sürpriz adayı):  n=%d  beklenen %.4f gerçek %.4f A/E %.2f'%((gn>=10).sum(),pm[gn>=10].mean(),y[gn>=10].mean(),y[gn>=10].mean()/pm[gn>=10].mean()))
# izotonik kalibrasyon yarar sağlıyor mu? (zaman bölmesi)
dates=np.array([m[0][0] for m in meta]); cut=np.sort(np.unique(dates))[int(len(np.unique(dates))*0.6)]
tr=dates<cut; te=~tr
iso=IsotonicRegression(out_of_bounds='clip',y_min=1e-4,y_max=1-1e-4).fit(pm[tr],y[tr]); pc=iso.predict(pm[te])
print('izotonik düzeltme (ilk %%60 öğren, kalan %%40 test): Brier %.5f -> %.5f ; logloss %.5f -> %.5f'%(
    brier_score_loss(y[te],pm[te]),brier_score_loss(y[te],pc),log_loss(y[te],np.clip(pm[te],1e-6,1-1e-6)),log_loss(y[te],np.clip(pc,1e-6,1-1e-6))))
# ---------- 2) PİYASASIZ MODEL + SHAP
print('\n== 2) PİYASASIZ MODEL (ganyan/AGF kullanmaz) ==')
from sklearn.ensemble import HistGradientBoostingClassifier
clf=HistGradientBoostingClassifier(max_iter=250,learning_rate=0.05,max_leaf_nodes=15,min_samples_leaf=60,l2_regularization=1.0,random_state=0,
    categorical_features=[14,15,16]).fit(X[tr],y[tr])
raw=clf.predict_proba(X[te])[:,1]
# koşu içi normalize
keys=[m[0] for m in meta]; kte=[k for k,t in zip(keys,te) if t]
def norm(p,ks):
    S=collections.defaultdict(float)
    for v,k in zip(p,ks): S[k]+=v
    return np.array([v/S[k] for v,k in zip(p,ks)])
pmod=norm(raw,kte)
print('TEST (görülmemiş son %%40, %d koşu): logloss  model %.5f | piyasa %.5f | havuz(tüm atlar eşit) ~ %.5f'%(len(set(kte)),log_loss(y[te],pmod),log_loss(y[te],np.clip(pm[te],1e-6,1-1e-6)),
      log_loss(y[te],np.clip(1/X[te][:,9],1e-6,1-1e-6))))
# koşu başına: kazananın model sırası ve piyasa sırası
S=collections.defaultdict(list)
for (m,p,q) in zip([meta[i] for i in np.where(te)[0]],pmod,pm[te]): S[m[0]].append((m[2],p,q,m[4],m[5]))
mr=[];pr=[]
for k,L in S.items():
    w=[i for i,t in enumerate(L) if t[0]][0]
    mr.append(1+sum(t[1]>L[w][1] for t in L)); pr.append(1+sum(t[2]>L[w][2] for t in L))
mr=np.array(mr);pr=np.array(pr)
print('kazananı 1. sıraya koyma: model %.1f%%  piyasa %.1f%% | ilk 3: model %.1f%%  piyasa %.1f%%'%(100*(mr==1).mean(),100*(pr==1).mean(),100*(mr<=3).mean(),100*(pr<=3).mean()))
# sürpriz kazananlar (ganyan>=10): model onları görüyor muydu?
sur=[(k,t) for k,L in S.items() for t in L if t[0] and t[3]>=10]
print('\nTEST dönemindeki sürpriz kazanan (ganyan>=10): %d koşu'%len(sur))
oran=[t[1]/t[2] for k,t in sur]
print('model olasılığı / piyasa olasılığı: ortalama %.2f, medyan %.2f; modelin piyasadan DAHA YÜKSEK verdiği %d/%d'%(np.mean(oran),np.median(oran),sum(o>1 for o in oran),len(oran)))
print('sürpriz kazananların model sırası: ortalama %.1f (tüm kazananlar %.1f)'%(
    np.mean([1+sum(u[1]>t[1] for u in S[k]) for k,t in sur]),mr.mean()))
# SHAP: sürpriz kazananlarda hangi özellik modeli yukarı/aşağı itti
import shap
idx=np.where(te)[0]; pos={ix:j for j,ix in enumerate(idx)}
sur_idx=[i for i in idx if y[i]==1 and gn[i]>=10]
rng=np.random.RandomState(0); bg=X[tr][rng.choice(tr.sum(),500,replace=False)]
ex=shap.TreeExplainer(clf,data=bg,feature_perturbation='interventional',model_output='raw')
sv=ex.shap_values(X[sur_idx])
mean_all=np.abs(ex.shap_values(X[rng.choice(idx,1500,replace=False)])).mean(0)
print('\nSürpriz kazananlarda ortalama SHAP katkısı (log-odds; + = model "bu at kazanabilir" dedi):')
order=np.argsort(-np.abs(sv.mean(0)))
for j in order[:8]: print(f'  {names[j]:14s} ort katkı {sv[:,j].mean():+.3f}   (tüm atlarda ort |katkı| {mean_all[j]:.3f})')
# örnek: en yüksek ganyanlı 5 sürpriz kazanan ve özellikleri
print('\nEn büyük 5 sürpriz (test dönemi) ve modelin payı:')
sur_sorted=sorted(sur,key=lambda s:-s[1][3])[:5]
for k,t in sur_sorted:
    i=[ix for ix in idx if meta[ix][0]==k and meta[ix][2]][0]
    j=np.argsort(-np.abs(ex.shap_values(X[[i]])[0]))[:3]
    s=ex.shap_values(X[[i]])[0]
    print(f'  {k[0]} {k[1]} {k[2]}. koşu  {t[4]:<22s} ganyan {t[3]:.1f}  piyasa p={t[2]:.3f}  model p={t[1]:.3f}  | en etkili: '+', '.join(f'{names[a]} {s[a]:+.2f}' for a in j))
