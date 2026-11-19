"""Maiden / Şartlı 19 (koşu kazanmamış atlar) sürpriz analizi — gerçek TJK sonuçlarıyla.
Kullanım: maiden_analiz.py veri/sonuc_temiz cikti.json
Piyasa olasılığı = kesin ganyandan (eküri tek bahis birimi). A/E = gerçek kazanma / piyasa beklentisi.
Önceki koşu sayısı yalnızca elimizdeki veriden (2025-05-07 sonrası) sayılır; 3 yaşlıların daha eski koşuları görünmez."""
import sys,glob,os,re,json,collections,statistics
TAGS={'KG','K','DB','SK','SKG','GKR','ÖG','BB','YP','KK','TB','SKK','ÖN','GK','SGKR','KUL','BH','DS'}
def ad_(n):
    t=n.replace('(Koşmaz)','').split()
    while len(t)>1 and t[-1] in TAGS: t.pop()
    return ' '.join(t)
def sinif(h):
    s=h.upper(); irk='Arap' if 'ARAP' in s else 'İngiliz'; yas=re.search(r'(\d) (VE YUKARI )?YAŞLI',s)
    y=(yas.group(1)+('+' if yas.group(2) else '')) if yas else '?'
    if re.search(r'MA[İI]DEN',s): t='Maiden'
    elif re.search(r'ŞARTLI ?-?(19|27)\b',s): t='Şartlı 19/27'
    elif re.search(r'G ?[123]\b|KV|SATI',s): t='KV/Grup/Satış'
    elif 'ŞARTLI' in s: t='Diğer Şartlı'
    elif re.search(r'HAND[İI]KAP',s): t='Handikap'
    else: t='Diğer'
    return t,irk,y
R=[]
for f in sorted(glob.glob(sys.argv[1]+'/*.csv')):
    tarih=os.path.basename(f)[:10]; cur=None
    for l in open(f,encoding='utf-8-sig').read().splitlines():
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]):
            t,irk,y=sinif(';'.join(c[1:3])); cur=dict(tarih=tarih,tur=t,irk=irk,yas=y,h=[],ek=[]); R.append(cur); continue
        if cur is not None and 'eküridir' in l: cur['ek'].append([ad_(a) for a in re.findall(r'\(\d+\)([^,\]]+)',l)])
        if cur is not None and c[0].isdigit() and len(c)>13:
            try:o=float(c[13].replace(',','.'))
            except:o=0
            cur['h'].append(dict(ad=ad_(c[1]),key=ad_(c[1])+'|'+c[3].strip(),pos=int(c[0]),o=o))
R.sort(key=lambda r:r['tarih'])
gecmis=collections.defaultdict(list)   # at -> önceki bitirişler (kronolojik, sızıntı yok)
S=collections.defaultdict(lambda:dict(n=0,fav=0,s10=0,s20=0,g=[]))
A=collections.defaultdict(lambda:[0,0.0,0,0.0])  # kazanma, piyasa beklentisi, birim, 1TL getiri
def ekle(k,u,q):
    a=A[k]; a[0]+=u['kaz']; a[1]+=q; a[2]+=1; a[3]+=u['o'] if u['kaz'] else 0
for r in R:
    h=r['h']; ok=len(h)>=4 and all(x['o']>1 for x in h)
    if ok:
        grp={a:i for i,E in enumerate(r['ek']) for a in E}; U={}
        for x in h: U.setdefault(grp.get(x['ad'],'t'+x['ad']),[]).append(x)
        un=[dict(o=L[0]['o'],kaz=any(x['pos']==1 for x in L),L=L) for L in U.values()]
        if sum(u['kaz'] for u in un)==1:
            tot=sum(1/u['o'] for u in un); fav=min(un,key=lambda u:u['o']); kaz=next(u for u in un if u['kaz'])
            mk=r['tur'] in ('Maiden','Şartlı 19/27')
            for k in ('TÜMÜ',r['tur'],(f"{r['tur']} {r['irk']} {r['yas']} yaş" if mk else None),('Maiden+Ş19 hepsi' if mk else 'Kazanmış atların koşuları')):
                if not k: continue
                s=S[k]; s['n']+=1; s['fav']+=fav['kaz']; s['s10']+=kaz['o']>=10; s['s20']+=kaz['o']>=20; s['g'].append(kaz['o'])
            if mk and r['tarih']>='2025-09-01':
                for u in un:
                    if len(u['L'])>1: continue
                    x=u['L'][0]; q=(1/u['o'])/tot; g=gecmis[x['key']]; n=len(g)
                    ekle('önceki koşu (veride): '+('0 = ilk koşu' if n==0 else '1' if n==1 else '2-3' if n<=3 else '4-6' if n<=6 else '7+'),u,q)
                    if n: ekle('son koşu bitirişi: '+('2' if g[-1]==2 else '3' if g[-1]==3 else '4-5' if g[-1]<=5 else '6+'),u,q)
                    kv='<3' if u['o']<3 else '3-5' if u['o']<5 else '5-10' if u['o']<10 else '10-20' if u['o']<20 else '20-50' if u['o']<50 else '50+'
                    ekle('ganyan '+kv,u,q)
                    if n==0: ekle(f"ilk koşu × {r['irk']} {r['yas']} yaş",u,q)
    for x in h: gecmis[x['key']].append(x['pos'])
out={'kosu':{},'ae':{}}
print("Koşu türüne göre (kesin ganyanı tam olan koşular)\n%-38s %5s %8s %10s %10s %8s"%('grup','koşu','favori%','gny≥10 %','gny≥20 %','medyan'))
for k in sorted(S,key=lambda k:(k!='TÜMÜ',k)):
    s=S[k]
    if s['n']<30: continue
    m=statistics.median(s['g']); out['kosu'][k]=dict(kosu=s['n'],favori=round(100*s['fav']/s['n'],1),s10=round(100*s['s10']/s['n'],1),s20=round(100*s['s20']/s['n'],1),medyan=m)
    print("%-38s %5d %8.1f %10.1f %10.1f %8.2f"%(k,s['n'],100*s['fav']/s['n'],100*s['s10']/s['n'],100*s['s20']/s['n'],m))
print("\nMaiden + Şartlı 19/27 içinde (2025-09-01 sonrası): birim, kazanma, piyasa beklentisi, A/E, 1 TL getiri")
for k in sorted(A):
    a=A[k]
    if a[2]<50: continue
    out['ae'][k]=dict(birim=a[2],kazanma=a[0],beklenti=round(a[1],1),ae=round(a[0]/a[1],2),getiri=round(100*a[3]/a[2],1))
    print("  %-34s %6d %5d %7.1f  %5.2f  %%%5.1f"%(k,a[2],a[0],a[1],a[0]/a[1],100*a[3]/a[2]))
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
