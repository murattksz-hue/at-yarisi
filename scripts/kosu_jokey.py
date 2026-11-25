"""Koşu türü, cinsiyet ve jokey analizi. Kullanım: kosu_jokey.py sonuc_dizini cikti.json
Piyasa A/E = gerçek birincilik / ganyan oranından türeyen beklenti (>1: halk hafife alıyor)."""
import sys,glob,os,re,json,collections,statistics
def tip(h):
    s=h.upper()
    for pat,ad in [(r'G ?1\b','G1'),(r'G ?2\b','G2'),(r'G ?3\b','G3'),(r'KV-? ?(\d+)','KV'),(r'SATI','Satış'),(r'MAIDEN|MAİDEN','Maiden'),
                   (r'ŞARTLI ?-?(\d+)','Şartlı'),(r'HANDİKAP ?(\d+)|HANDIKAP ?(\d+)','Handikap'),(r'AÇIK|ACIK','Açık')]:
        m=re.search(pat,s)
        if m:
            n=next((g for g in m.groups() if g),'') if m.groups() else ''
            return ad+(' '+n if n and ad in('KV','Şartlı','Handikap') else '')
    return 'Diğer'
CINS={'e':'erkek','d':'dişi','a':'aygır','k':'kısrak','g':'iğdiş'}
T=collections.defaultdict(lambda:dict(k=0,fav=0,hpl=0,hp=[],alan=0,ae=collections.defaultdict(lambda:[0,0.0])))
J=collections.defaultdict(lambda:collections.defaultdict(lambda:[0,0,0.0,0.0]))  # binis, kazanma, 1/n, piyasa
for f in sorted(glob.glob(sys.argv[1]+'/*.csv')):
    hip=os.path.basename(f)[11:-4]; cur=None; rs=[]
    for l in open(f,encoding='utf-8-sig').read().splitlines():
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]):
            cur=dict(tip=tip(c[1]),irk='Arap' if 'Arap' in l else 'İngiliz',dis='Dişi' in c[1],h=[]); rs.append(cur); continue
        if cur and c[0].isdigit() and len(c)>13:
            try:o=float(c[13].replace(',','.'))
            except Exception:o=0
            y=c[2].split(); kg=re.match(r'([\d,]+)',c[5])
            cur['h'].append(dict(pos=int(c[0]) if c[12].strip() else 99,o=o,hp=int(c[11]) if c[11].isdigit() else 0,cins=CINS.get(y[-1],'?') if y else '?',
                yas=y[0] if y else '?',jok=c[6].replace(' AP','').strip(),ap=' AP' in c[6],kg=float(kg.group(1).replace(',','.')) if kg else 0))
    for r in rs:
        h=r['h']; n=len(h)
        if n<4: continue
        key=f"{r['irk']}|{r['tip']}"; t=T[key]; t['k']+=1; t['alan']+=n; t['hp']+= [x['hp'] for x in h if x['hp']]
        oo=[x for x in h if x['o']>1]; tot=sum(1/x['o'] for x in oo) or 1
        if oo and min(oo,key=lambda x:x['o'])['pos']==1: t['fav']+=1
        rk=lambda x,k:1+sum(y[k]>x[k] for y in h)   # eşitlikte aynı sıra (kazananı kayırmaz)
        mh=max(x['hp'] for x in h); lid=[x for x in h if x['hp']==mh and mh>0]
        if lid: t['hpl']+=sum(x['pos']==1 for x in lid)/len(lid)
        for x in h:
            w=x['pos']==1; mp=(1/x['o'])/tot if x['o']>1 else 0
            r1,r2=rk(x,'hp'),rk(x,'kg')
            keys=['cins '+x['cins'],'kilo sırası '+(str(r2) if r2<4 else '4+')]+(['HP sırası '+(str(r1) if r1<4 else '4+')] if mh>0 else [])
            if not r['dis']: keys.append('karma koşuda '+('dişi' if x['cins'] in('dişi','kısrak') else 'erkek'))
            for k in keys: a=t['ae'][k]; a[0]+=w; a[1]+=mp
            for jk in ('genel',r['irk'],hip):
                j=J[x['jok']][jk]; j[0]+=1; j[1]+=w; j[2]+=1/n; j[3]+=mp
out={'kosu_turu':{},'jokey':{}}
print(f"{'ırk|koşu türü':22} koşu  alan  HP aralığı(%10-%90) fav% HPlider% | HP2 HP3 | dişi(karma) | kilo1")
for k in sorted(T,key=lambda k:-T[k]['k']):
    t=T[k]
    if t['k']<15: continue
    hp=sorted(t['hp']); q=lambda p:hp[int(p*(len(hp)-1))] if hp else 0
    ae={a:round(v[0]/v[1],2) for a,v in t['ae'].items() if v[1]>2}
    out['kosu_turu'][k]=dict(kosu=t['k'],ort_alan=round(t['alan']/t['k'],1),hp_p10=q(.1),hp_medyan=q(.5),hp_p90=q(.9),favori=round(100*t['fav']/t['k'],1),hp_lideri=round(100*t['hpl']/t['k'],1),piyasa_ae=ae)
    o=out['kosu_turu'][k]
    print(f"{k:22} {t['k']:4} {o['ort_alan']:5} {q(.1):4}-{q(.9):<4} (med {q(.5):3}) {o['favori']:5} {o['hp_lideri']:6} | {ae.get('HP sırası 2',0):.2f} {ae.get('HP sırası 3',0):.2f} | {ae.get('karma koşuda dişi',0):.2f} | {ae.get('kilo sırası 1',0):.2f}")
print(f"\n{'jokey':16} biniş kazanma% alan-A/E piyasa-A/E | Arap / İngiliz piyasa-A/E")
js=[(k,v) for k,v in J.items() if v['genel'][0]>=150]
for k,v in sorted(js,key=lambda kv:-kv[1]['genel'][1]/kv[1]['genel'][3]):
    g=v['genel']; pa=lambda d:f"{d[1]/d[3]:.2f}({d[0]})" if d[3]>1 else '-'
    out['jokey'][k]={kk:dict(binis=d[0],kazanma=d[1],alan_ae=round(d[1]/d[2],2) if d[2] else None,piyasa_ae=round(d[1]/d[3],2) if d[3] else None) for kk,d in v.items()}
    print(f"{k:16} {g[0]:5} {100*g[1]/g[0]:6.1f} {g[1]/g[2]:8.2f} {g[1]/g[3]:9.2f} | {pa(v['Arap'])} / {pa(v['İngiliz'])}")
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
