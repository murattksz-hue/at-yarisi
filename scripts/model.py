"""Irk x zemin x mesafe grubuna özel koşullu logit (koşu içi softmax) modeli.
Kullanım: model.py sonuc_dizini program_dizini test_baslangic(YYYY-AA-GG) cikti_agirlik.json
- Aygır ve kulvar istatistikleri test başlangıcından ÖNCEKİ sonuçlardan, at kendi koşusunu dışarıda bırakarak (leave-one-out) hesaplanır.
- Önce tüm koşular için genel ağırlıklar, sonra her grup için genel ağırlığa çekilen (L2) özel ağırlıklar öğrenilir."""
import sys,glob,os,re,json,collections,math
import numpy as np
SD,PD,T,OUT=sys.argv[1:5]; LAM=float(sys.argv[5]) if len(sys.argv)>5 else 300.0
def bant(m): return 'kisa' if m<=1400 else ('orta' if m<=1900 else 'uzun')
def kova(s): return '1-3' if s<=3 else '4-6' if s<=6 else '7-9' if s<=9 else '10+'
TAGS={'KG','K','DB','SK','SKG','GKR','ÖG','BB','YP','KK','TB','SKK','ÖN','GK','SGKR','KUL','BH','DS'}
def norm(n):
    t=n.replace('(Koşmaz)','').split()
    while len(t)>1 and t[-1] in TAGS: t.pop()
    return ' '.join(t)
def oku(f,sonuc):
    out=[];cur=None
    for l in open(f,encoding='utf-8-sig').read().splitlines():
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]):
            m=re.search(r'(\d{3,4})m',l)
            cur=dict(no=c[0].split('.')[0],irk='Arap' if 'Arap' in l else 'İngiliz',pist=next((p for p in ('Kum','Çim','Sentetik') if p in l),'?'),bant=bant(int(m.group(1))) if m else '?',h=[]);out.append(cur);continue
        if not(cur and c[0].isdigit()): continue
        if sonuc and len(c)>13:
            try:o=float(c[13].replace(',','.'))
            except:o=0
            st=re.match(r'(\d+)',c[9])
            cur['h'].append(dict(ad=norm(c[1]),pos=int(c[0]) if c[12].strip() else 99,o=o,baba=c[3].strip(),st=int(st.group(1)) if st else 0))
        elif not sonuc and len(c)>14 and 'Koşmaz' not in c[1]:
            ag=re.match(r'%([\d.]+)',c[10]); y=re.match(r'(\d+)y',c[2]); kg=re.match(r'([\d,]+)',c[5]); st=re.match(r'(\d+)',c[9])
            cur['h'].append(dict(ad=norm(c[1]),baba=c[3].strip(),hp=int(c[11]) if c[11].isdigit() else 0,son6=c[12],kgs=int(c[13]) if c[13].isdigit() else 0,
                s20=int(c[14]) if c[14].isdigit() else 0,agf=float(ag.group(1)) if ag else 0.5,yas=int(y.group(1)) if y else 4,
                kg=float(kg.group(1).replace(',','.')) if kg else 57,ap=' AP' in c[6],st=int(st.group(1)) if st else 0))
    return out
# ---- 1) sonuçlar: aygır ve kulvar istatistikleri (T öncesi)
files=sorted(glob.glob(SD+'/*.csv')); SON={}
AY=collections.defaultdict(lambda:[0,0.0]); KU=collections.defaultdict(lambda:[0,0.0])
for f in files:
    b=os.path.basename(f); g=b[:10]; hip=b[11:-4]; rs=oku(f,True); SON[b]=rs
    if g>=T: continue
    for r in rs:
        n=len(r['h'])
        if n<4: continue
        for x in r['h']:
            w=x['pos']==1
            for k in (f"{r['irk']}|{x['baba']}|{r['pist']}_{r['bant']}",f"{r['irk']}|{x['baba']}|genel"):
                AY[k][0]+=w; AY[k][1]+=1/n
            k=f"{hip}|{r['pist']}|{r['bant']}|{kova(x['st'])}"; KU[k][0]+=w; KU[k][1]+=1/n
def ae(D,k,w,e,pr=4,loo=True):
    s=D.get(k,[0,0.0]); W,E=(s[0]-w,s[1]-e) if loo else s
    return (max(W,0)+pr)/(max(E,0)+pr)
PC={'K':'Kum','Ç':'Çim','S':'Sentetik'}
FEAT=['hp','s20','form','pist_form','baba_kani','kulvar','agf','uzun_ara','apranti','yas','kilo']
def ozellik(r,hip,loo):
    n=len(r['h']); X=[]
    for x in r['h']:
        fm=re.findall(r'([KÇS])(\d)',x['son6']); pts=[(10-int(q)) if q!='0' else 0 for _,q in fm]
        pp=[(10-int(q)) if q!='0' else 0 for y,q in fm if PC[y]==r['pist']]
        form=sum(pts)/len(pts) if pts else 3; pf=sum(pp)/len(pp) if pp else form*0.8
        w=(x.get('pos')==1) if loo else 0; e=(1/n) if loo else 0
        ba=ae(AY,f"{r['irk']}|{x['baba']}|{r['pist']}_{r['bant']}",w,e,loo=loo)
        ku=ae(KU,f"{hip}|{r['pist']}|{r['bant']}|{kova(x['st'])}",w,e,pr=10,loo=loo)
        X.append([x['hp'],x['s20'],form,pf,math.log(ba),math.log(ku),math.log(max(x['agf'],0.3)),float(x['kgs']>60),float(x['ap']),x['yas'],x['kg']])
    X=np.array(X,float); sd=X.std(0); sd[sd==0]=1
    Z=(X-X.mean(0))/sd
    Z[:,6]=X[:,6]-X[:,6].mean()   # AGF: ham log oran (ölçeği anlamlı)
    return Z
