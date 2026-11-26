"""Gözden kaçan ne? Uzun atlarda (piyasa p<%10) piyasanın ötesindeki sinyal: piyasa logit'i sabit (init_score) tutulup gradient boosting yalnızca ARTIĞI öğrenir.
Kullanım: gozden_kacan_model.py (yalnızca ekrana yazar + veri/gozden_kacan_model.md; pip install lightgbm shap yalnızca elle)
Yöntem: at_gecmisi 2020–2026, kronolojik, sızıntısız özellikler; ilk %60 (zaman) eğitim, son %40 test. Ölçüt: test log-kaybı (yalnızca piyasa vs piyasa+model), model olasılığına göre onluk dilimlerde A/E (üst dilim >1, alt dilim <1 ise model piyasanın kaçırdığını buluyor), özellik önemi (gain) ve SHAP.
Özellikler: hp, hp farkı/sırası, start, yaş, cinsiyet, renk, ırk, kilo ve farkı, mesafe, koşan, jokey/antrenör oranı (büzülmüş), baş-başa skoru, son koşudaki sıra ve son 3 ortalaması, son koşudan beri gün, jokey değişti, mesafe farkı, pist/hipodrom değişti, bu mesafe bandında ilk-3 oranı farkı, ilk koşu, çeşit, hipodrom, ay + piyasa logit'i."""
import os,sys,glob,gzip,csv,io,re,math,collections,datetime,warnings
import numpy as np
warnings.filterwarnings('ignore')
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(K,'scripts')); import kosu_tipi
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
R=collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','*','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
CAT=collections.defaultdict(dict)
def kod(alan,v):
    d=CAT[alan]
    if v not in d and len(d)<250: d[v]=len(d)
    return d.get(v,0)
def band(m):
    m=f(m) or 0; return 0 if m<=1200 else 1 if m<=1400 else 2 if m<=1700 else 3 if m<=2100 else 4
