"""Soy (pedigri) raporu: aygır (baba) ve anne bazında gerçek sonuçlar. Kullanım: soy_rapor.py sonuc_dizini cikti.json
Aygır: yavru sayısı, koşu, galibiyet, kazanma %, alan A/E, piyasa A/E (eküri tek birim) iki dönem ayrı; yaşa göre (genç/4+); zemin.
Anne: yavru sayısı ve kardeşlerin toplam başarısı."""
import sys,glob,os,re,json,collections
TAGS={'KG','K','DB','SK','SKG','GKR','ÖG','BB','YP','KK','TB','SKK','ÖN','GK','SGKR','KUL','BH','DS'}
def ad_(n):
    t=n.replace('(Koşmaz)','').split()
    while len(t)>1 and t[-1] in TAGS: t.pop()
    return ' '.join(t)
fs=sorted(glob.glob(sys.argv[1]+'/*.csv')); gun=sorted(set(os.path.basename(f)[:10] for f in fs)); orta=gun[len(gun)//2]
S=collections.defaultdict(lambda:dict(at=set(),k=0,w=0,e=0.0,q=[0.0,0.0],wq=[0,0],gen=[0,0.0],yet=[0,0.0],pist=collections.defaultdict(lambda:[0,0.0])))
A=collections.defaultdict(lambda:dict(yavru=set(),k=0,w=0,e=0.0))
for f in fs:
    yr=0 if os.path.basename(f)[:10]<orta else 1; cur=None; rs=[]
    for l in open(f,encoding='utf-8-sig'):
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]): cur=dict(irk='Arap' if 'Arap' in l else 'İngiliz',pist=next((p for p in ('Kum','Çim','Sentetik') if p in l),'?'),h=[],ek=[]); rs.append(cur); continue
        if cur is not None and 'eküridir' in l: cur['ek'].append([ad_(a) for a in re.findall(r'\(\d+\)([^,\]]+)',l)])
        if cur is not None and c[0].isdigit() and len(c)>13:
            try:o=float(c[13].replace(',','.'))
            except Exception:o=0
            y=c[2].split()
            cur['h'].append(dict(ad=ad_(c[1]),pos=int(c[0]) if c[12].strip() else 99,o=o,baba=c[3].strip(),anne=c[4].strip(),genc=bool(y) and y[-1] in ('e','d')))
    for r in rs:
        h=r['h']; n=len(h)
        if n<4: continue
        ok=all(x['o']>1 for x in h)
        if ok:
            grp={a:i for i,E in enumerate(r['ek']) for a in E}; U={}
            for x in h: U.setdefault(grp.get(x['ad'],'t'+x['ad']),[]).append(x)
            tot=sum(1/L[0]['o'] for L in U.values())
            for L in U.values():
                for x in L: x['q']=(1/x['o'])/tot/len(L)
        for x in h:
            w=x['pos']==1; s=S[(r['irk'],x['baba'])]; s['at'].add(x['ad']); s['k']+=1; s['w']+=w; s['e']+=1/n
            if ok: s['q'][yr]+=x['q']; s['wq'][yr]+=w
            g=s['gen' if x['genc'] else 'yet']; g[0]+=w; g[1]+=1/n; p=s['pist'][r['pist']]; p[0]+=w; p[1]+=1/n
            a=A[(r['irk'],x['anne'])]; a['yavru'].add(x['ad']); a['k']+=1; a['w']+=w; a['e']+=1/n
out={'aygir':{},'anne':{}}
for I in ('Arap','İngiliz'):
    L=[(k[1],v) for k,v in S.items() if k[0]==I and v['k']>=150]
    L.sort(key=lambda kv:-kv[1]['w'])
    print(f"\n===== {I}: en çok kazanan 25 aygır (150+ yavru koşusu) =====")
    print(f"{'aygır':22} {'yavru':>5} {'koşu':>5} {'galibiyet':>9} {'%':>5} {'alan A/E':>8} {'piyasa A/E 1./2. dönem':>22} {'genç/4+ A/E':>12}  zemin A/E")
    for b,v in L[:25]:
        pa=[f"{v['wq'][i]/v['q'][i]:.2f}" if v['q'][i]>3 else '-' for i in (0,1)]
        gy=f"{v['gen'][0]/v['gen'][1]:.2f}/{v['yet'][0]/v['yet'][1]:.2f}" if v['gen'][1]>2 and v['yet'][1]>2 else '-'
        zm=' '.join(f"{p[:3]} {x[0]/x[1]:.2f}" for p,x in v['pist'].items() if x[1]>5)
        print(f"{b[:22]:22} {len(v['at']):5} {v['k']:5} {v['w']:9} {100*v['w']/v['k']:5.1f} {v['w']/v['e']:8.2f} {pa[0]:>11}/{pa[1]:<10} {gy:>12}  {zm}")
    for b,v in S.items():
        if b[0]==I and v['k']>=50:
            out['aygir'][f"{I}|{b[1]}"]=dict(yavru=len(v['at']),kosu=v['k'],galibiyet=v['w'],alan_ae=round(v['w']/v['e'],2),
                piyasa_ae=[round(v['wq'][i]/v['q'][i],2) if v['q'][i]>3 else None for i in (0,1)])
    AN=[(k[1],v) for k,v in A.items() if k[0]==I and len(v['yavru'])>=3 and v['k']>=20]
    AN.sort(key=lambda kv:-(kv[1]['w']+1)/(kv[1]['e']+1))
    print(f"\n{I}: 3+ yavrusu koşan {len(AN)} anne. Yavruları en başarılı 10 anne (alan A/E):")
    for a,v in AN[:10]: print(f"  {a[:22]:22} {len(v['yavru'])} yavru, {v['k']} koşu, {v['w']} galibiyet, A/E {v['w']/v['e']:.2f}")
    for a,v in A.items():
        if a[0]==I and v['k']>=10: out['anne'][f"{I}|{a[1]}"]=dict(yavru=len(v['yavru']),kosu=v['k'],galibiyet=v['w'],alan_ae=round(v['w']/v['e'],2))
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False)
# aygır piyasa A/E kalıcı mı? (1. dönem ile 2. dönem korelasyonu)
import statistics
for I in ('Arap','İngiliz'):
    P=[(v['wq'][0]/v['q'][0],v['wq'][1]/v['q'][1]) for k,v in S.items() if k[0]==I and v['q'][0]>8 and v['q'][1]>8]
    if len(P)>5: print(f"\n{I}: aygır piyasa A/E kalıcılığı: {len(P)} aygır, 1. ve 2. dönem korelasyonu {statistics.correlation([a for a,_ in P],[b for _,b in P]):.2f}")
