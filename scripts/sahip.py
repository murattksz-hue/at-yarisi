"""Sahip (at sahibi) raporu ve testi (gerçek TJK sonuçları). Kullanım: antrenor.py sonuc_dizini rapor.json [isinma_gun]
Rapor: koşu, galibiyet, %, alan A/E, piyasa A/E (iki dönem; eküri tek birim), favori dönüşümü, ilk koşan ve uzun aradan (>60 gün) dönen atlarla A/E, hipodrom.
Test (kronolojik, piyasa ağırlığı 1, 10 katlı gün CV): sahip_piyasa, sahip_ilk_kosu, sahip_uzun_ara, sahip_hipodrom, ayrıca sahip_alan (alan A/E)."""
import sys,glob,os,re,json,collections,math,datetime,statistics
import numpy as np
TAGS={'KG','K','DB','SK','SKG','GKR','ÖG','BB','YP','KK','TB','SKK','ÖN','GK','SGKR','KUL','BH','DS'}
def ad_(n):
    t=n.replace('(Koşmaz)','').split()
    while len(t)>1 and t[-1] in TAGS: t.pop()
    return ' '.join(t)
SD,OUT=sys.argv[1:3]; IS=int(sys.argv[3]) if len(sys.argv)>3 else 45
R=[]
for f in sorted(glob.glob(SD+'/*.csv')):
    b=os.path.basename(f); g=b[:10]; cur=None
    for l in open(f,encoding='utf-8-sig'):
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]): cur=dict(g=g,hip=b[11:-4],irk='Arap' if 'Arap' in l else 'İngiliz',h=[],ek=[]); R.append(cur); continue
        if cur is not None and 'eküridir' in l: cur['ek'].append([ad_(a) for a in re.findall(r'\(\d+\)([^,\]]+)',l)])
        if cur is not None and c[0].isdigit() and len(c)>13:
            try:o=float(c[13].replace(',','.'))
            except Exception:o=0
            cur['h'].append(dict(ad=ad_(c[1]),pos=int(c[0]) if c[12].strip() else 99,o=o,ant=c[7].strip()))