CINS={'e':0,'a':1,'d':2,'k':3,'g':4}
JW=collections.defaultdict(lambda:[0,0]); AW=collections.defaultdict(lambda:[0,0]); H2=collections.defaultdict(lambda:[0,0])
HIST=collections.defaultdict(list)   # kod -> [(tarih,jokey,mesafe,pist,hip,sira)]
HB=collections.defaultdict(lambda:[0,0]); HA=collections.defaultdict(lambda:[0,0])
NAMES=['hp','hp_fark','hp_sira','start','yas','cinsiyet','renk','irk','kilo','kilo_fark','mesafe','kosan','jokey_oran','jokey_n','antrenor_oran','antrenor_n','pist','aile','hipodrom','bas_basa','son_sira','son3_ort','kgs','jokey_degisti','mesafe_fark','pist_hip_degisti','bant_uyum','ilk_kosu','ay','p_logit']
X=[];meta=[]
def gun(a,b): return (datetime.date.fromisoformat(a)-datetime.date.fromisoformat(b)).days
for key in sorted(R):
    rs=R[key]; g=[f(r['ganyan']) for r in rs]; b=band(rs[0]['mesafe'])
    ok=len(rs)>=5 and not any(x is None or x<=1 for x in g) and sum(r['sonuc'].strip()=='1' for r in rs)==1
    pos={r['kod']:int(r['sonuc']) for r in rs if r['sonuc'].strip().isdigit()}
    if ok:
        n=len(rs); inv=np.array([1/v for v in g]); pm=inv/inv.sum(); w=[r['sonuc'].strip()=='1' for r in rs].index(True)
        hp=[f(r['hp']) or 0 for r in rs]; kl=[f(r['kilo']) or 0 for r in rs]; hm=np.mean(hp); km=np.mean(kl); hr=(lambda h:1+(h[None,:]>h[:,None]).sum(1))(np.array(hp,float))
        kods=[r['kod'] for r in rs]; aile=kosu_tipi.aile(kosu_tipi.tur(rs[0]['tur'] or ''))
        for i,r in enumerate(rs):
            if pm[i]>=0.10: continue
            t=r['yas'].split(); ym=re.match(r'(\d+)y',t[0]) if t else None
            jn,jw=JW[r['jokey']]; an,aw=AW[r['antrenor']]; L=HIST[r['kod']]
            bb=0.0
            for j,c in enumerate(kods):
                if j!=i:
                    ww,m=H2[(kods[i],c)]
                    if m>0: bb+=(2*ww-m)/(m+1)
            if L:
                l=L[-1]; so=l[5]; s3=np.mean([x[5] for x in L[-3:]]); kg=gun(key[0],l[0]); jd=float(l[1]!=r['jokey']); md=(f(r['mesafe']) or 0)-(l[2] or 0); ph=float(l[3]!=r['pist'] or l[4]!=r['hip']); ik=0.0
                na,ta=HA[r['kod']]; nb,tb=HB[(r['kod'],b)]; bu=((tb+3*ta/na)/(nb+3)-ta/na) if na>=4 else 0.0
            else: so=s3=kg=md=bu=0.0; jd=ph=0.0; ik=1.0; so=s3=np.nan; kg=np.nan
            X.append([hp[i],hp[i]-hm,hr[i],f(r['start']) or 0,int(ym.group(1)) if ym else 0,CINS.get(t[2],5) if len(t)>2 else 5,kod('renk',t[1]) if len(t)>2 else 0,kod('irk',(r['grup'] or '?')[-1:]),kl[i],kl[i]-km,f(r['mesafe']) or 0,n,(jw+0.1)/(jn+1),jn,(aw+0.1)/(an+1),an,kod('pist',r['pist']),kod('aile',aile),kod('hip',key[1]),bb/max(n-1,1),so,s3,kg,jd,md,ph,bu,ik,int(key[0][5:7]),math.log(pm[i]/(1-pm[i]))])
            meta.append((key,i==w,float(pm[i]),r['at'],g[i]))
    for r in rs:
        win=r['sonuc'].strip()=='1'; JW[r['jokey']][0]+=1; JW[r['jokey']][1]+=win; AW[r['antrenor']][0]+=1; AW[r['antrenor']][1]+=win
        if r['sonuc'].strip().isdigit():
            p_=int(r['sonuc']); HIST[r['kod']].append((key[0],r['jokey'],f(r['mesafe']),r['pist'],r['hip'],p_)); HB[(r['kod'],b)][0]+=1; HB[(r['kod'],b)][1]+=p_<=3; HA[r['kod']][0]+=1; HA[r['kod']][1]+=p_<=3
    ks=list(pos)
    for a in ks:
        for c in ks:
            if a!=c:
                H2[(a,c)][1]+=1
                if pos[a]<pos[c]: H2[(a,c)][0]+=1
X=np.array(X,float); y=np.array([m[1] for m in meta],int); pm=np.array([m[2] for m in meta]); keys=[m[0] for m in meta]; gan=np.array([m[4] for m in meta])
dates=np.array([k[0] for k in keys]); cut=np.sort(np.unique(dates))[int(len(np.unique(dates))*0.6)]; tr=dates<cut; te=~tr
print(f'uzun at-koşu {len(y):,} | kazanan {y.sum()} | eğitim {tr.sum():,} (<{cut}) test {te.sum():,} ({y[te].sum()} kazanan)')
import lightgbm as lgb
off=np.log(pm/(1-pm))
ds=lgb.Dataset(X[tr],label=y[tr],init_score=off[tr],feature_name=NAMES,free_raw_data=False)
params=dict(objective='binary',learning_rate=0.03,num_leaves=8,min_data_in_leaf=300,feature_fraction=0.7,bagging_fraction=0.8,bagging_freq=1,lambda_l2=10.0,verbose=-1,seed=0)
m=lgb.train(params,ds,num_boost_round=250)
raw=m.predict(X[te],raw_score=True)+off[te]; pmod=1/(1+np.exp(-raw)); yy=y[te]; pbase=pm[te]
ll=lambda p:-np.mean(yy*np.log(p)+(1-yy)*np.log(1-p))
print(f'test log-kaybı: yalnızca piyasa {ll(pbase):.5f} | piyasa+model {ll(pmod):.5f} | fark {ll(pbase)-ll(pmod):+.5f} (+ = model daha iyi)')
rr=np.random.RandomState(0); idx=np.arange(len(yy)); d=[]
for _ in range(400):
    s=rr.choice(idx,len(idx)); d.append(-np.mean(yy[s]*np.log(pbase[s])+(1-yy[s])*np.log(1-pbase[s]))+np.mean(yy[s]*np.log(pmod[s])+(1-yy[s])*np.log(1-pmod[s])))
