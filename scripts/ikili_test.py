"""Benter yönü: ikili ve sıralı ikili bahislerinde değer var mı? (gerçek TJK sonuçları ve ödemeleri)
Kazanma olasılıkları: piyasa (ganyan, eküri tek birim) + doğrulanmış geçmiş etkenleri, 10 katlı gün CV (ozellik_test2 altyapısı).
Kombinasyon olasılığı: Harville (model p ve piyasa q için ayrı). Kazandıran kombinasyon = gerçek 1. ve 2.; ödeme sonuç satırından (1 TL başına).
Bahis kuralları: (a) her koşuda modelin en olası kombinasyonu, (b) model olasılığı piyasa Harville olasılığının k katı (ve ≥%3).
Not: piyasa çifti olasılığı ganyandan (Harville) türetilir; gerçek ikili havuzunun fiyatı değildir. Kullanım: ikili_test.py sonuc_temiz_dizini"""
import sys,os,re,math,collections,glob
import numpy as np
BURA=os.path.dirname(os.path.abspath(__file__)); SD=sys.argv[1]
src=open(os.path.join(BURA,'ozellik_test2.py'),encoding='utf-8').read().split("print('test koşusu:'")[0]
sys.argv=['x',SD,'45']; G_={'__name__':'__main__','__file__':os.path.join(BURA,'ozellik_test2.py')}; exec(compile(src,'ozellik_test2','exec'),G_)
ORN,META,FEAT=G_['ORN'],G_['META'],G_['FEAT']; ad_=lambda n:G_['ayir'](n)[0]
SEC=['pist_mesafe_galibi','pist_galibi','deneyim','sahip','hiz_son','hiz_en_iyi3']; C=[FEAT.index(k)+1 for k in SEC]
POS={}; ODE={}
for f in glob.glob(SD+'/*.csv'):
    bh=os.path.basename(f)[:-4]; ilk=None
    for l in open(f,encoding='utf-8-sig'):
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]): ilk=None; continue
        if c[0].isdigit() and len(c)>13:
            a=ad_(c[1]); POS[(bh,a)]=int(c[0]) if c[12].strip() else 99
            if ilk is None: ilk=a
        if 'GANYAN(' in l and ilk:
            t=l.replace('SIRALI İKİLİ','SIRALIIKILI'); ik=re.search(r'(?<!SIRALI)İKİLİ\([\d/]+\)\s*:\s*([\d.,]+)',t); si=re.search(r'SIRALIIKILI\([\d/]+\)\s*:\s*([\d.,]+)',t)
            ODE[(bh,ilk)]=dict(ikili=float(ik.group(1).replace('.','').replace(',','.')) if ik else None,sirali=float(si.group(1).replace('.','').replace(',','.')) if si else None)
print('test koşusu:',len(ORN),flush=True)
def fit(D,it=250,lr=0.15,lam=2.0):
    w=np.zeros(len(C))
    for _ in range(it):
        gr=np.zeros(len(C))
        for _,X,y in D:
            u=X[:,0]+X[:,C]@w; p=np.exp(u-u.max()); p/=p.sum(); gr+=X[:,C].T@(y-p)
        w+=lr*(gr-lam*w)/len(D)
    return w
def harville(v,i,j): return v[i]*v[j]/(1-v[i]) if v[i]<1 else 0
days=sorted(set(o[0] for o in ORN)); fold={d:i%10 for i,d in enumerate(days)}
R=collections.defaultdict(lambda:[0,0,0.0,0.0]); KAL=collections.defaultdict(lambda:[0,0.0,0])   # bahis, isabet, ödenen, model beklenen
for f in range(10):
    w=fit([o for o in ORN if fold[o[0]]!=f])
    for (d,X,y),(bh,adlar,oran,birim) in zip(ORN,META):
        if fold[d]!=f: continue
        ps=[POS.get((bh,a),99) for a in adlar]
        if 1 not in ps or 2 not in ps or len(set(birim))!=len(birim): continue   # eküri/ölü yarış koşularını dışla
        bir=[k for k in ODE if k[0]==bh and k[1] in adlar]
        if not bir: continue
        od=ODE[bir[0]]; i1,i2=ps.index(1),ps.index(2)
        u=X[:,0]+X[:,C]@w; p=np.exp(u-u.max()); p/=p.sum(); q=np.exp(X[:,0]); q/=q.sum(); n=len(p)
        for tur,key in (('sıralı ikili','sirali'),('ikili','ikili')):
            if not od[key]: continue
            komb=[]
            for i in range(n):
                for j in range(n):
                    if i==j or (tur=='ikili' and j<i): continue
                    pm=harville(p,i,j)+(harville(p,j,i) if tur=='ikili' else 0); qm=harville(q,i,j)+(harville(q,j,i) if tur=='ikili' else 0)
                    hit=(i==i1 and j==i2) if tur=='sıralı ikili' else ({i,j}=={i1,i2})
                    komb.append((pm,qm,hit))
            b=max(komb,key=lambda x:x[0]); k=(tur,'her koşu: modelin en olası kombinasyonu'); R[k][0]+=1; R[k][1]+=b[2]; R[k][2]+=od[key] if b[2] else 0; R[k][3]+=b[0]
            for pm,qm,hit in komb:
                for esik in (1.3,1.6,2.0):
                    if pm>esik*qm and pm>=0.03:
                        k=(tur,f'model > {esik}× piyasa (≥%3)'); R[k][0]+=1; R[k][1]+=hit; R[k][2]+=od[key] if hit else 0; R[k][3]+=pm
            KAL[tur][0]+=1
    print('kat',f+1,flush=True)
print(f"\n{'bahis':13} {'kural':42} {'bahis':>6} {'isabet':>6} {'isabet %':>8} {'1 TL getirisi':>13} {'model beklenen isabet':>21}")
for (tur,kural),v in sorted(R.items()):
    print(f"{tur:13} {kural:42} {v[0]:6} {v[1]:6} {100*v[1]/max(v[0],1):7.1f}% {100*v[2]/max(v[0],1):12.1f}% {v[3]:21.1f}")
print({k:v[0] for k,v in KAL.items()},'koşu değerlendirildi (eküri ve ölü yarış koşuları hariç)')
