"""Bütün parçalar birlikte: piyasa (ganyan, eküri düzeltmeli) + doğrulanmış geçmiş etkenleri + galop.
Kullanım: tam_test.py sonuc_dizini galop_dizini
Çıktı: 10 katlı gün bazlı CV log-olabilirlik, kalibrasyon tablosu, değer bahsi getirisi (sabit ve 1/4 Kelly)."""
import sys,os,json,math,datetime,collections
import numpy as np
SD,GD=sys.argv[1:3]; BURA=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(BURA,'ozellik_test2.py'),encoding='utf-8').read().split("print('test koşusu:'")[0]
sys.argv=['x',SD,'45']; G_={'__name__':'__main__','__file__':os.path.join(BURA,'ozellik_test2.py')}; exec(compile(src,'ozellik_test2','exec'),G_)
ORN,META,FEAT=G_['ORN'],G_['META'],G_['FEAT']
SEC=['pist_mesafe_galibi','pist_galibi','deneyim','sahip','hiz_son','hiz_en_iyi3']; C=[FEAT.index(k)+1 for k in SEC]
GAL={}; D=[]
for (gi,X,y),(bh,adlar,oran,birim) in zip(ORN,META):
    gf=os.path.join(GD,bh+'.json')
    if not os.path.exists(gf): continue
    if bh not in GAL: GAL[bh]=json.load(open(gf,encoding='utf-8'))
    gun=datetime.date.fromisoformat(bh[:10]); Gx=[]
    for a in adlar:
        L=[i for i in GAL[bh].get(a,{}).get('idmanlar',[]) if datetime.datetime.strptime(i['tarih'],'%d.%m.%Y').date()<gun]
        d30=[i for i in L if (gun-datetime.datetime.strptime(i['tarih'],'%d.%m.%Y').date()).days<=30]
        t4=[i['split'].get('400') for i in d30 if i['split'].get('400')]; gn=(gun-datetime.datetime.strptime(L[0]['tarih'],'%d.%m.%Y').date()).days if L else None
        Gx.append([min(t4) if t4 else np.nan,float(not t4),float(gn is not None and gn<=7),min(len(d30),5)/5,float(bool(L) and L[0].get('efor')=='Çalışarak')])
    Gx=np.array(Gx,float); v=Gx[:,0]; ok=np.isfinite(v); z=np.zeros(len(v))
    if ok.sum()>1 and v[ok].std()>0: z[ok]=np.clip(-(v[ok]-v[ok].mean())/v[ok].std(),-2.5,2.5)
    Gx[:,0]=z
    D.append((gi,np.hstack([X[:,[0]+C],Gx]),y,np.array(oran),birim))
print('galop verisi olan test koşusu:',len(D))
def fit(DD,cols,it=300,lr=0.15,lam=2.0):
    w=np.zeros(len(cols))
    for _ in range(it):
        gr=np.zeros(len(cols))
        for _,X,y,_,_ in DD:
            u=X[:,0]+X[:,cols]@w; p=np.exp(u-u.max()); p/=p.sum(); gr+=X[:,cols].T@(y-p)
        w+=lr*(gr-lam*w)/len(DD)
    return w
GECMIS=list(range(1,1+len(C))); GALOP=list(range(1+len(C),6+len(C)))
days=sorted(set(d[0] for d in D)); fold={d:i%10 for i,d in enumerate(days)}
TAH={k:[None]*len(D) for k in ('piyasa','gecmis','tam')}
for f in range(10):
    tr=[d for d in D if fold[d[0]]!=f]; W={'piyasa':None,'gecmis':fit(tr,GECMIS),'tam':fit(tr,GECMIS+GALOP)}
    for i,(gi,X,y,o,b) in enumerate(D):
        if fold[gi]!=f: continue
        for k,cols in (('piyasa',[]),('gecmis',GECMIS),('tam',GECMIS+GALOP)):
            u=X[:,0]+(X[:,cols]@W[k] if cols else 0); p=np.exp(u-u.max()); p/=p.sum(); TAH[k][i]=p
n=len(D)
for k in TAH: print(f"{k:8} log-olabilirlik {np.mean([math.log(TAH[k][i][D[i][2]==1][0]) for i in range(n)]):.4f}")
# kalibrasyon (tam model; eküri birimi)
print("\nKalibrasyon (tam model, bahis birimi): tahmin aralığı | birim sayısı | ortalama tahmin | gerçek kazanma")
K=collections.defaultdict(lambda:[0,0.0,0])
B=[]   # (p_birim, q_birim, oran, kazandı)
for i,(gi,X,y,o,b) in enumerate(D):
    p=TAH['tam'][i]; q=np.exp(X[:,0]); U=collections.defaultdict(lambda:[0.0,0.0,0,0])
    for j,key in enumerate(b): U[key][0]+=p[j]; U[key][1]+=q[j]; U[key][2]=o[j]; U[key][3]|=int(y[j])
    for pu,qu,ou,w in U.values():
        kv=min(int(pu*20),9); K[kv][0]+=1; K[kv][1]+=pu; K[kv][2]+=w; B.append((pu,qu,ou,w))
for kv in sorted(K):
    a=K[kv]; print(f"  %{5*kv:>2}-{5*kv+5:<3} {a[0]:6} {100*a[1]/a[0]:6.1f}% {100*a[2]/a[0]:6.1f}%")
print("\nDeğer bahsi (tam model; ganyan = koşu sonrası kesin oran, gerçekte bahis anında bilinmez):")
for esik in (1.1,1.2,1.3,1.5):
    S=[x for x in B if x[0]>esik*x[1] and x[2]<=30 and x[0]>=0.05]
    if not S: continue
    yat=len(S); don=sum(x[2] for x in S if x[3])
    kel=[max(0.0,(x[0]*x[2]-1)/(x[2]-1))/4 for x in S]; ky=sum(kel); kd=sum(k*x[2] for k,x in zip(kel,S) if x[3])
    print(f"  p > {esik}×piyasa: {yat} bahis, kazanan {sum(x[3] for x in S)}, sabit 1 TL getiri %{100*don/yat:.1f} | 1/4 Kelly getiri %{100*kd/ky if ky else 0:.1f}")
