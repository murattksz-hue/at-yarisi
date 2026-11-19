"""Ganyan projesinden (github.com/fatihbozdag/Ganyan, MIT) alınan özellik fikirleri piyasaya bilgi katıyor mu?
Gerçek veri: ebayi sonuç JSON'ları (.gunluk/ebayi, 2024-01 → ). Piyasa = kesin ganyan (eküri tek birim). Koşullu logit, piyasa ağırlığı 1,
10 katlı GÜN bazlı çapraz doğrulama; her at için yalnızca o günden ÖNCEKİ koşuları kullanılır (sızıntı yok). Hızlı: vektörel Newton.
Kullanım: ganyan_ozellik_test.py .gunluk/ebayi cikti.json"""
import sys,glob,gzip,json,os,math,collections
import numpy as np
def sayi(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
F=sorted(glob.glob(sys.argv[1]+'/*.json.gz')); KOS=[]
for f in F:
    g=os.path.basename(f)[:8]
    for k in json.load(gzip.open(f,'rt',encoding='utf-8')).get('kosular',[]):
        A=[a for a in k.get('atlar',[]) if not a.get('KOSMAZ') and str(a.get('SONUC') or '').isdigit()]
        if len(A)<4: continue
        KOS.append(dict(g=g,mes=sayi(k.get('MESAFE')),pist=(k.get('PIST') or '').lower(),A=A))
KOS.sort(key=lambda r:r['g']); gunler=sorted({r['g'] for r in KOS}); gi={g:i for i,g in enumerate(gunler)}
ISIN=60; HIS=collections.defaultdict(list); D=[]
ADLAR=['s20_edge','dinlenme_kisa(<=10g)','dinlenme_uzun(46-90g)','dinlenme_cok_uzun(>90g)','kilo_fark','mesafe_fark','pist_degisti']
for r in KOS:
    A=r['A']; G=[sayi(a.get('GANYAN')) for a in A]
    if all(x and x>1 for x in G) and sum(a['SONUC']=='1' for a in A)==1 and gi[r['g']]>=ISIN:
        U=collections.defaultdict(list)
        for i,a in enumerate(A): U[('E',G[i]) if a.get('EKURI') else ('t',i)].append(i)
        tot=sum(1/G[L[0]] for L in U.values()); q=np.zeros(len(A))
        for L in U.values():
            for i in L: q[i]=(1/G[L[0]])/tot/len(L)
        s20=[sayi(a.get('SON20')) for a in A]; v=[x for x in s20 if x is not None]; m=sum(v)/len(v) if v else 0
        X=[]
        for i,a in enumerate(A):
            H=HIS.get(a.get('KOD')); kgs=sayi(a.get('KGS')); kilo=sayi(a.get('KILO')); p=H[-1] if H else None
            X.append([math.log(q[i]),
                ((s20[i]-m)/m) if (s20[i] is not None and m>0) else 0.0,
                float(kgs is not None and kgs<=10),float(kgs is not None and 46<=kgs<=90),float(kgs is not None and kgs>90),
                max(-2,min(2,(kilo-p['kilo'])/3)) if (p and kilo and p['kilo']) else 0.0,
                max(-.5,min(.5,(r['mes']-p['mes'])/p['mes'])) if (p and r['mes'] and p['mes']) else 0.0,
                float(p is not None and bool(p['pist']) and p['pist']!=r['pist'])])
        D.append((gi[r['g']],np.array(X),int(next(i for i,a in enumerate(A) if a['SONUC']=='1'))))
    for a in A: HIS[a.get('KOD')].append(dict(kilo=sayi(a.get('KILO')),mes=r['mes'],pist=r['pist']))
# dolgulu diziler
R=len(D); Hm=max(len(x[1]) for x in D); NF=len(ADLAR)
X=np.zeros((R,Hm,NF+1)); M=np.zeros((R,Hm),bool); Y=np.zeros(R,int); GUN=np.zeros(R,int)
for j,(g,x,w) in enumerate(D): X[j,:len(x)]=x; M[j,:len(x)]=True; Y[j]=w; GUN[j]=g
X[~M,0]=-50
def fit(idx,cols,lam=1.0):
    w=np.zeros(len(cols)); Z=X[idx][:,:,cols]; off=X[idx][:,:,0]; y=Y[idx]
    for _ in range(25):
        u=off+Z@w; p=np.exp(u-u.max(1,keepdims=True)); p/=p.sum(1,keepdims=True)
        zy=Z[np.arange(len(idx)),y]; ez=(p[:,:,None]*Z).sum(1)
        gr=(zy-ez).sum(0)-lam*w
        Hs=np.einsum('rh,rhi,rhj->ij',p,Z,Z)-np.einsum('ri,rj->ij',ez,ez)+lam*np.eye(len(cols))
        st=np.linalg.solve(Hs,gr); w+=st
        if np.abs(st).max()<1e-6: break
    return w
def ll(idx,cols,w):
    u=X[idx][:,:,0]+(X[idx][:,:,cols]@w if cols else 0); u=u-u.max(1,keepdims=True)
    return u[np.arange(len(idx)),Y[idx]]-np.log(np.exp(u).sum(1))
fold=np.array([g%10 for g in GUN])
def cv(cols):
    out=np.zeros(R)
    for f in range(10):
        te=np.where(fold==f)[0]; tr=np.where(fold!=f)[0]
        out[te]=ll(te,cols,fit(tr,cols) if cols else None)
    return out
b=cv([]); yari=GUN>=np.median(GUN)
print(f"test koşusu {R} ({gunler[ISIN][:4]}-{gunler[ISIN][4:6]} → {gunler[-1][:4]}-{gunler[-1][4:6]}) | sadece piyasa {b.mean():.4f}")
S={}
gruplar={'s20_edge':[1],'dinlenme (3 kova)':[2,3,4],'kilo_fark':[5],'mesafe_fark':[6],'pist_degisti':[7]}
for ad,c in gruplar.items():
    l=cv(c); d=l-b; w=fit(np.arange(R),c)
    S[ad]=dict(binde=round(1000*d.mean(),2),ilk_yari=round(1000*d[~yari].mean(),2),ikinci_yari=round(1000*d[yari].mean(),2),agirlik=[round(x,3) for x in w])
    print(f"  + {ad:20} fark binde {1000*d.mean():+6.2f} | ilk yarı {1000*d[~yari].mean():+6.2f} ikinci yarı {1000*d[yari].mean():+6.2f} | ağırlık {np.round(w,3)}",flush=True)
iyi=[c for ad,c in gruplar.items() if S[ad]['ilk_yari']>0.3 and S[ad]['ikinci_yari']>0.3]
if iyi:
    c=sorted(sum(iyi,[])); l=cv(c); d=l-b
    print(f"iki yarıda da artı olanlar birlikte {c}: binde {1000*d.mean():+.2f} (ilk {1000*d[~yari].mean():+.2f}, ikinci {1000*d[yari].mean():+.2f})"); S['birlikte']=dict(kolonlar=c,binde=round(1000*d.mean(),2))
json.dump(dict(kosu=R,piyasa=round(float(b.mean()),4),sonuc=S),open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