# ---- 2) program + sonuç eşle
egit,test=[],[]
for b,rs in SON.items():
    pf=os.path.join(PD,b)
    if not os.path.exists(pf): continue
    g=b[:10]; hip=b[11:-4]; P={r['no']:r for r in oku(pf,False)}
    for r in rs:
        p=P.get(r['no'])
        if not p or len(p['h'])<4: continue
        sm={x['ad']:x for x in r['h']}
        if not any(x['pos']==1 for x in r['h']): continue
        for x in p['h']:
            s=sm.get(x['ad']); x['pos']=s['pos'] if s else 99; x['o']=s['o'] if s else 0
        if sum(x['pos']==1 for x in p['h'])!=1: continue
        loo=g<T; Z=ozellik(p,hip,loo); y=np.array([x['pos']==1 for x in p['h']],float)
        o=np.array([x['o'] for x in p['h']]); seg=f"{p['irk']}|{p['pist']}|{p['bant']}"
        (test if g>=T else egit).append((seg,Z,y,o))
print('eğitim koşusu:',len(egit),'test koşusu:',len(test))
# ---- 3) koşullu logit
def fit(data,w0,lam,it=400,lr=0.05):
    w=w0.copy()
    for _ in range(it):
        gr=np.zeros_like(w)
        for _,Z,y,_ in data:
            u=Z@w; p=np.exp(u-u.max()); p/=p.sum(); gr+=Z.T@(y-p)
        gr=gr/len(data)-lam*(w-w0)/len(data)
        w+=lr*gr
    return w
def ll(data,W):
    return np.mean([np.log((lambda u:(np.exp(u-u.max())/np.exp(u-u.max()).sum()))(Z@W(seg))[y==1][0]) for seg,Z,y,_ in data])
d=len(FEAT); wg=fit(egit,np.zeros(d),lam=1.0)
SEG={}
for seg in sorted(set(s for s,*_ in egit)):
    ds=[x for x in egit if x[0]==seg]
    SEG[seg]=fit(ds,wg,lam=LAM) if len(ds)>=25 else wg
Wseg=lambda s:SEG.get(s,wg); Wglob=lambda s:wg
wa=np.zeros(d); wa[6]=1.0; Wagf=lambda s:wa
def degerlendir(data,W,ad):
    t1=t3=0; bet=ret=0.0; vb=vr=0.0
    for seg,Z,y,o in data:
        u=Z@W(seg); p=np.exp(u-u.max()); p/=p.sum(); srt=np.argsort(-p); kaz=int(np.argmax(y))
        t1+=srt[0]==kaz; t3+=kaz in srt[:3]; bet+=1; ret+=o[srt[0]] if srt[0]==kaz else 0
        q=np.where(o>1,1/np.where(o>1,o,1),0); q=q/q.sum() if q.sum() else q
        for i in range(len(p)):
            if o[i]>1 and o[i]<=30 and p[i]>1.3*q[i]: vb+=1; vr+=o[i] if i==kaz else 0
    n=len(data)
    print(f"{ad:30} log-olabilirlik {ll(data,W):.3f} | 1. seçim %{100*t1/n:.1f} | ilk 3 %{100*t3/n:.1f} | 1. seçim ganyan getirisi %{100*ret/bet:.0f} | değer bahsi: {int(vb)} bahis, getiri %{100*vr/vb if vb else 0:.0f}")
print('\nTEST (görülmemiş günler):')
degerlendir(test,Wagf,'Sadece AGF (halk)')
degerlendir(test,Wglob,'Genel model')
degerlendir(test,Wseg,'Irk/zemin/mesafe özel model')
print('\nAğırlıklar (+ = kazanma şansını artırır):')
print(f"{'grup':24}"+''.join(f"{f[:9]:>10}" for f in FEAT))
print(f"{'GENEL':24}"+''.join(f"{v:10.2f}" for v in wg))
for s,w in SEG.items(): print(f"{s:24}"+''.join(f"{v:10.2f}" for v in w))
# canlı kullanım için tüm sonuçlardan aygır ve kulvar tabloları
AY2=collections.defaultdict(lambda:[0,0.0]); KU2=collections.defaultdict(lambda:[0,0.0])
for b,rs in SON.items():
    hip=b[11:-4]
    for r in rs:
        n=len(r['h'])
        if n<4: continue
        for x in r['h']:
            w=x['pos']==1
            AY2[f"{r['irk']}|{x['baba']}|{r['pist']}_{r['bant']}"][0]+=w; AY2[f"{r['irk']}|{x['baba']}|{r['pist']}_{r['bant']}"][1]+=1/n
            AY2[f"{r['irk']}|{x['baba']}|genel"][0]+=w; AY2[f"{r['irk']}|{x['baba']}|genel"][1]+=1/n
            k=f"{hip}|{r['pist']}|{r['bant']}|{kova(x['st'])}"; KU2[k][0]+=w; KU2[k][1]+=1/n
json.dump(dict(ozellikler=FEAT,genel=wg.tolist(),grup={k:v.tolist() for k,v in SEG.items()},test_baslangic=T,
    aygir={k:[v[0],round(v[1],3)] for k,v in AY2.items()},kulvar={k:[v[0],round(v[1],3)] for k,v in KU2.items()}),open(OUT,'w'),ensure_ascii=False)
