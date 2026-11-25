"""Her koşu türünde ne geliyor: favori mi, AGF favorisi mi, sürpriz mi? Gerçek TJK sonuçları.
Kullanım: kosu_turu_analiz.py veri/sonuc_temiz cikti.json
Bahis birimi: eküri tek birim. Favori = en düşük kesin ganyan. AGF favorisi = AGF sırası (1). HP lideri = en yüksek handikap puanı.
Sürpriz = kazananın ganyanı ≥10; büyük sürpriz ≥20."""
import sys,glob,os,re,json,collections,statistics
TAGS={'KG','K','DB','SK','SKG','GKR','ÖG','BB','YP','KK','TB','SKK','ÖN','GK','SGKR','KUL','BH','DS'}
def ad_(n):
    t=n.replace('(Koşmaz)','').split()
    while len(t)>1 and t[-1] in TAGS: t.pop()
    return ' '.join(t)
def tur(s):
    S=s.upper()
    for pat,f in [(r'\bG ?([123])\b',lambda m:'Grup '+m.group(1)),(r'KV-? ?(\d+)',lambda m:'KV-'+m.group(1)),(r'SATI',lambda m:'Satış'),
                  (r'MA[İI]DEN',lambda m:'Maiden'),(r'ŞARTLI ?-?(\d+)',lambda m:'Şartlı '+m.group(1)),(r'HAND[İI]KAP ?(\d+)',lambda m:'Handikap '+m.group(1)),(r'AÇIK|ACIK',lambda m:'Açık'),
                  (r'\bLİSTE|LISTED',lambda m:'Listed')]:
        m=re.search(pat,S)
        if m: return f(m)
    return 'Diğer'
def aile(t):
    if t.startswith('Şartlı 19') or t.startswith('Şartlı 27') or t=='Maiden': return 'Maiden (kazanmamışlar)'
    for a in ('Şartlı','Handikap','KV','Grup','Satış','Açık','Listed'):
        if t.startswith(a): return a
    return 'Diğer'
S=collections.defaultdict(lambda:collections.Counter()); G=collections.defaultdict(list)
for f in sorted(glob.glob(sys.argv[1]+'/*.csv')):
    cur=None; rs=[]
    for l in open(f,encoding='utf-8-sig').read().splitlines():
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]):
            t=tur(c[1]); cur=dict(t=t,a=aile(t),irk='Arap' if 'Arap' in l else 'İngiliz',h=[],ek=[]); rs.append(cur); continue
        if cur is not None and 'eküridir' in l: cur['ek'].append([ad_(a) for a in re.findall(r'\(\d+\)([^,\]]+)',l)])
        if cur is not None and c[0].isdigit() and len(c)>13:
            try:o=float(c[13].replace(',','.'))
            except Exception:o=0
            m=re.search(r'\((\d+)\)',c[10]); 
            try:hp=int(c[11])
            except Exception:hp=-1
            cur['h'].append(dict(ad=ad_(c[1]),pos=int(c[0]),o=o,ar=int(m.group(1)) if m else 0,hp=hp))
    for r in rs:
        h=r['h']
        if len(h)<4 or not all(x['o']>1 for x in h): continue
        grp={a:i for i,E in enumerate(r['ek']) for a in E}; U={}
        for x in h: U.setdefault(grp.get(x['ad'],'t'+x['ad']),[]).append(x)
        un=[dict(o=L[0]['o'],kaz=any(x['pos']==1 for x in L),ar=min((x['ar'] for x in L if x['ar']),default=99),hp=max(x['hp'] for x in L)) for L in U.values()]
        if sum(u['kaz'] for u in un)!=1: continue
        kaz=next(u for u in un if u['kaz']); fav=min(un,key=lambda u:u['o']); agf_var=any(u['ar']<99 for u in un)
        srt=sorted(un,key=lambda u:u['o']); hpm=max(u['hp'] for u in un); tot=sum(1/u['o'] for u in un)
        fq=(1/fav['o'])/tot; sq=sum((1/u['o'])/tot for u in un if u['o']>=10)
        for k in ('TÜMÜ',f"{r['a']}",f"{r['irk']} {r['a']}",f"{r['irk']} {r['t']}"):
            s=S[k]; s['n']+=1; s['birim']+=len(un); s['fav']+=fav['kaz']; s['fav_get']+=fav['o'] if fav['kaz'] else 0
            s['ilk3']+=kaz in srt[:3]; s['s10']+=kaz['o']>=10; s['s20']+=kaz['o']>=20; s['fq']+=fq; s['sq']+=sq
            rk=srt.index(kaz)
            for j in range(1,9): s[f'rk{j}']+=rk<j
            if agf_var: s['agf_n']+=1; s['agf1']+=kaz['ar']==1; s['agf3']+=kaz['ar']<=3
            if hpm>0: s['hp_n']+=1; s['hp1']+=kaz['hp']==hpm
            G[k].append(kaz['o'])