gunler=sorted(set(r['g'] for r in R)); gi={g:i for i,g in enumerate(gunler)}; orta=gunler[len(gunler)//2]
SON={}   # at -> son koşu tarihi
T=collections.defaultdict(lambda:dict(atlar=set(),ekb=0,ekw=0,k=0,w=0,e=0.0,q=[0.0,0.0],wq=[0,0],fb=0,fw=0,ilk=[0,0.0],uzun=[0,0.0],hip=collections.defaultdict(lambda:[0,0])))
P=collections.defaultdict(lambda:[0,0.0]); PI=collections.defaultdict(lambda:[0,0.0]); PU=collections.defaultdict(lambda:[0,0.0]); PH=collections.defaultdict(lambda:[0,0.0]); PG=collections.defaultdict(lambda:[0,0.0]); D=[]
for g in gunler:
    gd=datetime.date.fromisoformat(g); gun=[r for r in R if r['g']==g and len(r['h'])>=4]
    for r in gun:
        h=r['h']; ok=all(x['o']>1 for x in h); r['ok']=ok and sum(x['pos']==1 for x in h)==1
        if ok:
            grp={a:i for i,E in enumerate(r['ek']) for a in E}; U={}
            for x in h: U.setdefault(grp.get(x['ad'],'t'+x['ad']),[]).append(x)
            tot=sum(1/L[0]['o'] for L in U.values()); fav=min(L[0]['o'] for L in U.values())
            for L in U.values():
                for x in L: x['q']=(1/x['o'])/tot/len(L); x['fav']=x['o']==fav
        for x in h:
            s=SON.get(x['ad']); x['ilk']=s is None; x['uzun']=s is not None and (gd-s).days>60
        if gi[g]>=IS and r['ok']:
            X=[]
            for x in h:
                a=x['ant']; pa=P[a]; gen=PG[a]; ae=(gen[0]+5)/(gen[1]+5)
                X.append([math.log(x['q']),math.log((pa[0]+10)/(pa[1]+10)),math.log(ae),
                          math.log((PI[a][0]+3)/(PI[a][1]+3)/ae) if x['ilk'] else 0.0,
                          math.log((PU[a][0]+3)/(PU[a][1]+3)/ae) if x['uzun'] else 0.0,
                          math.log((PH[(a,r['hip'])][0]+5)/(PH[(a,r['hip'])][1]+5)/ae)])
            X=np.array(X)
            for j in (1,2,5):
                col=X[:,j]; X[:,j]=np.clip((col-col.mean())/(col.std() or 1),-2.5,2.5)
            D.append((gi[g],X,np.array([x['pos']==1 for x in h],float)))
    for r in gun:
        n=len(r['h'])
        for x in r['h']:
            a=x['ant']; w=x['pos']==1; t=T[a]; yr=0 if g<orta else 1
            t['atlar'].add(x['ad'])
            if any(x['ad'] in E for E in r['ek']): t['ekb']+=1; t['ekw']+=w
            t['k']+=1; t['w']+=w; t['e']+=1/n; t['hip'][r['hip']][0]+=1; t['hip'][r['hip']][1]+=w
            if r['ok']:
                t['q'][yr]+=x['q']; t['wq'][yr]+=w; P[a][0]+=w; P[a][1]+=x['q']
                if x['fav']: t['fb']+=1; t['fw']+=w
            if x['ilk']: t['ilk'][0]+=w; t['ilk'][1]+=1/n; PI[a][0]+=w; PI[a][1]+=1/n
            if x['uzun']: t['uzun'][0]+=w; t['uzun'][1]+=1/n; PU[a][0]+=w; PU[a][1]+=1/n
            PH[(a,r['hip'])][0]+=w; PH[(a,r['hip'])][1]+=1/n; PG[a][0]+=w; PG[a][1]+=1/n
            SON[x['ad']]=gd
L=sorted([(a,v) for a,v in T.items() if v['k']>=200],key=lambda kv:-kv[1]['w'])
print(f"===== En çok kazanan 30 sahip (200+ koşu; {len(L)} sahip) =====")
print(f"{'sahip':22} {'at':>4} {'eküri':>9} {'koşu':>5} {'gal.':>5} {'%':>5} {'alan A/E':>8} {'piyasa A/E 1./2.':>17} {'favori':>9} {'ilk koşu A/E':>13} {'uzun ara A/E':>13}")
for a,v in L[:30]:
    pa=[f"{v['wq'][i]/v['q'][i]:.2f}" if v['q'][i]>5 else '-' for i in (0,1)]
    f_=lambda z:f"{z[0]/z[1]:.2f}" if z[1]>2 else '-'
    print(f"{a[:22]:22} {len(v['atlar']):4} {v['ekw']:>3}/{v['ekb']:<5} {v['k']:5} {v['w']:5} {100*v['w']/v['k']:5.1f} {v['w']/v['e']:8.2f} {pa[0]:>8}/{pa[1]:<8} {v['fw']:>3}/{v['fb']:<5} {f_(v['ilk']):>13} {f_(v['uzun']):>13}")
PP=[(v['wq'][0]/v['q'][0],v['wq'][1]/v['q'][1]) for v in T.values() if v['q'][0]>8 and v['q'][1]>8]
print(f"\nSahip piyasa A/E kalıcılığı: {len(PP)} sahip, 1. ve 2. dönem korelasyonu {statistics.correlation([a for a,_ in PP],[b for _,b in PP]):.2f}")
json.dump({a:dict(at=len(v['atlar']),kosu=v['k'],galibiyet=v['w'],yuzde=round(100*v['w']/v['k'],1),alan_ae=round(v['w']/v['e'],2),
    piyasa_ae=[round(v['wq'][i]/v['q'][i],2) if v['q'][i]>5 else None for i in (0,1)],favori=[v['fw'],v['fb']],
    hipodrom={h:dict(kosu=x[0],galibiyet=x[1]) for h,x in v['hip'].items()}) for a,v in T.items() if v['k']>=20},open(OUT,'w'),ensure_ascii=False)
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
for ad,cols in (('sahip_piyasa',[1]),('sahip_alan',[2]),('sahip_ilk_kosu',[3]),('sahip_uzun_ara',[4]),('sahip_hipodrom',[5]),('hepsi',[1,2,3,4,5])):
    l=cv(cols); print(f"  + {ad:14} {l:.4f}  fark {1000*(l-b):+.2f} binde",flush=True)
