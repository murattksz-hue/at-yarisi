"""Irk x zemin x mesafe grubuna özel koşullu logit (koşu içi softmax) modeli.
Kullanım: model.py sonuc_dizini program_dizini test_baslangic(YYYY-AA-GG) cikti_agirlik.json
- Aygır ve kulvar istatistikleri test başlangıcından ÖNCEKİ sonuçlardan, at kendi koşusunu dışarıda bırakarak (leave-one-out) hesaplanır.
- Önce tüm koşular için genel ağırlıklar, sonra her grup için genel ağırlığa çekilen (L2) özel ağırlıklar öğrenilir."""
import sys,glob,os,re,json,collections,math
import numpy as np
GO=json.load(open(os.environ['GECMIS'],encoding='utf-8'))
HV=json.load(open(os.environ.get('HAVA','/home/user/at-yarisi/veri/hava_gecmis.json'),encoding='utf-8'))
SD,PD,T,OUT=sys.argv[1:5]; LAM=float(sys.argv[5]) if len(sys.argv)>5 else 1000.0; SEGMOD=sys.argv[6] if len(sys.argv)>6 else 'irk'; AGFSIZ=len(sys.argv)>7 and sys.argv[7]=='agfsiz'
def aile(h):
    s=h.upper()
    for pat,ad in [(r'G ?[123]\b','Grup'),(r'KV','KV'),(r'SATI','Satış'),(r'MAIDEN|MAİDEN|ŞARTLI ?-?19','Maiden'),(r'ŞARTLI','Şartlı'),(r'HANDİKAP|HANDIKAP','Handikap')]:
        if re.search(pat,s): return ad
    return 'Diğer'
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
            cur=dict(disi_kosu='Dişi' in c[1],aile=aile(c[1]),no=c[0].split('.')[0],irk='Arap' if 'Arap' in l else 'İngiliz',pist=next((p for p in ('Kum','Çim','Sentetik') if p in l),'?'),bant=bant(int(m.group(1))) if m else '?',h=[]);out.append(cur);continue
        if not(cur and c[0].isdigit()): continue
        if sonuc and len(c)>13:
            try:o=float(c[13].replace(',','.'))
            except Exception:o=0
            st=re.match(r'(\d+)',c[9])
            cur['h'].append(dict(ad=norm(c[1]),pos=int(c[0]) if c[12].strip() else 99,o=o,baba=c[3].strip(),st=int(st.group(1)) if st else 0,jok=c[6].replace(' AP','').strip()))
        elif not sonuc and len(c)>14 and 'Koşmaz' not in c[1]:
            ag=re.match(r'%([\d.]+)',c[10]); y=re.match(r'(\d+)y',c[2]); kg=re.match(r'([\d,]+)',c[5]); st=re.match(r'(\d+)',c[9])
            cur['h'].append(dict(ad=norm(c[1]),baba=c[3].strip(),hp=int(c[11]) if c[11].isdigit() else 0,son6=c[12],kgs=int(c[13]) if c[13].isdigit() else 0,
                s20=int(c[14]) if c[14].isdigit() else 0,agf=float(ag.group(1)) if ag else 0.5,yas=int(y.group(1)) if y else 4,
                kg=float(kg.group(1).replace(',','.')) if kg else 57,ap=' AP' in c[6],st=int(st.group(1)) if st else 0,jok=c[6].replace(' AP','').strip(),dis=(c[2].split() or ['?'])[-1] in ('d','k'),cins=(c[2].split() or ['?'])[-1]))
    return out
# ---- 1) sonuçlar: aygır ve kulvar istatistikleri (T öncesi)
files=sorted(glob.glob(SD+'/*.csv')); SON={}
AYW=collections.defaultdict(lambda:[0,0.0]); AY=collections.defaultdict(lambda:[0,0.0]); KU=collections.defaultdict(lambda:[0,0.0]); JK=collections.defaultdict(lambda:[0,0.0])
for f in files:
    b=os.path.basename(f); g=b[:10]; hip=b[11:-4]; rs=oku(f,True); SON[b]=rs
def islak(b): return (HV.get(b[:-4],{}).get('islaklik') or 0)>=5
def biriktir(b,rs):
    hip=b[11:-4]; wt='ıslak' if islak(b) else 'kuru'
    for r in rs:
        n=len(r['h'])
        if n<4: continue
        for x in r['h']:
            w=x['pos']==1
            for k in (f"{r['irk']}|{x['baba']}|{r['pist']}_{r['bant']}",f"{r['irk']}|{x['baba']}|genel"):
                AY[k][0]+=w; AY[k][1]+=1/n
            k=f"{hip}|{r['pist']}|{r['bant']}|{kova(x['st'])}"; KU[k][0]+=w; KU[k][1]+=1/n
            JK[f"{r['irk']}|{x['jok']}"][0]+=w; JK[f"{r['irk']}|{x['jok']}"][1]+=1/n
            AYW[f"{r['irk']}|{x['baba']}|{wt}"][0]+=w; AYW[f"{r['irk']}|{x['baba']}|{wt}"][1]+=1/n
def ae(D,k,w,e,pr=4,loo=True):
    s=D.get(k,[0,0.0]); W,E=(s[0]-w,s[1]-e) if loo else s
    return (max(W,0)+pr)/(max(E,0)+pr)
