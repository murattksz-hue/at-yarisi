"""Soy etkenleri piyasaya bilgi katıyor mu? (kronolojik; her gün yalnızca önceki günlerden)
Özellikler: baba_piyasa (aygırın yavrularının piyasa A/E'si), anne_kardes (aynı anneden kardeşlerin alan A/E'si, atın kendisi hariç),
baba_yas (aygırın bu yaş grubundaki (genç / 4+) yavrularının alan A/E'si). Piyasa = ganyan (eküri tek birim), ağırlık 1.
10 katlı gün CV. Kullanım: soy_test.py sonuc_dizini [isinma_gun]"""
import sys,glob,os,re,collections,math
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
        if re.match(r'^\d+\. Kosu',c[0]): cur=dict(g=g,irk='Arap' if 'Arap' in l else 'İngiliz',h=[],ek=[]); R.append(cur); continue
        if cur is not None and 'eküridir' in l: cur['ek'].append([ad_(a) for a in re.findall(r'\(\d+\)([^,\]]+)',l)])
        if cur is not None and c[0].isdigit() and len(c)>13:
            try:o=float(c[13].replace(',','.'))
            except Exception:o=0
            y=c[2].split(); cur['h'].append(dict(ad=ad_(c[1]),pos=int(c[0]) if c[12].strip() else 99,o=o,baba=c[3].strip(),anne=c[4].strip(),genc=bool(y) and y[-1] in ('e','d')))
BP=collections.defaultdict(lambda:[0,0.0]); AK=collections.defaultdict(lambda:collections.defaultdict(lambda:[0,0.0])); BY=collections.defaultdict(lambda:[0,0.0])
gunler=sorted(set(r['g'] for r in R)); gi={g:i for i,g in enumerate(gunler)}; D=[]
for g in gunler:
    gun=[r for r in R if r['g']==g and len(r['h'])>=4]
    for r in gun:
        h=r['h']; ok=all(x['o']>1 for x in h); r['ok']=ok and sum(x['pos']==1 for x in h)==1
        if ok:
            grp={a:i for i,E in enumerate(r['ek']) for a in E}; U={}
            for x in h: U.setdefault(grp.get(x['ad'],'t'+x['ad']),[]).append(x)
            tot=sum(1/L[0]['o'] for L in U.values())
            for L in U.values():
                for x in L: x['q']=(1/x['o'])/tot/len(L)
        if gi[g]>=IS and r['ok']:
            X=[]
            for x in h:
                bp=BP[(r['irk'],x['baba'])]; kd=[v for k,v in AK[(r['irk'],x['anne'])].items() if k!=x['ad']]
                kw=sum(v[0] for v in kd); ke=sum(v[1] for v in kd); by=BY[(r['irk'],x['baba'],x['genc'])]
                X.append([math.log(x['q']),math.log((bp[0]+10)/(bp[1]+10)),math.log((kw+2)/(ke+2)),float(len(kd)==0),math.log((by[0]+5)/(by[1]+5))])
            X=np.array(X)
            for j in (1,2,4):
                col=X[:,j]; X[:,j]=np.clip((col-col.mean())/(col.std() or 1),-2.5,2.5)
            D.append((gi[g],X,np.array([x['pos']==1 for x in h],float)))
    for r in gun:   # günü geçmişe ekle
        n=len(r['h'])
        for x in r['h']:
            w=x['pos']==1
            if r['ok']: BP[(r['irk'],x['baba'])][0]+=w; BP[(r['irk'],x['baba'])][1]+=x['q']
            a=AK[(r['irk'],x['anne'])][x['ad']]; a[0]+=w; a[1]+=1/n
            BY[(r['irk'],x['baba'],x['genc'])][0]+=w; BY[(r['irk'],x['baba'],x['genc'])][1]+=1/n
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
b=cv([]); print(f"sadece piyasa: {b:.4f}",flush=True)
for ad,cols in (('baba_piyasa',[1]),('anne_kardes (+kardeşi yok)',[2,3]),('baba_yas',[4]),('üçü birlikte',[1,2,3,4])):
    l=cv(cols); print(f"  + {ad:28} {l:.4f}  fark {1000*(l-b):+.2f} binde",flush=True)
w=fit(D,[1,2,3,4]); print('ağırlıklar (tüm veri):',dict(zip(['baba_piyasa','anne_kardes','kardes_yok','baba_yas'],np.round(w,3))))
