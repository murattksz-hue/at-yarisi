"""Cinsiyet kodlarına göre ayrı ayrı analiz (gerçek TJK sonuçları). Kullanım: cinsiyet_analiz.py sonuc_dizini
Kodlar (programdaki yaş alanının sonu): e=erkek, d=dişi, a=aygır, k=kısrak, g=iğdiş.
Ölçüler: alan A/E (kazanma / 1-bölü-at-sayısı) ve piyasa A/E (kazanma / ganyandan beklenti, eküri tek birim); iki dönem ayrı."""
import sys,glob,os,re,collections
TAGS={'KG','K','DB','SK','SKG','GKR','ÖG','BB','YP','KK','TB','SKK','ÖN','GK','SGKR','KUL','BH','DS'}
def ad_(n):
    t=n.replace('(Koşmaz)','').split()
    while len(t)>1 and t[-1] in TAGS: t.pop()
    return ' '.join(t)
CINS={'e':'erkek','d':'dişi','a':'aygır','k':'kısrak','g':'iğdiş'}
fs=sorted(glob.glob(sys.argv[1]+'/*.csv')); gun=sorted(set(os.path.basename(f)[:10] for f in fs)); orta=gun[len(gun)//2]
A=collections.defaultdict(lambda:[0,0.0,0.0,0,0,0])   # kazanma, alan beklenti, piyasa beklenti, at, piyasalı at, piyasalı kazanma
YAS=collections.defaultdict(collections.Counter)
for f in fs:
    yari=1 if os.path.basename(f)[:10]<orta else 2; cur=None; rs=[]
    for l in open(f,encoding='utf-8-sig'):
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]): cur=dict(irk='Arap' if 'Arap' in l else 'İngiliz',dis='Dişi' in c[1],h=[],ek=[]); rs.append(cur); continue
        if cur is not None and 'eküridir' in l: cur['ek'].append([ad_(a) for a in re.findall(r'\(\d+\)([^,\]]+)',l)])
        if cur is not None and c[0].isdigit() and len(c)>13:
            try:o=float(c[13].replace(',','.'))
            except Exception:o=0
            y=c[2].split(); yas=int(y[0][:-1]) if y and y[0][:-1].isdigit() else None
            cur['h'].append(dict(ad=ad_(c[1]),pos=int(c[0]) if c[12].strip() else 99,o=o,cins=CINS.get(y[-1],'?') if y else '?',yas=yas))
    for r in rs:
        h=r['h']; n=len(h)
        if n<4: continue
        karma=not r['dis'] and len(set(x['cins'] in ('dişi','kısrak') for x in h))==2
        ok=all(x['o']>1 for x in h)
        if ok:
            grp={a:i for i,E in enumerate(r['ek']) for a in E}; U={}
            for x in h: U.setdefault(grp.get(x['ad'],'t'+x['ad']),[]).append(x)
            tot=sum(1/L[0]['o'] for L in U.values())
            for L in U.values():
                for x in L: x['q']=(1/x['o'])/tot/len(L)
        for x in h:
            YAS[(r['irk'],x['cins'])][x['yas']]+=1
            for k in ((r['irk'],x['cins'],'tüm koşular',yari),(r['irk'],x['cins'],'karma koşu',yari) if karma else None):
                if not k: continue
                a=A[k]; a[0]+=x['pos']==1; a[1]+=1/n; a[3]+=1
                if ok: a[2]+=x['q']; a[4]+=1; a[5]+=x['pos']==1
print("Cinsiyetlerin yaş dağılımı (kodların anlamını veriyle doğrulamak için):")
for I in ('Arap','İngiliz'):
    for c in ('erkek','dişi','aygır','kısrak','iğdiş'):
        Y=YAS[(I,c)]
        if sum(Y.values()): print(f"  {I:7} {c:7} {sum(Y.values()):6} at-koşu | yaşlar: "+', '.join(f"{y}:{v}" for y,v in sorted(Y.items()) if y))
print(f"\nA/E (1,00 = ortalama). Piyasa A/E <1: halk fazla oynuyor. Dönem sınırı {orta}.")
print(f"{'ırk':7} {'cinsiyet':8} {'kapsam':11} {'dönem':5} {'at':>6} {'kazanan':>7} {'alan A/E':>9} {'piyasa A/E':>11}")
for I in ('Arap','İngiliz'):
    for c in ('erkek','dişi','aygır','kısrak','iğdiş'):
        for kp in ('tüm koşular','karma koşu'):
            for yr in (1,2):
                a=A[(I,c,kp,yr)]
                if a[3]<100: continue
                print(f"{I:7} {c:8} {kp:11} {yr:5} {a[3]:6} {a[0]:7} {a[0]/a[1]:9.2f} {a[5]/a[2] if a[2] else 0:11.2f}")
