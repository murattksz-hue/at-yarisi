"""2. tur: HP değişimi, pist-mesafe galibi, dinlenme, deneyim, antrenör-jokey, sahip. Literatürdeki etkenleri kendi verimizde test eder (Benter 2. aşama: piyasa + özellik).
Kullanım: ozellik_test.py sonuc_dizini [isinma_gun_sayisi]
Her atın geçmişi yalnızca ÖNCEKİ koşulardan kurulur. Test: piyasa log-olasılığı sabit (ağırlık 1),
özellik ağırlıkları gün bazlı 10 katlı çapraz doğrulamayla öğrenilir, dışarıda kalan günlerde ölçülür."""
import sys,glob,os,re,json,collections,math,statistics
import numpy as np
SD=sys.argv[1]; ISINMA=int(sys.argv[2]) if len(sys.argv)>2 else 45
TAGS={'KG','K','DB','SK','SKG','GKR','ÖG','BB','YP','KK','TB','SKK','ÖN','GK','SGKR','KUL','BH','DS'}
def ayir(n):
    t=n.replace('(Koşmaz)','').split(); tg=set()
    while len(t)>1 and t[-1] in TAGS: tg.add(t.pop())
    return ' '.join(t),tg
def sn(x):
    m=re.match(r'(\d+):(\d+)\.(\d+)',x.strip()) or re.match(r'(\d+)\.(\d+)\.(\d+)',x.strip())
    return int(m.group(1))*60+int(m.group(2))+int(m.group(3))/100 if m else None
def tl(x):
    m=re.search(r'1\.\)([\d.]+)',x); return float(m.group(1).replace('.','')) if m else None
# ---- tüm sonuçları oku
R=[]
for f in sorted(glob.glob(SD+'/*.csv')):
    b=os.path.basename(f); g=b[:10]; hip=b[11:-4]; cur=None; ln=open(f,encoding='utf-8-sig').read().splitlines()
    for i,l in enumerate(ln):
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]):
            m=re.search(r'(\d{3,4})m',l); pr=tl(ln[i+2]) if i+2<len(ln) else None
            cur=dict(g=g,hip=hip,irk='Arap' if 'Arap' in l else 'İngiliz',pist=next((p for p in ('Kum','Çim','Sentetik') if p in l),'?'),m=int(m.group(1)) if m else 0,odul=pr,h=[],ekuri=[]); R.append(cur); continue
        if cur is not None and 'eküridir' in l:
            cur['ekuri'].append([ayir(a)[0] for a in re.findall(r'\(\d+\)([^,\]]+)',l)])
        if cur is not None and c[0].isdigit() and len(c)>13:
            try:o=float(c[13].replace(',','.'))
            except:o=0
            ad,tg=ayir(c[1]); kg=re.match(r'([\d,]+)',c[5])
            cur['h'].append(dict(ad=ad,tg=tg,pos=int(c[0]) if c[12].strip() else 99,o=o,t=sn(c[12]),kg=float(kg.group(1).replace(',','.')) if kg else None,
                jok=c[6].replace(' AP','').strip(),ant=c[8].strip(),sah=c[7].strip(),hp=int(c[11]) if c[11].isdigit() else None))
R=[r for r in R if len(r['h'])>=4 and r['m']]
# ---- hız puanı: par (önceki günlerin kazanan süre medyanı) + günlük pist değişkeni
gunler=sorted(set(r['g'] for r in R)); PAR=collections.defaultdict(list)
HIS=collections.defaultdict(list); AJ=collections.defaultdict(lambda:[0,0.0]); SH=collections.defaultdict(lambda:[0,0.0]); TR=collections.defaultdict(list); JR=collections.defaultdict(list); JH=collections.defaultdict(lambda:[0,0.0]); JK=collections.defaultdict(lambda:[0,0.0])
def par(r): L=PAR[(r['hip'],r['pist'],r['m'],r['irk'])]; return statistics.median(L) if len(L)>=4 else None
def ant_ae(a,g):  # antrenör: son 60 gün, alan beklentisine göre
    L=[x for x in TR[a] if x[0]>=g-60]; w=sum(x[1] for x in L); e=sum(x[2] for x in L); return (w+3)/(e+3)