out={}
print("%-30s %5s %5s | %6s %6s %6s %6s | %6s %6s | %6s | %6s %6s %6s | %6s"%('koşu türü','koşu','alan','fav%','fvbek','ilk3%','favTL','AGF1%','AGF3%','HP1%','gny10+','bek','gny20+','medyan'))
def yaz(k):
    s=S[k]; n=s['n']
    if n<30: return
    d=dict(kosu=n,alan=round(s['birim']/n,1),favori=round(100*s['fav']/n,1),fav_ilk3=round(100*s['ilk3']/n,1),fav_getiri=round(100*s['fav_get']/n,1),
           agf1=round(100*s['agf1']/s['agf_n'],1) if s['agf_n'] else None,agf3=round(100*s['agf3']/s['agf_n'],1) if s['agf_n'] else None,
           hp1=round(100*s['hp1']/s['hp_n'],1) if s['hp_n'] else None,s10=round(100*s['s10']/n,1),fav_bek=round(100*s['fq']/n,1),s10_bek=round(100*s['sq']/n,1),s20=round(100*s['s20']/n,1),medyan=round(statistics.median(G[k]),2),
           ilk_k={j:round(100*s[f'rk{j}']/n,1) for j in range(1,9)})
    d['oneri_at']=next((j for j in range(3,9) if d['ilk_k'][j]>=80),8)   # kazananın en az %80'ini kapsayan en küçük at sayısı (en az 3)
    out[k]=d
    print("%-30s %5d %5.1f | %6.1f %6.1f %6.1f %6.1f | %6s %6s | %6s | %6.1f %6.1f %6.1f | %6.2f"%(k[:30],n,d['alan'],d['favori'],d['fav_bek'],d['fav_ilk3'],d['fav_getiri'],d['agf1'],d['agf3'],d['hp1'],d['s10'],d['s10_bek'],d['s20'],d['medyan']))
yaz('TÜMÜ'); print('-- aile')
for k in sorted(k for k in S if ' ' not in k or k.startswith('Maiden')):
    if k!='TÜMÜ' and not k.startswith(('Arap','İngiliz')): yaz(k)
for irk in ('Arap','İngiliz'):
    print('--',irk,'aile'); [yaz(k) for k in sorted(S) if k.startswith(irk+' ') and k[len(irk)+1:] in ('Maiden (kazanmamışlar)','Şartlı','Handikap','KV','Grup','Satış','Açık','Listed','Diğer')]
    print('--',irk,'tür'); [yaz(k) for k in sorted(S,key=lambda k:(re.sub(r'\d+','',k),int(re.search(r'\d+',k).group()) if re.search(r'\d+',k) else 0)) if k.startswith(irk+' ') and k[len(irk)+1:] not in ('Maiden (kazanmamışlar)','Şartlı','Handikap','KV','Grup','Satış','Açık','Listed','Diğer')]
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
