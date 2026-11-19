"""Harville (ikili/sıralı ikili) kalibrasyonu: ganyandan türeyen kazanma olasılıklarıyla tahmin edilen
'ilk iki' olasılığı ile gerçek sonuç karşılaştırılır (eküri tek birim). Kullanım: harville_test.py sonuc_dizini"""
import sys,glob,re,collections
TAGS={'KG','K','DB','SK','SKG','GKR','ÖG','BB','YP','KK','TB','SKK','ÖN','GK','SGKR','KUL','BH','DS'}
def ad_(n):
    t=n.replace('(Koşmaz)','').split()
    while len(t)>1 and t[-1] in TAGS: t.pop()
    return ' '.join(t)
K=collections.defaultdict(lambda:[0,0.0,0]); S2=collections.defaultdict(lambda:[0,0.0,0]); nk=0
for f in sorted(glob.glob(sys.argv[1]+'/*.csv')):
    cur=None; rs=[]
    for l in open(f,encoding='utf-8-sig'):
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]): cur=dict(h=[],ek=[]); rs.append(cur); continue
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
        un=[(1/L[0]['o'],min(x['pos'] for x in L)) for L in U.values()]; tot=sum(a for a,_ in un); un=[(a/tot,b) for a,b in un]
        if sorted(b for _,b in un)[:2]!=[1,2]: continue
        nk+=1
        for i,(pi,bi) in enumerate(un):
            # 'ilk ikide' olasılığı (Harville): p_i + sum_j p_j p_i/(1-p_j)
            p2=pi+sum(pj*pi/(1-pj) for j,(pj,_) in enumerate(un) if j!=i)
            kv=min(int(p2*10),9); S2[kv][0]+=1; S2[kv][1]+=p2; S2[kv][2]+=bi<=2
        # sıralı ikili: en olası 3 sıralı kombinasyon
        C=sorted(((pi*pj/(1-pi),bi,bj) for i,(pi,bi) in enumerate(un) for j,(pj,bj) in enumerate(un) if i!=j),reverse=True)
        for pr,bi,bj in C[:5]:
            kv=min(int(pr*20),9); K[kv][0]+=1; K[kv][1]+=pr; K[kv][2]+=(bi==1 and bj==2)
print('koşu:',nk)
print("İlk ikiye girme (Harville tahmini vs gerçek):")
for kv in sorted(S2): a=S2[kv]; print(f"  tahmin %{10*kv}-{10*kv+10}: {a[0]:6} birim, ort. tahmin %{100*a[1]/a[0]:5.1f}, gerçek %{100*a[2]/a[0]:5.1f}")
print("Sıralı ikili (her koşunun en olası 5 kombinasyonu):")
for kv in sorted(K): a=K[kv]; print(f"  tahmin %{5*kv}-{5*kv+5}: {a[0]:6} kombinasyon, ort. tahmin %{100*a[1]/a[0]:5.1f}, gerçek %{100*a[2]/a[0]:5.1f}")
