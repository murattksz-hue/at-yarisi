"""Sürpriz atlarda değer var mı? Piyasa (ganyan, eküri tek birim) + doğrulanmış geçmiş etkenleri; 10 katlı gün CV tahminleri.
Model olasılığı piyasanın k katı olan atların ganyan aralığına göre gerçek getirisi. Kullanım: surpriz_deger_test.py sonuc_dizini"""
import sys,os,math,collections
import numpy as np
BURA=os.path.dirname(os.path.abspath(__file__)); SD=sys.argv[1]
src=open(os.path.join(BURA,'ozellik_test2.py'),encoding='utf-8').read().split("print('test koşusu:'")[0]
sys.argv=['x',SD,'45']; G_={'__name__':'__main__','__file__':os.path.join(BURA,'ozellik_test2.py')}; exec(compile(src,'ozellik_test2','exec'),G_)
ORN,META,FEAT=G_['ORN'],G_['META'],G_['FEAT']
SEC=['pist_mesafe_galibi','pist_galibi','deneyim','sahip','hiz_son','hiz_en_iyi3']; C=[FEAT.index(k)+1 for k in SEC]
print('test koşusu:',len(ORN),flush=True)
def fit(D,it=250,lr=0.15,lam=2.0):
    w=np.zeros(len(C))
    for _ in range(it):
        gr=np.zeros(len(C))
        for _,X,y in D:
            u=X[:,0]+X[:,C]@w; p=np.exp(u-u.max()); p/=p.sum(); gr+=X[:,C].T@(y-p)
        w+=lr*(gr-lam*w)/len(D)
    return w
days=sorted(set(o[0] for o in ORN)); fold={d:i%10 for i,d in enumerate(days)}; B=[]
for f in range(10):
    w=fit([o for o in ORN if fold[o[0]]!=f])
    for (d,X,y),(bh,adlar,oran,birim) in zip(ORN,META):
        if fold[d]!=f: continue
        u=X[:,0]+X[:,C]@w; p=np.exp(u-u.max()); p/=p.sum(); q=np.exp(X[:,0]); U=collections.defaultdict(lambda:[0.0,0.0,0.0,0])
        for j,k in enumerate(birim): U[k][0]+=p[j]; U[k][1]+=q[j]; U[k][2]=oran[j]; U[k][3]|=int(y[j])
        B+= [tuple(v) for v in U.values()]
    print('kat',f+1,'tamam',flush=True)
kv=lambda o:'1-5' if o<5 else '5-10' if o<10 else '10-20' if o<20 else '20-50' if o<50 else '50+'
print(f"\nTahmin edilen birim: {len(B)}")
print(f"{'ganyan':7} {'koşul':16} {'bahis':>6} {'kazanan':>7} {'1 TL getirisi':>14} {'beklenen kazanan (model)':>25}")
for band in ['1-5','5-10','10-20','20-50','50+']:
    for ad,kosul in (('hepsi',lambda p,q:True),('p>1,2×piyasa',lambda p,q:p>1.2*q),('p>1,5×piyasa',lambda p,q:p>1.5*q),('p>2×piyasa',lambda p,q:p>2*q)):
        S=[b for b in B if kv(b[2])==band and kosul(b[0],b[1])]
        if len(S)<20: continue
        don=sum(b[2] for b in S if b[3]); print(f"{band:7} {ad:16} {len(S):6} {sum(b[3] for b in S):7} {100*don/len(S):13.1f}% {sum(b[0] for b in S):25.1f}")