def jform(j,g):
    L=[x for x in JR[j] if x[0]>=g-30]; w=sum(x[1] for x in L); e=sum(x[2] for x in L); return (w+3)/(e+3)
def jae(j): s=JK[j]; return (s[0]+10)/(s[1]+10)
ORN=[]  # (gün, özellik matrisi, kazanan vektörü)
META=[]  # (tarih_hipodrom, at adları, ganyan, eküri birim anahtarı)
FEAT=['hp_degisim','pist_mesafe_galibi','pist_galibi','dinlenme_kisa','dinlenme_uzun','deneyim','antrenor_jokey','sahip','jokey_form30','jokey_hipodrom','hiz_son','hiz_en_iyi3','hiz_yok','son_fark_sn','sinif_degisim','kilo_degisim','ilk_kez_KG','antrenor_form','jokey_yukselme','mesafe_degisim','son_koşu_derece']
gi={g:i for i,g in enumerate(gunler)}
for g in gunler:
    gun=[r for r in R if r['g']==g]
    # 1) özellikler (yalnızca geçmişten)
    if gi[g]>=ISINMA:
        for r in gun:
            h=r['h']
            if not all(x['o']>1 for x in h) or sum(x['pos']==1 for x in h)!=1: continue
            grup={}
            for i,E in enumerate(r['ekuri']):
                for a in E: grup[a]=i
            birim={}
            for x in h: birim.setdefault(grup.get(x['ad'],'t'+x['ad']),[]).append(x)
            tot=sum(1/L[0]['o'] for L in birim.values())
            for L in birim.values():
                for x in L: x['q']=(1/L[0]['o'])/tot/len(L)
            X=[]
            for x in h:
                H=HIS[(r['irk'],x['ad'])]; son=H[-1] if H else None
                figs=[y['fig'] for y in H[-3:] if y['fig'] is not None]
                gs=[y for y in H if y['pos']==1]
                X.append([math.log(x['q']),
                    (x['hp']-son['hp']) if son and son.get('hp') is not None and x['hp'] is not None else 0.0,
                    float(any(y['hip']==r['hip'] and y['pist']==r['pist'] and abs(y['m']-r['m'])<=100 for y in gs)),
                    float(any(y['pist']==r['pist'] for y in gs)),
                    float(son is not None and gi[g]-son['gi']<=10), float(son is not None and gi[g]-son['gi']>60),
                    math.log(1+len(H)),
                    math.log((AJ[(x['ant'],x['jok'])][0]+3)/(AJ[(x['ant'],x['jok'])][1]+3)),
                    math.log((SH[x['sah']][0]+3)/(SH[x['sah']][1]+3)),math.log(jform(x['jok'],gi[g])/jae(x['jok'])),math.log((JH[(x['jok'],r['hip'])][0]+5)/(JH[(x['jok'],r['hip'])][1]+5)/jae(x['jok'])),
                    son['fig'] if son and son['fig'] is not None else np.nan, max(figs) if figs else np.nan, float(not figs),
                    min(son['fark'],10) if son and son['fark'] is not None else np.nan,
                    math.log(r['odul']/son['odul']) if son and son['odul'] and r['odul'] else 0.0,
                    (x['kg']-son['kg']) if son and son['kg'] and x['kg'] else 0.0,
                    float('KG' in x['tg'] and son is not None and 'KG' not in son['tg']),
                    math.log(ant_ae(x['ant'],gi[g])),
                    math.log(jae(x['jok'])/jae(son['jok'])) if son else 0.0,
                    abs(r['m']-son['m'])/1000 if son else 0.0,
                    (10-min(son['pos'],10)) if son else np.nan])
            X=np.array(X,float)
            for j in range(1,X.shape[1]):   # koşu içi standartlaştırma, eksik = 0
                col=X[:,j]; ok=np.isfinite(col)
                if j in (2,3,4,5,13,15,16,17,18,19,20): X[~ok,j]=0; continue
                if ok.sum()>1 and col[ok].std()>0: X[ok,j]=np.clip((col[ok]-col[ok].mean())/col[ok].std(),-2.5,2.5)
                else: X[ok,j]=0
                X[~ok,j]=0
            for j in (1,6,7,8,9,10,15,16,19,20):
                col=X[:,j]; X[:,j]=np.clip((col-col.mean())/(col.std() or 1),-2.5,2.5)
            ORN.append((gi[g],X,np.array([x['pos']==1 for x in h],float)))
            META.append((r['g']+'_'+r['hip'],[x['ad'] for x in h],[x['o'] for x in h],[grup.get(x['ad'],'t'+x['ad']) for x in h]))
    # 2) günü geçmişe ekle
    var=collections.defaultdict(list)
    for r in gun:
        p=par(r); w=[x for x in r['h'] if x['pos']==1 and x['t']]
        if p and w: var[(r['hip'],r['pist'])].append((w[0]['t']-p)/p)
    for r in gun:
        p=par(r); v=statistics.median(var[(r['hip'],r['pist'])]) if var[(r['hip'],r['pist'])] else 0
        w=[x for x in r['h'] if x['pos']==1 and x['t']]; n=len(r['h'])
        for x in r['h']:
            fig=-1000*((x['t']-p)/p-v) if (p and x['t'] and x['pos']<99) else None
            HIS[(r['irk'],x['ad'])].append(dict(gi=gi[g],hip=r['hip'],pist=r['pist'],hp=x['hp'],fig=fig,fark=(x['t']-w[0]['t']) if (w and x['t']) else None,odul=r['odul'],kg=x['kg'],tg=x['tg'],jok=x['jok'],m=r['m'],pos=x['pos']))
            TR[x['ant']].append((gi[g],x['pos']==1,1/n)); JK[x['jok']][0]+=x['pos']==1; JK[x['jok']][1]+=1/n
            AJ[(x['ant'],x['jok'])][0]+=x['pos']==1; AJ[(x['ant'],x['jok'])][1]+=1/n; SH[x['sah']][0]+=x['pos']==1; SH[x['sah']][1]+=1/n
            JR[x['jok']].append((gi[g],x['pos']==1,1/n)); JH[(x['jok'],r['hip'])][0]+=x['pos']==1; JH[(x['jok'],r['hip'])][1]+=1/n
        if w and w[0]['t']: PAR[(r['hip'],r['pist'],r['m'],r['irk'])].append(w[0]['t'])
