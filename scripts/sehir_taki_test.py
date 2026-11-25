"""Şehir ve takı değişikliği piyasaya bilgi katıyor mu? (form_test altyapısı). Son 6 koşu formunun çeşitleri piyasaya bilgi katıyor mu? (kronolojik, gerçek sonuçlar; piyasa ağırlığı 1, 10 katlı gün CV)
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
        if re.match(r'^\d+\. Kosu',c[0]): cur=dict(hip=os.path.basename(f)[11:-4],g=g,irk='Arap' if 'Arap' in l else 'İngiliz',pist=next((p for p in ('Kum','Çim','Sentetik') if p in l),'?'),h=[],ek=[]); R.append(cur); continue
        if cur is not None and 'eküridir' in l: cur['ek'].append([ad_(a) for a in re.findall(r'\(\d+\)([^,\]]+)',l)])
        if cur is not None and c[0].isdigit() and len(c)>13:
            try:o=float(c[13].replace(',','.'))
            except Exception:o=0
            t_=c[1].replace('(Koşmaz)','').split(); tg=set()
            while len(t_)>1 and t_[-1] in TAGS: tg.add(t_.pop())
            cur['h'].append(dict(ad=ad_(c[1]),pos=int(c[0]) if c[12].strip() else 99,o=o,tg=frozenset(tg)))
FEAT=['sehir_degisti','sehir_degisti_burada_kazanmis','taki_degisti','taki_eklendi','taki_cikarildi','bu_taki_ile_kazanmis']
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
            H=HIS[(r['irk'],x['ad'])]; son=H[-1] if H else None
            if son:
                sd=son[3]!=r['hip']; bk=any(y[3]==r['hip'] and y[1]==1 for y in H)
                X.append([math.log(x['q']),float(sd),float(sd and bk),float(son[4]!=x['tg']),float(bool(x['tg']-son[4])),float(bool(son[4]-x['tg'])),float(any(y[1]==1 and y[4]==x['tg'] for y in H))])
            else: X.append([math.log(x['q']),0,0,0,0,0,0])
        X=np.array(X,float)
        D.append((gi[g],X,np.array([x['pos']==1 for x in h],float)))
    for r in gun:
        n=len(r['h'])
        for x in r['h']: HIS[(r['irk'],x['ad'])].append((min(x['pos'],n)/n,x['pos'],r['pist'],r['hip'],x['tg']))
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
