"""2024 verisi modele fayda sağlıyor mu? Gerçek veri: ebayi sonuç JSON'ları (.gunluk/ebayi, 2024-01 → ).
Geçmişten hesaplanan özellikler (jokey, antrenör, baba, atın kendi A/E'si) iki ayrı geçmişle hesaplanır:
  KISA: 2025-05-01'den itibaren (şu anki veri/sonuc başlangıcı)   UZUN: 2024-01-01'den itibaren
Her koşuda yalnızca o GÜNDEN ÖNCEKİ koşular kullanılır (sızıntı yok). Ağırlıklar 2025-07-01..2026-05-31 koşularında öğrenilir,
test 2026-06-01 → son gün (görülmemiş). Model A: piyasa (kesin ganyan, eküri tek birim) + özellikler. Model B: AGF'siz (HP + özellikler).
Kullanım: eski_veri_test.py .gunluk/ebayi cikti.json"""
import sys,glob,gzip,json,os,math,collections
import numpy as np
def sayi(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
KISA0,EG0,TEST0='20250501','20250701','20260601'
KOS=[]
for f in sorted(glob.glob(sys.argv[1]+'/*.json.gz')):
    g=os.path.basename(f)[:8]
    for k in json.load(gzip.open(f,'rt',encoding='utf-8')).get('kosular',[]):
        A=[a for a in k.get('atlar',[]) if not a.get('KOSMAZ') and str(a.get('SONUC') or '').isdigit()]
        if len(A)>=4: KOS.append((g,A))
KOS.sort(key=lambda r:r[0])
ST={'kisa':collections.defaultdict(lambda:[0.0,0.0]),'uzun':collections.defaultdict(lambda:[0.0,0.0])}
def ae(S,k): w,e=S.get(k,(0.0,0.0)); return math.log((w+2)/(e+2))
def anahtarlar(a): return [('j',a.get('JOKEYKODU')),('a',a.get('ANTRENORKODU')),('b',a.get('BABAKODU')),('h',a.get('KOD'))]
D=[]; i=0
while i<len(KOS):
    g=KOS[i][0]; j=i
    while j<len(KOS) and KOS[j][0]==g: j+=1
    gun=KOS[i:j]
    if g>=EG0:
        for _,A in gun:
            G=[sayi(a.get('GANYAN')) for a in A]
            if not(all(x and x>1 for x in G) and sum(a['SONUC']=='1' for a in A)==1): continue
            U=collections.defaultdict(list)
            for t,a in enumerate(A): U[('E',G[t]) if a.get('EKURI') else ('t',t)].append(t)
            tot=sum(1/G[L[0]] for L in U.values()); q=np.zeros(len(A))
            for L in U.values():
                for t in L: q[t]=(1/G[L[0]])/tot/len(L)
            hp=np.array([sayi(a.get('HANDIKAP')) or 0.0 for a in A]); hz=(hp-hp.mean())/(hp.std()+1e-9) if hp.std()>0 else hp*0
            X={}
            for s in ('kisa','uzun'):
                X[s]=np.array([[math.log(q[t]),hz[t]]+[ae(ST[s],k) for k in anahtarlar(a)] for t,a in enumerate(A)])
            D.append((g,X,next(t for t,a in enumerate(A) if a['SONUC']=='1')))
    for _,A in gun:
        n=len(A)
        for a in A:
            w=float(a['SONUC']=='1')
            for s in ('kisa','uzun'):
                if s=='kisa' and g<KISA0: continue
                for k in anahtarlar(a): ST[s][k][0]+=w; ST[s][k][1]+=1/n
    i=j
R=len(D); Hm=max(len(x[1]['kisa']) for x in D)
def dizi(s):
    X=np.zeros((R,Hm,6)); M=np.zeros((R,Hm),bool)
    for r,(g,x,w) in enumerate(D): X[r,:len(x[s])]=x[s]; M[r,:len(x[s])]=True
    return X,M
Y=np.array([w for _,_,w in D]); TE=np.array([g>=TEST0 for g,_,_ in D]); tr=np.where(~TE)[0]; te=np.where(TE)[0]
def fit(X,M,idx,cols,off):
    w=np.zeros(len(cols)); Z=X[idx][:,:,cols]; O=(X[idx][:,:,0] if off else 0.0)+np.where(M[idx],0,-50); y=Y[idx]
    for _ in range(30):
        u=O+Z@w; p=np.exp(u-u.max(1,keepdims=True)); p/=p.sum(1,keepdims=True)
        zy=Z[np.arange(len(idx)),y]; ez=(p[:,:,None]*Z).sum(1); gr=(zy-ez).sum(0)-w
        H=np.einsum('rh,rhi,rhj->ij',p,Z,Z)-np.einsum('ri,rj->ij',ez,ez)+np.eye(len(cols))
        st=np.linalg.solve(H,gr); w+=st
        if np.abs(st).max()<1e-7: break
    return w
def deg(X,M,idx,cols,off,w):
    u=(X[idx][:,:,0] if off else 0.0)+X[idx][:,:,cols]@w+np.where(M[idx],0,-50); u=u-u.max(1,keepdims=True)
    ll=u[np.arange(len(idx)),Y[idx]]-np.log(np.exp(u).sum(1)); bir=(u.argmax(1)==Y[idx]); return ll,bir
SON={}; print(f"eğitim koşusu {len(tr)} ({EG0}..{TEST0}), test koşusu {len(te)} ({TEST0}..{D[-1][0]})")
for mod,cols,off in [('A_piyasa+gecmis',[2,3,4,5],True),('B_agfsiz_hp+gecmis',[1,2,3,4,5],False)]:
    r={}
    for s in ('kisa','uzun'):
        X,M=dizi(s); w=fit(X,M,tr,cols,off); ll,bir=deg(X,M,te,cols,off,w); r[s]=(ll,bir,w)
    if off:
        X,M=dizi('uzun'); u=X[te][:,:,0]+np.where(M[te],0,-50); u=u-u.max(1,keepdims=True)
        pll=u[np.arange(len(te)),Y[te]]-np.log(np.exp(u).sum(1)); print(f"  sadece piyasa: LL {pll.mean():.4f}, favori %{100*(u.argmax(1)==Y[te]).mean():.1f}")
    d=r['uzun'][0]-r['kisa'][0]; se=d.std()/math.sqrt(len(d))
    SON[mod]={s:dict(ll=round(float(r[s][0].mean()),4),birinci=round(100*float(r[s][1].mean()),1),agirlik=[round(float(x),3) for x in r[s][2]]) for s in r}
    SON[mod]['fark_binde']=round(1000*float(d.mean()),2); SON[mod]['z']=round(float(d.mean()/se),2)
    print(f"{mod}: KISA LL {r['kisa'][0].mean():.4f} 1.seçim %{100*r['kisa'][1].mean():.1f} | UZUN LL {r['uzun'][0].mean():.4f} 1.seçim %{100*r['uzun'][1].mean():.1f} | fark binde {1000*d.mean():+.2f} (z {d.mean()/se:+.2f})",flush=True)
json.dump(dict(egitim=len(tr),test=len(te),sonuc=SON),open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
