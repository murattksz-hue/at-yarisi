"""Arap ve İngiliz atlarının karakteristik yapısı (gerçek TJK sonuçlarından). Kullanım: irk_karakter.py sonuc_dizini
Hız: kazanan süresinden m/sn. Yaş/cinsiyet: alan büyüklüğüne göre A/E. İstikrar: aynı atın ardışık koşularındaki bitiş derecesi ilişkisi.
Kazanma farkı: 1. ile 2. arası saniye."""
import sys,glob,os,re,collections,statistics
TAGS={'KG','K','DB','SK','SKG','GKR','ÖG','BB','YP','KK','TB','SKK','ÖN','GK','SGKR','KUL','BH','DS'}
def ad_(n):
    t=n.replace('(Koşmaz)','').split()
    while len(t)>1 and t[-1] in TAGS: t.pop()
    return ' '.join(t)
def sn(x):
    m=re.match(r'(\d+):(\d+)\.(\d+)',x.strip()); return int(m.group(1))*60+int(m.group(2))+int(m.group(3))/100 if m else None
CINS={'e':'erkek','d':'dişi','a':'aygır','k':'kısrak','g':'iğdiş'}
HIZ=collections.defaultdict(list); KOSU=collections.Counter(); MES=collections.defaultdict(collections.Counter); PIST=collections.defaultdict(collections.Counter)
YAS=collections.defaultdict(lambda:[0,0.0,0]); CIN=collections.defaultdict(lambda:[0,0.0,0]); FARK=collections.defaultdict(list); ALAN=collections.defaultdict(list)
GECMIS=collections.defaultdict(list); KILO=collections.defaultdict(list)
for f in sorted(glob.glob(sys.argv[1]+'/*.csv')):
    cur=None; rs=[]
    for l in open(f,encoding='utf-8-sig'):
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]):
            m=re.search(r'(\d{3,4})m',l); cur=dict(irk='Arap' if 'Arap' in l else 'İngiliz',pist=next((p for p in ('Kum','Çim','Sentetik') if p in l),'?'),m=int(m.group(1)) if m else 0,dis='Dişi' in c[1],h=[]); rs.append(cur); continue
        if cur is not None and c[0].isdigit() and len(c)>13:
            y=c[2].split(); kg=re.match(r'([\d,]+)',c[5])
            cur['h'].append(dict(ad=ad_(c[1]),pos=int(c[0]) if c[12].strip() else 99,t=sn(c[12]),yas=int(y[0][:-1]) if y and y[0][:-1].isdigit() else None,cins=CINS.get(y[-1],'?') if y else '?',kg=float(kg.group(1).replace(',','.')) if kg else None))
    for r in rs:
        h=r['h']; n=len(h); I=r['irk']
        if n<4 or not r['m']: continue
        KOSU[I]+=1; ALAN[I].append(n); b='≤1400' if r['m']<=1400 else '1500-1900' if r['m']<=1900 else '2000+'; MES[I][b]+=1; PIST[I][r['pist']]+=1
        w=sorted([x for x in h if x['t'] and x['pos']<99],key=lambda x:x['pos'])
        if len(w)>=2 and w[0]['pos']==1:
            HIZ[(I,r['pist'],b)].append(r['m']/w[0]['t']); FARK[I].append(w[1]['t']-w[0]['t'])
        for x in h:
            wn=x['pos']==1
            if x['yas']: a=YAS[(I,min(x['yas'],8))]; a[0]+=wn; a[1]+=1/n; a[2]+=1
            if not r['dis']: k=CIN[(I,'dişi' if x['cins'] in ('dişi','kısrak') else 'erkek')]; k[0]+=wn; k[1]+=1/n; k[2]+=1
            if x['kg']: KILO[I].append(x['kg'])
            GECMIS[(I,x['ad'])].append(min(x['pos'],15)/n)
print("=== Genel ===")
for I in ('Arap','İngiliz'): print(f"{I}: {KOSU[I]} koşu, ortalama {statistics.mean(ALAN[I]):.1f} at/koşu, ortalama kilo {statistics.mean(KILO[I]):.1f} kg, kazanma farkı medyanı {statistics.median(FARK[I]):.2f} sn (1. ile 2. arası)")
print("\n=== Mesafe ve zemin dağılımı (koşu payı) ===")
for I in ('Arap','İngiliz'):
    print(f"{I}: mesafe "+', '.join(f"{k} %{100*v/KOSU[I]:.0f}" for k,v in sorted(MES[I].items()))+" | zemin "+', '.join(f"{k} %{100*v/KOSU[I]:.0f}" for k,v in PIST[I].most_common()))
print("\n=== Kazanan hızı (m/sn, medyan) ===")
for p in ('Kum','Çim','Sentetik'):
    for b in ('≤1400','1500-1900','2000+'):
        a,i=HIZ.get(('Arap',p,b),[]),HIZ.get(('İngiliz',p,b),[])
        if len(a)>=10 and len(i)>=10: print(f"  {p:8} {b:10} Arap {statistics.median(a):.2f} ({len(a)})  İngiliz {statistics.median(i):.2f} ({len(i)})  fark %{100*(statistics.median(i)/statistics.median(a)-1):.1f}")
print("\n=== Yaşa göre kazanma (alan büyüklüğüne göre A/E; 1,00 = ortalama) ===")
for I in ('Arap','İngiliz'):
    print(f"{I}: "+', '.join(f"{y}{'+' if y==8 else ''} yaş {YAS[(I,y)][0]/YAS[(I,y)][1]:.2f} ({YAS[(I,y)][2]})" for y in range(2,9) if YAS[(I,y)][2]>=200))
print("\n=== Karma koşularda cinsiyet (A/E) ===")
for I in ('Arap','İngiliz'): print(f"{I}: "+', '.join(f"{c} {CIN[(I,c)][0]/CIN[(I,c)][1]:.2f} ({CIN[(I,c)][2]})" for c in ('erkek','dişi')))
print("\n=== İstikrar: atın ardışık iki koşusundaki göreli derece korelasyonu (yüksek = daha tutarlı) ===")
for I in ('Arap','İngiliz'):
    xs,ys=[],[]
    for (ii,_),L in GECMIS.items():
        if ii!=I: continue
        for a,b in zip(L,L[1:]): xs.append(a); ys.append(b)
    print(f"{I}: {statistics.correlation(xs,ys):.3f} ({len(xs)} ardışık koşu çifti)")
