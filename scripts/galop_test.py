"""Galop özellikleri piyasaya göre değer katıyor mu? Kullanım: galop_test.py sonuc_dizini galop_dizini
1) Grup A/E (piyasaya göre). 2) Koşullu logit: log(piyasa olasılığı) + galop özellikleri, her gün dışarıda bırakılarak (leave-one-day-out)."""
import sys,glob,os,re,json,datetime,collections,math
import numpy as np
SD,GD=sys.argv[1:3]
TAGS={'KG','K','DB','SK','SKG','GKR','ÖG','BB','YP','KK','TB','SKK','ÖN','GK','SGKR','KUL','BH','DS'}
def norm(n):
    t=n.replace('(Koşmaz)','').split()
    while len(t)>1 and t[-1] in TAGS: t.pop()
    return ' '.join(t)
races=[]
for gf in sorted(glob.glob(GD+'/*.json')):
    b=os.path.basename(gf)[:-5]; sf=os.path.join(SD,b+'.csv')
    if not os.path.exists(sf): continue
    G=json.load(open(gf,encoding='utf-8')); gun=datetime.date.fromisoformat(b[:10]); cur=None; rs=[]
    for l in open(sf,encoding='utf-8-sig').read().splitlines():
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]): cur=[]; rs.append(cur); continue
        if cur is not None and c[0].isdigit() and len(c)>13:
            try:o=float(c[13].replace(',','.'))
            except:o=0
            cur.append(dict(ad=norm(c[1]),pos=int(c[0]) if c[12].strip() else 99,o=o))
    for h in rs:
        if len(h)<4 or not all(x['o']>1 for x in h): continue
        tot=sum(1/x['o'] for x in h)
        for x in h:
            x['q']=(1/x['o'])/tot; L=[i for i in G.get(x['ad'],{}).get('idmanlar',[]) if datetime.datetime.strptime(i['tarih'],'%d.%m.%Y').date()<gun]
            d30=[i for i in L if (gun-datetime.datetime.strptime(i['tarih'],'%d.%m.%Y').date()).days<=30]
            t4=[i['split'].get('400') for i in d30 if i['split'].get('400')]
            x['b400']=min(t4) if t4 else None; x['n30']=len(d30)
            x['gun']=(gun-datetime.datetime.strptime(L[0]['tarih'],'%d.%m.%Y').date()).days if L else None
            x['efor']=(L[0].get('efor') or '?') if L else 'yok'; x['puan']=float(L[0]['puan']) if L and (L[0].get('puan') or '').isdigit() else None
        v=[x['b400'] for x in h if x['b400']]
        for x in h: x['r400']=1+sum(1 for y in v if y<x['b400']) if x['b400'] else None
        races.append((b[:10],h))
print('koşu:',len(races),'| galop verisi olan at oranı: %',round(100*np.mean([x['b400'] is not None for _,h in races for x in h]),1))
A=collections.defaultdict(lambda:[0,0.0,0])
for _,h in races:
    for x in h:
        w=x['pos']==1
        ks=['400m: en hızlı' if x['r400']==1 else '400m: 2-3.' if x['r400'] in (2,3) else '400m: 4+' if x['r400'] else '400m: son 30 günde yok',
            'son idman: '+('≤3 gün' if x['gun'] is not None and x['gun']<=3 else '4-7 gün' if x['gun'] is not None and x['gun']<=7 else '8-14 gün' if x['gun'] is not None and x['gun']<=14 else '15+ gün/yok'),
            '30 günde idman: '+('0' if x['n30']==0 else '1-2' if x['n30']<=2 else '3+'),'son efor: '+x['efor']]
        for k in ks: a=A[k]; a[0]+=w; a[1]+=x['q']; a[2]+=1
print(f"\n{'grup':28} at  kazanma  piyasa beklentisi  piyasa A/E")
for k in sorted(A):
    a=A[k]
    if a[2]>=30: print(f"{k:28} {a[2]:4} {a[0]:5}  {a[1]:8.1f}  {a[0]/a[1]:6.2f}")
# koşullu logit: piyasa + galop
def feats(h):
    v=np.array([x['b400'] if x['b400'] else np.nan for x in h]); m=np.nanmean(v) if np.isfinite(v).any() else 0; s=np.nanstd(v) if np.isfinite(v).sum()>1 else 1
    F=[]
    for x,b in zip(h,v):
        z=-(b-m)/(s or 1) if np.isfinite(b) else 0.0
        F.append([math.log(x['q']),max(min(z,2.5),-2.5),float(not np.isfinite(b)),float(x['gun'] is not None and x['gun']<=7),min(x['n30'],5)/5,float(x['efor']=='Çalışarak')])
    return np.array(F)
D=[(g,feats(h),np.array([x['pos']==1 for x in h],float)) for g,h in races if any(x['pos']==1 for x in h)]
def fit(data,it=300,lr=0.1):
    w=np.zeros(6); w[0]=1.0
    for _ in range(it):
        gr=np.zeros(6)
        for _,F,y in data:
            u=F@w; p=np.exp(u-u.max()); p/=p.sum(); gr+=F.T@(y-p)
        gr[0]=0; w+=lr*(gr/len(data)-0.5*w*np.r_[0,np.ones(5)]/len(data))
    return w
gunler=sorted(set(g for g,_,_ in D)); ll0=ll1=0
for g in gunler:
    w=fit([d for d in D if d[0]!=g])
    for gg,F,y in D:
        if gg!=g: continue
        for W,ref in ((np.r_[1,0,0,0,0,0],0),(w,1)):
            u=F@W; p=np.exp(u-u.max()); p/=p.sum(); l=math.log(p[y==1][0])
            if ref: ll1+=l
            else: ll0+=l
n=len(D); wall=fit(D)
print(f"\nGünü dışarıda bırakarak test ({len(gunler)} gün, {n} koşu): sadece piyasa log-olabilirlik {ll0/n:.4f} | piyasa+galop {ll1/n:.4f}")
print("Tüm veriyle ağırlıklar: 400m hız %.2f, galop yok %.2f, son 7 günde idman %.2f, idman sayısı %.2f, zorlanarak %.2f"%tuple(wall[1:]))
json.dump(dict(agirlik=wall.tolist(),ozellik=["log_piyasa","hiz400_z","galop_yok","son7gun","idman_sayisi_5","zorlanarak"]),open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","veri","galop_agirlik.json"),"w"))
