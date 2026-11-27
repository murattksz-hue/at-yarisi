"""Koşu riski v2: kazananın piyasa ilk 3 (ya da ilk 4) dışından gelme olasılığı. Kullanım: kosu_riski_v2.py [YYYY-AA-GG] -> veri/kosu_riski_v2.md
Neden: 3 atlık liste kazananı kaçırır mı sorusu için en iyi ayırıcı. Test (2025-07 sonrası): ilk 3 dışı hedefinde AUC 0,648 (yalnız piyasa riski 0,597); gözden kaçan kazanan (ganyan>=10) hedefinde fark yok (0,655 / 0,648).
Özellikler: piyasada p<%10 payı, at sayısı, ilk üç favori payı, entropi, HP/kilo yayılımı, ırk, mesafe, zemin, hipodrom, çeşit, saat. Eğitim: at_gecmisi 2022+ (kapanış ganyanı); canlı: son AGF görüntüsü (yaklaşık).
Sınıf: eğitim verisi tersilleri (düşük/orta/yüksek). Kural (CLAUDE.md): ölçüler çelişirse daha riskli olanı al. Yalnızca okur; yazar veri/kosu_riski_v2.md."""
import gzip,glob,csv,collections,io,sys,os,re,datetime
import numpy as np
import lightgbm as lgb
D=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
sys.path.insert(0,D+'scripts'); import kosu_tipi as K
GUN=sys.argv[1] if len(sys.argv)>1 else datetime.date.today().isoformat()
def fl(x):
    try: return float(str(x).replace(',','.'))
    except Exception: return None
HIPS=['Adana','Ankara','Antalya','Bursa','Diyarbakır','Elazığ','İstanbul','İzmir','Kocaeli','Şanlıurfa']
AILE=['Şartlı','Handikap','KV','Grup','Satış','Açık','Listed','Maiden (kazanmamışlar)','Diğer']
PIST=['Kum','Çim','Sentetik']
def feat(pp,hp,kl,irk,mesafe,wd,pist,hip,aile,saat):
    pp=np.asarray(pp);sp=np.sort(pp)[::-1];hpv=[x for x in hp if x];klv=[x for x in kl if x]
    return [float(pp[pp<.10].sum()),len(pp),float(sp[0]),float(sp[1]),float(sp[2]),-float(np.sum(pp*np.log(pp))),float(sp[0]-sp[1]),
            float(np.std(hpv)) if len(hpv)>2 else -1,float(max(hpv)-min(hpv)) if len(hpv)>2 else -1,
            float(np.std(klv)) if len(klv)>2 else -1,float(max(klv)-min(klv)) if len(klv)>2 else -1,
            irk,float(mesafe or 0),wd,PIST.index(pist) if pist in PIST else 3,HIPS.index(hip) if hip in HIPS else -1,AILE.index(aile) if aile in AILE else -1,saat]
X=[];Y3=[];Y4=[]
for p in sorted(glob.glob(D+'veri/at_gecmisi/202[2-6]/*.csv.gz')):
    R=collections.defaultdict(list)
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(p),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
    for k,rs in R.items():
        g=[fl(r['ganyan']) for r in rs]
        if len(rs)<5 or any(x is None or x<=1 for x in g) or sum(r['sonuc']=='1' for r in rs)!=1: continue
        s=sum(1/x for x in g);pp=np.array([1/x/s for x in g]);order=np.argsort(-pp)
        wi=[i for i,r in enumerate(rs) if r['sonuc']=='1'][0];rw=int(np.where(order==wi)[0][0])+1
        t=K.tur(rs[0]['tur'] or '');saat=rs[0]['saat'][:2]
        X.append(feat(pp,[fl(r['hp']) for r in rs],[fl(r['kilo']) for r in rs],int((rs[0]['grup'] or '').strip().endswith('A')),fl(rs[0]['mesafe']),datetime.date.fromisoformat(k[0]).weekday(),(rs[0]['pist'] or '').strip(),rs[0]['hip'],K.aile(t),float(saat) if saat.isdigit() else -1))
        Y3.append(int(rw>3));Y4.append(int(rw>4))
X=np.array(X)
mk=lambda y:lgb.LGBMClassifier(n_estimators=300,learning_rate=0.03,num_leaves=15,min_child_samples=100,subsample=0.8,colsample_bytree=0.8,verbose=-1).fit(X,y)
M3=mk(Y3);M4=mk(Y4);P3=M3.predict_proba(X)[:,1];P4=M4.predict_proba(X)[:,1]
Q3=np.quantile(P3,[1/3,2/3]);Q4=np.quantile(P4,[1/3,2/3])
sinif=lambda p,q:'düşük' if p<=q[0] else 'orta' if p<=q[1] else 'yüksek'
out=[]
for hip in HIPS:
    fs=sorted(glob.glob(D+'veri/agf_kayit/'+GUN+f'/{hip}_[0-9][0-9][0-9][0-9]UTC.csv'))
    if not fs: continue
    t=open(fs[-1],encoding='utf-8-sig').read().splitlines();race=None;R={};H={}
    for l in t:
        m=re.match(r'(\d+)\. Kosu\s*:\s*([\d.]+);(.*)',l)
        if m: race=int(m.group(1));R[race]=[];H[race]=(m.group(2),m.group(3));continue
        c=l.split(';')
        if race and c[0].isdigit() and len(c)>11:
            a=re.search(r'%?([\d.]+)\(',c[10]);kg=re.match(r'[\d,.]+',c[5])
            R[race].append((float(a.group(1)) if a else 0,fl(c[11]),fl(kg.group(0)) if kg else None))
    for r,v in R.items():
        s=sum(x[0] for x in v)
        if s<=0: continue
        pp=[x[0]/s for x in v];head=H[r][1];sn=K.sinif(head.replace(';',' '))
        f=feat(pp,[x[1] for x in v],[x[2] for x in v],int('Arap' in head),sn['mesafe'],datetime.date.fromisoformat(GUN).weekday(),sn['pist'],hip,sn['aile'],float(H[r][0][:2]))
        p3=M3.predict_proba([f])[0][1];p4=M4.predict_proba([f])[0][1]
        out.append((p3,p4,hip,r,H[r][0],len(v),sn['aile'],'Arap' if 'Arap' in head else 'İng',sn['mesafe']))
L=[f'# Koşu riski v2 — {GUN}','',f'Olasılıklar: kazananın piyasa ilk 3 (3 atlık liste kaçırır) / ilk 4 dışından gelmesi (eğitim tabanı %{100*np.mean(Y3):.0f} / %{100*np.mean(Y4):.0f}). Sınıf eşikleri eğitim tersilleri: ilk 3 dışı ≤%{100*Q3[0]:.0f} düşük, ≤%{100*Q3[1]:.0f} orta, üstü yüksek. Canlı girdi son AGF görüntüsü, yaklaşık.','','| Sınıf (ilk 3) | Kaçırma ilk 3 | Kaçırma ilk 4 | Hip | Koşu | Saat | At | Çeşit | Irk | Mesafe |','|---|---|---|---|---|---|---|---|---|---|']
for o in sorted(out):
    L.append(f'| {sinif(o[0],Q3)} | %{100*o[0]:.0f} | %{100*o[1]:.0f} | {o[2]} | {o[3]} | {o[4]} | {o[5]} | {o[6]} | {o[7]} | {o[8]} |')
open(D+'veri/kosu_riski_v2.md','w',encoding='utf-8').write('\n'.join(L)+'\n')
print('\n'.join(L))