print('test koşusu:',len(ORN),'| ısınma günü:',ISINMA)
def fit(D,cols,it=250,lr=0.15,lam=2.0):
    w=np.zeros(len(cols))
    for _ in range(it):
        gr=np.zeros(len(cols))
        for _,X,y in D:
            u=X[:,0]+X[:,cols]@w; p=np.exp(u-u.max()); p/=p.sum(); gr+=X[:,cols].T@(y-p)
        w+=lr*(gr-lam*w)/len(D)
    return w
def cv(cols,k=10):
    days=sorted(set(d for d,_,_ in ORN)); fold={d:i%k for i,d in enumerate(days)}; ll=0
    for f in range(k):
        w=fit([o for o in ORN if fold[o[0]]!=f],cols) if cols else None
        for d,X,y in ORN:
            if fold[d]!=f: continue
            u=X[:,0]+(X[:,cols]@w if cols else 0); p=np.exp(u-u.max()); p/=p.sum(); ll+=math.log(p[y==1][0])
    return ll/len(ORN)
base=cv([]); print(f"sadece piyasa: {base:.4f}")
sonuc={}
for j,ad in enumerate(FEAT,1):
    l=cv([j]); sonuc[ad]=l-base; print(f"  + {ad:16} {l:.4f}  fark {1000*(l-base):+.2f} (binde)")
iyi=[j for j,ad in enumerate(FEAT,1) if sonuc[ad]>0.0005]
l=cv(iyi); w=fit(ORN,iyi)
print(f"\nişe yarayanların hepsi birlikte {[FEAT[j-1] for j in iyi]}: {l:.4f}  fark {1000*(l-base):+.2f} (binde)")
print('ağırlıklar:',{FEAT[j-1]:round(float(v),3) for j,v in zip(iyi,w)})
json.dump(dict(ozellikler=[FEAT[j-1] for j in iyi],agirlik=w.tolist(),tek_tek={k:round(1000*v,2) for k,v in sonuc.items()},birlikte=round(1000*(l-base),2),test_kosu=len(ORN)),
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','veri','ozellik_test2.json'),'w'),ensure_ascii=False,indent=1)
