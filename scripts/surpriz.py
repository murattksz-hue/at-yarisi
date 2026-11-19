"""Sürpriz analizi (eküri tek bahis birimi). Kullanım: surpriz.py sonuc_dizini hava_gecmis.json cikti.json
Sürpriz = kazanan birimin ganyanı >= 10 (yani piyasa olasılığı ~%8 altı)."""
import sys,glob,os,re,json,collections
TAGS={'KG','K','DB','SK','SKG','GKR','ÖG','BB','YP','KK','TB','SKK','ÖN','GK','SGKR','KUL','BH','DS'}
def ad_(n):
    t=n.replace('(Koşmaz)','').split()
    while len(t)>1 and t[-1] in TAGS: t.pop()
    return ' '.join(t)
def aile(h):
    s=h.upper()
    for pat,a in [(r'G ?[123]\b','Grup'),(r'KV','KV'),(r'SATI','Satış'),(r'MAIDEN|MAİDEN|ŞARTLI ?-?19','Maiden'),(r'ŞARTLI','Şartlı'),(r'HANDİKAP|HANDIKAP','Handikap')]:
        if re.search(pat,s): return a
    return 'Diğer'
HV=json.load(open(sys.argv[2],encoding='utf-8'))
S=collections.defaultdict(lambda:[0,0,0])   # koşu, favori kazandı, sürpriz
B=collections.defaultdict(lambda:[0,0.0,0,0.0])   # oran kovası: kazanma, piyasa beklentisi, birim sayısı, 1 TL getiri
for f in sorted(glob.glob(sys.argv[1]+'/*.csv')):
    b=os.path.basename(f)[:-4]; isl=(HV.get(b,{}).get('islaklik') or 0)>=5; cur=None; rs=[]
    for l in open(f,encoding='utf-8-sig').read().splitlines():
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]):
            cur=dict(aile=aile(c[1]),irk='Arap' if 'Arap' in l else 'İngiliz',pist=next((p for p in ('Kum','Çim','Sentetik') if p in l),'?'),h=[],ek=[]); rs.append(cur); continue
        if cur is not None and 'eküridir' in l: cur['ek'].append([ad_(a) for a in re.findall(r'\(\d+\)([^,\]]+)',l)])
        if cur is not None and c[0].isdigit() and len(c)>13:
            try:o=float(c[13].replace(',','.'))
            except:o=0
            cur['h'].append(dict(ad=ad_(c[1]),pos=int(c[0]) if c[12].strip() else 99,o=o))
    for r in rs:
        h=r['h']
        if len(h)<4 or not all(x['o']>1 for x in h): continue
        grp={a:i for i,E in enumerate(r['ek']) for a in E}; U={}
        for x in h: U.setdefault(grp.get(x['ad'],'t'+x['ad']),[]).append(x)
        un=[dict(o=L[0]['o'],kaz=any(x['pos']==1 for x in L)) for L in U.values()]
        if sum(u['kaz'] for u in un)!=1: continue
        tot=sum(1/u['o'] for u in un); fav=min(un,key=lambda u:u['o']); kaz=next(u for u in un if u['kaz'])
        n=len(un); alan='≤7' if n<=7 else '8-10' if n<=10 else '11-13' if n<=13 else '14+'
        for k in ('TÜMÜ',f"ırk: {r['irk']}",f"koşu türü: {r['irk']} {r['aile']}",f"alan (bahis birimi): {alan}",f"pist: {r['pist']}{' ıslak' if isl else ''}",
                  'eküri var' if r['ek'] else 'eküri yok',f"favori piyasa olasılığı: {min(int(100*(1/fav['o'])/tot)//10*10,60)}%+"):
            s=S[k]; s[0]+=1; s[1]+=fav['kaz']; s[2]+=kaz['o']>=10
        for u in un:
            q=(1/u['o'])/tot; kv='1-2' if u['o']<2 else '2-3' if u['o']<3 else '3-5' if u['o']<5 else '5-10' if u['o']<10 else '10-20' if u['o']<20 else '20-50' if u['o']<50 else '50+'
            bb=B[kv]; bb[0]+=u['kaz']; bb[1]+=q; bb[2]+=1; bb[3]+=u['o'] if u['kaz'] else 0
out={'gruplar':{},'oran_kovalari':{}}
print(f"{'grup':40} koşu favori%  sürpriz%(ganyan≥10)")
for k in sorted(S,key=lambda k:(k!='TÜMÜ',k)):
    s=S[k]
    if s[0]<30: continue
    out['gruplar'][k]=dict(kosu=s[0],favori=round(100*s[1]/s[0],1),surpriz=round(100*s[2]/s[0],1))
    print(f"{k:40} {s[0]:5} {100*s[1]/s[0]:6.1f}  {100*s[2]/s[0]:6.1f}")
print(f"\nGanyan oranına göre (eküri tek birim): birim sayısı, kazanma, piyasa beklentisi, piyasa A/E, 1 TL'nin getirisi")
for kv in ['1-2','2-3','3-5','5-10','10-20','20-50','50+']:
    bb=B[kv]
    if not bb[2]: continue
    out['oran_kovalari'][kv]=dict(birim=bb[2],kazanma=bb[0],piyasa_ae=round(bb[0]/bb[1],2),getiri=round(100*bb[3]/bb[2],1))
    print(f"  ganyan {kv:6} {bb[2]:6} {bb[0]:5} {bb[1]:8.1f}  {bb[0]/bb[1]:5.2f}  %{100*bb[3]/bb[2]:5.1f}")
json.dump(out,open(sys.argv[3],'w'),ensure_ascii=False,indent=1)