d=sorted(d); print(f'  bootstrap %95 [{d[10]:+.5f}, {d[389]:+.5f}]')
print('\nmodel olasılığına göre onluk dilimler (test, uzun atlar): gerçek / piyasa beklentisi')
dec=np.argsort(np.argsort(pmod/pbase))*10//len(pmod)   # modelin piyasaya göre oranına göre
for q in range(10):
    s=dec==q; e=pbase[s].sum(); print(f'  dilim {q+1:2d}: n={s.sum():5d} gerçek {yy[s].sum():3d} beklenen {e:6.1f} A/E {yy[s].sum()/e:.2f}')
imp=m.feature_importance('gain'); o=np.argsort(-imp)
print('\nözellik önemi (gain %):',', '.join(f'{NAMES[j]} {100*imp[j]/imp.sum():.0f}' for j in o[:12]))
try:
    import shap
    sv=shap.TreeExplainer(m).shap_values(X[te][yy==1]); sv=sv[1] if isinstance(sv,list) else sv
    print('\nKAZANAN uzun atlarda (test) SHAP ortalaması (+ = model piyasanın üstüne çıkarıyor):'); 
    for j in np.argsort(-np.abs(sv.mean(0)))[:8]: print(f'  {NAMES[j]:18s} {sv[:,j].mean():+.4f}')
except Exception as e: print('SHAP atlandı:',e)

# --- gerçek ganyan getirisi (1 TL, kapanış ganyanı): model/piyasa oranına göre onluk dilimler ---
gt=gan[te]; oran=pmod/pbase; sira=np.argsort(np.argsort(-oran))   # 0 = en yüksek oran
dt=dates[te]; orta=np.sort(np.unique(dt))[len(np.unique(dt))//2]
print('\nGERÇEK GANYAN GETİRİSİ (uzun atlara 1 TL; ROI = ortalama getiri − 1):')
def roi(sel):
    n=sel.sum(); return n,(yy[sel]*gt[sel]).sum()/n-1 if n else 0
for ad,k in (('en iyi %1',0.01),('en iyi %5',0.05),('en iyi %10',0.10),('en iyi %20',0.20),('hepsi',1.0)):
    sel=sira<int(k*len(sira)); n,r_=roi(sel); n1,r1=roi(sel&(dt<orta)); n2,r2=roi(sel&(dt>=orta))
    b=[]; ii=np.where(sel)[0]
    for _ in range(300): sb=rr.choice(ii,len(ii)); b.append((yy[sb]*gt[sb]).mean()-1)
    b=sorted(b); print(f'  {ad:10s} n={n:6d} kazanan {yy[sel].sum():4d} ROI {100*r_:+6.1f}% [%95 {100*b[7]:+.0f}, {100*b[292]:+.0f}] | ilk yarı {100*r1:+.0f}% (n={n1}) ikinci yarı {100*r2:+.0f}% (n={n2})')

# --- teşhis: en iyi %1 kimler? ---
top=sira<int(0.01*len(sira)); Xt=X[te]
print('\nTEŞHİS en iyi %1:', 'ort. piyasa p %.4f'%pbase[top].mean(), '| ort. model p %.3f'%pmod[top].mean(), '| ganyan medyan %.1f'%np.median(gt[top]))
for nm in ('hp','hp_fark','hp_sira','kosan','kgs','start','mesafe'):
    j=NAMES.index(nm); print(f'  {nm:10s} en iyi %1 medyan {np.nanmedian(Xt[top][:,j]):.1f} | tüm uzun atlar medyan {np.nanmedian(Xt[:,j]):.1f}')
import collections as _c
print('  en iyi 1 yüzde kazanma oranı %.1f%%'%(100*yy[top].mean()),'| piyasanın beklediği %.1f%%'%(100*pbase[top].mean()))
print('  örnek (tarih, hip, at, hp, hp_sira, ganyan, kazandı):')
ii=np.where(te)[0][np.where(top)[0][:8]]
for j in ii: print('   ',keys[j][0],keys[j][1],keys[j][2],meta[j][3][:14],X[j][0],X[j][2],meta[j][4],int(meta[j][1]))
