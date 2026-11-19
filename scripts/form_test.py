"""Son 6 koşu formunun çeşitleri piyasaya bilgi katıyor mu? (kronolojik, gerçek sonuçlar; piyasa ağırlığı 1, 10 katlı gün CV)
Göreli derece = bitiş sırası / at sayısı (küçük = iyi). Kullanım: form_test.py sonuc_dizini [isinma_gun]"""
import sys,glob,os,re,collections,math,statistics
import numpy as np
TAGS={'KG','K','DB','SK','SKG','GKR','ÖG','BB','YP','KK','TB','SKK','ÖN','GK','SGKR','KUL','BH','DS'}
def ad_(n):
    t=n.replace('(Koşmaz)','').split()
    while len(t)>1 and t[-1] in TAGS: t.pop()
    return ' '.join(t)
SD=sys.argv[1]; IS=int(sys.argv[2]) if len(sys.argv)>2 else 45
R=[]
for f in sorted(glob.glob(SD+'/*.csv')):
    g=os.path.basename(f)[:10]; cur=None
    for l in open(f,encoding='utf-8-sig'):
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]): cur=dict(g=g,irk='Arap' if 'Arap' in l else 'İngiliz',pist=next((p for p in ('Kum','Çim','Sentetik') if p in l),'?'),h=[],ek=[]); R.append(cur); continue
        if cur is not None and 'eküridir' in l: cur['ek'].append([ad_(a) for a in re.findall(r'\(\d+\)([^,\]]+)',l)])
        if cur is not None and c[0].isdigit() and len(c)>13:
            try:o=float(c[13].replace(',','.'))
            except:o=0
            cur['h'].append(dict(ad=ad_(c[1]),pos=int(c[0]) if c[12].strip() else 99,o=o))
FEAT=['son1','son3_ort','son6_ort','agirlikli6','gidisat','istikrarsizlik','ilk3_sayisi','galibiyet_sayisi','pist_son6','form_yok']
HIS=collections.defaultdict(list); gunler=sorted(set(r['g'] for r in R)); gi={g:i for i,g in enumerate(gunler)}; D=[]
for g in gunler:
    gun=[r for r in R if r['g']==g and len(r['h'])>=4]
    for r in gun:
        h=r['h']; n=len(h)
        if not all(x['o']>1 for x in h) or sum(x['pos']==1 for x in h)!=1: r['ok']=False; continue
        r['ok']=True
        if gi[g]<IS: continue
        grp={a:i for i,E in enumerate(r['ek']) for a in E}; U={}
        for x in h: U.setdefault(grp.get(x['ad'],'t'+x['ad']),[]).append(x)
        tot=sum(1/L[0]['o'] for L in U.values()); X=[]
        for L in U.values():
            for x in L: x['q']=(1/x['o'])/tot/len(L)
        for x in h:
            H=HIS[(r['irk'],x['ad'])][-6:]; rd=[y[0] for y in H]
            if rd:
                w=[0.5**(len(rd)-1-i) for i in range(len(rd))]
                ps=[y[0] for y in H if y[2]==r['pist']]
                X.append([math.log(x['q']),rd[-1],statistics.mean(rd[-3:]),statistics.mean(rd),sum(a*b for a,b in zip(w,rd))/sum(w),
                          (statistics.mean(rd[-3:])-statistics.mean(rd[:-3])) if len(rd)>=4 else 0.0,statistics.pstdev(rd) if len(rd)>=3 else 0.0,
                          sum(y[1]<=3 for y in H),sum(y[1]==1 for y in H),statistics.mean(ps) if ps else np.nan,0.0])
            else: X.append([math.log(x['q'])]+[np.nan]*8+[np.nan,1.0])
        X=np.array(X,float)
        for j in range(1,10):
            col=X[:,j]; ok=np.isfinite(col); z=np.zeros(len(col))
            if ok.sum()>1 and col[ok].std()>0: z[ok]=np.clip((col[ok]-col[ok].mean())/col[ok].std(),-2.5,2.5)
            X[:,j]=z
        X[:,1:7]*=-1; X[:,9]*=-1   # derece/gidişat/istikrarsızlık: küçük = iyi → işaret çevrildi (artı = iyi); istikrarsızlık için artı = istikrarlı
        D.append((gi[g],X,np.array([x['pos']==1 for x in h],float)))
    for r in gun:
        n=len(r['h'])
        for x in r['h']: HIS[(r['irk'],x['ad'])].append((min(x['pos'],n)/n,x['pos'],r['pist']))
print('test koşusu:',len(D),flush=True)
def fit(DD,cols,it=250,lr=0.15,lam=2.0):
    w=np.zeros(len(cols))
    for _ in range(it):
        gr=np.zeros(len(cols))
        for _,X,y in DD:
            u=X[:,0]+X[:,cols]@w; p=np.exp(u-u.max()); p/=p.sum(); gr+=X[:,cols].T@(y-p)
        w+=lr*(gr-lam*w)/len(DD)
    return w
def cv(cols):
    days=sorted(set(d for d,_,_ in D)); fold={d:i%10 for i,d in enumerate(days)}; ll=0
    for f in range(10):
        w=fit([o for o in D if fold[o[0]]!=f],cols) if cols else None
        for d,X,y in D:
            if fold[d]!=f: continue
            u=X[:,0]+(X[:,cols]@w if cols else 0); p=np.exp(u-u.max()); p/=p.sum(); ll+=math.log(p[y==1][0])
    return ll/len(D)
b=cv([]); print(f"sadece piyasa: {b:.4f}",flush=True); sonuc={}
for j,ad in enumerate(FEAT,1):
    l=cv([j]); sonuc[ad]=l-b; print(f"  + {ad:16} {l:.4f}  fark {1000*(l-b):+.2f} binde",flush=True)
iyi=[j for j,ad in enumerate(FEAT,1) if sonuc[ad]>0.0003]
if iyi:
    l=cv(iyi); w=fit(D,iyi); print(f"işe yarayanlar birlikte {[FEAT[j-1] for j in iyi]}: fark {1000*(l-b):+.2f} binde; ağırlıklar {dict(zip([FEAT[j-1] for j in iyi],np.round(w,3)))}")
