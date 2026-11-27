"""Hipodrom galibi testi: at bu hipodromda (ve benzer mesafede) daha önce kazanmış mı, piyasanın ötesinde bilgi var mı? Kullanım: hipodrom_galibi_testi.py -> veri/hipodrom_galibi_testi.md
Özellikler yalnızca koşudan ÖNCEKİ geçmişten (kronolojik, sızıntı yok): hip_galip (bu hipodromda önceki galibiyet), hip_mes_galip (bu hipodromda ±200 m içinde galibiyet), mes_galip (herhangi bir hipodromda ±200 m galibiyet), hip_kosmus (bu hipodromda daha önce koşmuş).
Ölçü: A/E = kazanma / kapanış ganyanından normalize beklenen; z=(w-e)/sqrt(e). Yalnızca okur; yazar veri/hipodrom_galibi_testi.md"""
import os,glob,gzip,csv,io,math,collections
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
R=collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','*','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
win_hip=collections.defaultdict(list)   # kod -> [(hip,mesafe)]
ran_hip=collections.defaultdict(set)    # kod -> {hip}
win_all=collections.defaultdict(list)
S=collections.defaultdict(lambda:[0,0,0.0,0,0.0,0,0.0])   # grup -> n,w,e, uzun_n(p<.10) ... , ilk yarı
rows=[]
for key in sorted(R):
    rs=R[key]; g=[f(r['ganyan']) for r in rs]
    ok=key[0]>='2022-01-01' and len(rs)>=5 and not any(x is None or x<=1 for x in g) and sum(r['sonuc'].strip()=='1' for r in rs)==1
    if ok:
        sv=sum(1/x for x in g); m=f(rs[0]['mesafe']) or 0
        for r,x in zip(rs,g):
            kd=r['kod']; p=(1/x)/sv; w=r['sonuc'].strip()=='1'
            hw=[mm for h,mm in win_hip[kd] if h==key[1]]
            F={'hip_galip':bool(hw),'hip_mes_galip':any(abs(mm-m)<=200 for mm in hw),'mes_galip':any(abs(mm-m)<=200 for h,mm in win_hip[kd]),'hip_kosmus':key[1] in ran_hip[kd]}
            rows.append((key[0],p,w,x,F))
    for r in rs:
        kd=r['kod']; ran_hip[kd].add(key[1])
        if r['sonuc'].strip()=='1': win_hip[kd].append((key[1],f(r['mesafe']) or 0))
mid=sorted({t for t,*_ in rows})[len({t for t,*_ in rows})//2]
def tab(baslik,filt):
    L=[f'### {baslik}','','| Özellik | Değer | At | Kazanan | A/E | z | ilk yarı A/E | ganyan≥10 kazanan |','|---|---|---|---|---|---|---|---|']
    for ad in ('hip_galip','hip_mes_galip','mes_galip','hip_kosmus'):
        for val in (True,False):
            n=w=su=w1=0;e=e1=0.0
            for t,p,wi,x,F in rows:
                if not filt(p,x) or F[ad]!=val: continue
                n+=1;e+=p;w+=wi;su+=(wi and x>=10)
                if t<mid: e1+=p;w1+=wi
            if n>=200: L.append(f'| {ad} | {"evet" if val else "hayır"} | {n:,} | {w:,} | {w/e:.2f} | {(w-e)/math.sqrt(e):+.1f} | {(w1/e1) if e1 else 0:.2f} | {su} |')
    return L+['']
OUT=['# Hipodrom galibi testi','',f'at_gecmisi 2022–2026, {len(rows):,} at-koşu. Özellikler koşudan önceki geçmişten.','']
OUT+=tab('Tüm atlar',lambda p,x:True)
OUT+=tab('Uzun atlar (piyasa p<%10)',lambda p,x:p<0.10)
OUT+=tab('Orta (p %10-25)',lambda p,x:0.10<=p<0.25)
OUT+=tab('Favori (p>=%25)',lambda p,x:p>=0.25)
open(os.path.join(K,'veri','hipodrom_galibi_testi.md'),'w',encoding='utf-8').write('\n'.join(OUT)+'\n')
print('\n'.join(OUT))
