"""Mesafe sicili testi: atın bugünkü mesafe (±200 m), uzun (>=1900 m) ve kısa (<=1500 m) geçmişi piyasanın ötesinde bilgi veriyor mu? Kullanım: mesafe_sicil_testi.py -> veri/mesafe_sicil_testi.md
Özellikler yalnızca koşudan ÖNCEKİ geçmişten (kronolojik, sızıntı yok; at_gecmisi 2020+, değerlendirme 2022+). Ölçü: A/E = kazanma / kapanış ganyanından normalize beklenen; z=(w-e)/sqrt(e).
Gruplar: tüm atlar, uzun atlar (piyasa p<%10), orta (%10-25), favori (>=%25). Yalnızca okur; yazar veri/mesafe_sicil_testi.md."""
import os,glob,gzip,csv,io,math,collections
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
R=collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','*','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
H=collections.defaultdict(list)   # kod -> [(mesafe, sonuc)]
rows=[]
def st(L): return (len(L),sum(1 for x in L if x[1]==1),sum(1 for x in L if x[1] and x[1]<=3))
for key in sorted(R):
    rs=R[key]; g=[f(r['ganyan']) for r in rs]
    ok=key[0]>='2022-01-01' and len(rs)>=5 and not any(x is None or x<=1 for x in g) and sum(r['sonuc'].strip()=='1' for r in rs)==1
    if ok:
        sv=sum(1/x for x in g); m=f(rs[0]['mesafe']) or 0
        for r,x in zip(rs,g):
            h=H[r['kod']]; p=(1/x)/sv; w=r['sonuc'].strip()=='1'
            yak=[v for v in h if abs(v[0]-m)<=200]; uz=[v for v in h if v[0]>=1900]; ks=[v for v in h if v[0]<=1500]
            a=st(yak); u=st(uz); k=st(ks)
            F={}
            F['mesafe ±200 m: >=3 start, galibiyet oranı >=%30']=a[0]>=3 and a[1]/a[0]>=0.30
            F['mesafe ±200 m: >=3 start, ilk 3 oranı >=%50']=a[0]>=3 and a[2]/a[0]>=0.50
            F['mesafe ±200 m: >=3 start, hiç galibiyet yok']=a[0]>=3 and a[1]==0
            F['mesafe ±200 m: hiç koşmamış']=a[0]==0
            if m>=1900:
                F['uzun mesafe günü: uzun sicil iyi (>=3 start, ilk 3 >=%50)']=u[0]>=3 and u[2]/u[0]>=0.5
                F['uzun mesafe günü: uzun sicil kötü (>=4 start, ilk 3 yok)']=u[0]>=4 and u[2]==0
                F['uzun mesafe günü: kısa mesafe atı (>=5 kısa start, uzun <=1 start)']=k[0]>=5 and u[0]<=1
            if m<=1500:
                F['kısa mesafe günü: kısa sicil iyi (>=3 start, ilk 3 >=%50)']=k[0]>=3 and k[2]/k[0]>=0.5
                F['kısa mesafe günü: kısa sicil kötü (>=4 start, ilk 3 yok)']=k[0]>=4 and k[2]==0
                F['kısa mesafe günü: uzun mesafe atı (>=5 uzun start, kısa <=1 start)']=u[0]>=5 and k[0]<=1
            rows.append((key[0],p,w,x,F))
    for r in rs:
        s=r['sonuc'].strip()
        H[r['kod']].append((f(r['mesafe']) or 0,int(s) if s.isdigit() else None))
tarihler=sorted({t for t,*_ in rows}); mid=tarihler[len(tarihler)//2]
names=[]
for *_,F in rows:
    for k in F:
        if k not in names: names.append(k)
def tab(baslik,filt):
    L=[f'### {baslik}','','| Özellik | At | Kazanan | A/E | z | ilk yarı A/E | ikinci yarı A/E |','|---|---|---|---|---|---|---|']
    for ad in names:
        n=w=0;e=e1=e2=0.0;w1=w2=0
        for t,p,wi,x,F in rows:
            if ad not in F or not F[ad] or not filt(p,x): continue
            n+=1;e+=p;w+=wi
            if t<mid: e1+=p;w1+=wi
            else: e2+=p;w2+=wi
        if n>=300 and e>0: L.append(f'| {ad} | {n:,} | {w:,} | {w/e:.2f} | {(w-e)/math.sqrt(e):+.1f} | {(w1/e1) if e1 else 0:.2f} | {(w2/e2) if e2 else 0:.2f} |')
    return L+['']
OUT=['# Mesafe sicili testi','',f'at_gecmisi 2022–2026, {len(rows):,} at-koşu. A/E>1: piyasa eksik fiyatlamış. Çoklu karşılaştırma: |z|<3 zayıf, iki yarı aynı yönde değilse güvenme.','']
OUT+=tab('Tüm atlar',lambda p,x:True)
OUT+=tab('Uzun atlar (piyasa p<%10)',lambda p,x:p<0.10)
OUT+=tab('Orta (p %10-25)',lambda p,x:0.10<=p<0.25)
OUT+=tab('Favori (p>=%25)',lambda p,x:p>=0.25)
open(os.path.join(K,'veri','mesafe_sicil_testi.md'),'w',encoding='utf-8').write('\n'.join(OUT)+'\n')
print('\n'.join(OUT))