PC={'K':'Kum','Ç':'Çim','S':'Sentetik'}
FEAT=['hp','s20','form','pist_form','baba_kani','kulvar','agf','uzun_ara','apranti','yas','kilo','jokey','islak_hp','islak_agf','baba_islak',
      'hiz_en_iyi3','hiz_son','pist_mesafe_galibi','pist_galibi','deneyim','sahip','galop_400','galop_yok','galop_son7','galop_sayi30','galop_zorlanarak','disi_karma','genc_erkek','igdis']
def ozellik(r,hip,loo,wet=False,b=None):
    n=len(r['h']); X=[]
    for x in r['h']:
        fm=re.findall(r'([KÇS])(\d)',x['son6']); pts=[(10-int(q)) if q!='0' else 0 for _,q in fm]
        pp=[(10-int(q)) if q!='0' else 0 for y,q in fm if PC[y]==r['pist']]
        form=sum(pts)/len(pts) if pts else 3; pf=sum(pp)/len(pp) if pp else form*0.8
        w=(x.get('pos')==1) if loo else 0; e=(1/n) if loo else 0
        ba=ae(AY,f"{r['irk']}|{x['baba']}|{r['pist']}_{r['bant']}",w,e,loo=loo)
        ku=ae(KU,f"{hip}|{r['pist']}|{r['bant']}|{kova(x['st'])}",w,e,pr=10,loo=loo)
        jk=ae(JK,f"{r['irk']}|{x['jok']}",w,e,pr=10,loo=loo)
        bw=math.log(ae(AYW,f"{r['irk']}|{x['baba']}|ıslak",0,0,pr=3,loo=False)/ae(AYW,f"{r['irk']}|{x['baba']}|kuru",0,0,pr=3,loo=False)) if wet else 0.0
        X.append([x['hp'],x['s20'],form,pf,math.log(ba),math.log(ku),math.log(max(x['agf'],0.3)),float(x['kgs']>60),float(x['ap']),x['yas'],x['kg'],math.log(jk),0,0,bw])
    X=np.array(X,float); sd=X.std(0); sd[sd==0]=1
    Z=np.clip((X-X.mean(0))/sd,-2.5,2.5)   # küçük alanlarda uç değer şişmesini sınırla
    Z[:,6]=X[:,6]-X[:,6].mean()   # AGF: ham log oran (ölçeği anlamlı)
    if AGFSIZ: Z[:,6]=0            # AGF'siz model (bahis açılmadan önce)
    if wet: Z[:,12]=Z[:,0]; Z[:,13]=Z[:,6]
    else: Z[:,12]=0; Z[:,13]=0
    Z[:,14]=X[:,14]-X[:,14].mean()
    E=np.array([[np.nan if v is None else v for v in GO.get(f"{b[:-4] if b and b.endswith('.csv') else b}|{r['no']}|{x['ad']}",[None,None,0,0,0,0,None,0,0,0,0,0])[:11]] for x in r['h']],float)
    E[:,6]=-E[:,6]   # 400 m: düşük süre = iyi
    for j in (0,1,4,5,6):
        col=E[:,j]; ok=np.isfinite(col); z=np.zeros(len(col))
        if ok.sum()>1 and col[ok].std()>0: z[ok]=np.clip((col[ok]-col[ok].mean())/col[ok].std(),-2.5,2.5)
        E[:,j]=z
    E=np.nan_to_num(E)
    DK=np.array([[float(x.get('dis',False) and not r.get('disi_kosu',False)),float(x.get('cins')=='e'),float(x.get('cins')=='g')] for x in r['h']])
    return np.hstack([Z,E,DK])
# ---- 2) program + sonuç eşle
egit,test=[],[]
onceki=None
for b in sorted(SON):   # kronolojik: her günün özellikleri yalnızca önceki günlerden
    rs=SON[b]
    if onceki and onceki[:10]!=b[:10]:
        for bb in bekleyen: biriktir(bb,SON[bb])
        bekleyen=[]
    if onceki is None: bekleyen=[]
    onceki=b; bekleyen.append(b)
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
        Z=ozellik(p,hip,False,islak(b),b); y=np.array([x['pos']==1 for x in p['h']],float)
        o=np.array([x['o'] for x in p['h']]); seg=f"{p['irk']}|{p['pist']}|{p['bant']}" if SEGMOD=='irk' else f"{p['irk']}|{p['aile']}"
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
AY2=collections.defaultdict(lambda:[0,0.0]); KU2=collections.defaultdict(lambda:[0,0.0]); JK2=collections.defaultdict(lambda:[0,0.0])
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
            JK2[f"{r['irk']}|{x['jok']}"][0]+=w; JK2[f"{r['irk']}|{x['jok']}"][1]+=1/n
AYW2=collections.defaultdict(lambda:[0,0.0])
for b,rs in SON.items():
    wt='ıslak' if islak(b) else 'kuru'
    for r in rs:
        n=len(r['h'])
        if n<4: continue
        for x in r['h']: AYW2[f"{r['irk']}|{x['baba']}|{wt}"][0]+=x['pos']==1; AYW2[f"{r['irk']}|{x['baba']}|{wt}"][1]+=1/n
json.dump(dict(aygir_islak={k:[v[0],round(v[1],3)] for k,v in AYW2.items()},agfsiz=AGFSIZ,ozellikler=FEAT,genel=wg.tolist(),grup={k:v.tolist() for k,v in SEG.items()},test_baslangic=T,
    aygir={k:[v[0],round(v[1],3)] for k,v in AY2.items()},kulvar={k:[v[0],round(v[1],3)] for k,v in KU2.items()},jokey={k:[v[0],round(v[1],3)] for k,v in JK2.items()},segmod=SEGMOD),open(OUT,'w'),ensure_ascii=False)
