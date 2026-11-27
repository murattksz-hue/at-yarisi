"""Apranti jokey (kilo indirimi) ve kilo testleri. Kullanım: apranti_kilo_testi.py -> veri/apranti_kilo_testi.md
Apranti işareti: veri/arsiv/ebayi ham JSON'daki atlar[].APRANTIKILOINDIRIMI > 0 (at_gecmisi'nde yok). at_gecmisi ile (tarih, hip, koşu, at) üzerinden birleştirilir.
Ölçü: A/E = kazanma sayısı / kapanış ganyanından normalize beklenen (piyasa); z = (w-e)/sqrt(e). Salt okur; yazar: veri/apranti_kilo_testi.md"""
import os,glob,gzip,json,csv,io,math,collections,re
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
TR=str.maketrans('İıŞşĞğÜüÖöÇç','IiSsGgUuOoCc')
def norm(s): return s.translate(TR).upper().strip()
AP={}   # (tarih,HIP,kosu,AD) -> indirim
for fn in sorted(glob.glob(os.path.join(K,'veri','arsiv','ebayi','*.json.gz'))):
    b=os.path.basename(fn); m=re.match(r'(\d{8})_(.+)\.json\.gz',b)
    if not m: continue
    t=f'{m.group(1)[:4]}-{m.group(1)[4:6]}-{m.group(1)[6:]}'; hip=m.group(2)
    try: J=json.load(gzip.open(fn,'rt',encoding='utf-8'))
    except Exception: continue
    for k in J.get('kosular',[]):
        for a in k.get('atlar',[]):
            AP[(t,hip,str(k.get('NO')),norm(a.get('AD','')))]=f(a.get('APRANTIKILOINDIRIMI')) or 0
R=collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','202[2-6]','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
rows=[]   # dict'ler
eslesen=toplam=0
for key,rs in R.items():
    g=[f(r['ganyan']) for r in rs]; kl=[f(r['kilo']) for r in rs]
    if len(rs)<8 or any(x is None or x<=1 for x in g) or any(x is None or x<=0 for x in kl) or sum(r['sonuc'].strip()=='1' for r in rs)!=1: continue
    sv=sum(1/x for x in g); sp=max(kl)-min(kl); top=max(kl); n=len(rs)
    hand=(rs[0]['tur'] or '').lower().startswith('handikap')
    for i,r in enumerate(rs):
        toplam+=1
        ind=AP.get((key[0],norm(r['hip']),key[2],norm(r['at'])))
        if ind is not None: eslesen+=1
        rows.append(dict(hip=r['hip'],pist=(r['pist'] or '').strip(),hand=hand,p=(1/g[i])/sv,w=r['sonuc'].strip()=='1',g=g[i],ap=(ind or 0)>0,ind=ind or 0,known=ind is not None,
                         kilo=kl[i],fark=top-kl[i],sp=sp,kr=1+sum(x>kl[i] for x in kl),n=n,t=key[0]))
def tab(baslik,sat,filt=lambda r:True,gr=lambda r:'hepsi',sirala=None,minn=300):
    S=collections.defaultdict(lambda:[0,0.0,0,0,0.0,0,0.0])
    mid=sorted({r['t'] for r in rows})[len({r['t'] for r in rows})//2]
    for r in rows:
        if not filt(r): continue
        x=S[gr(r)];x[0]+=1;x[1]+=r['p'];x[2]+=r['w'];x[3]+=(r['w'] and r['g']>=10)
        if r['t']<mid: x[4]+=r['p'];x[5]+=r['w']
        else: x[6]+=r['p']
    L=[f'### {baslik}','','| Grup | At | Kazanan | A/E | z | ilk yarı A/E | ganyan≥10 kazanan |','|---|---|---|---|---|---|---|']
    for k in (sirala or sorted(S)):
        if k not in S: continue
        n,e,w,su,e1,w1,e2=S[k]
        if n<minn: continue
        a1=(w1/e1) if e1 else 0
        L.append(f'| {k} | {n:,} | {w:,} | {w/e:.2f} | {(w-e)/math.sqrt(e):+.1f} | {a1:.2f} | {su} |')
    return L+['']
OUT=['# Apranti jokey ve kilo testleri','',f'Kaynak: at_gecmisi 2022–2026 (≥8 at, ganyan ve kilo tam, tek kazanan) {toplam:,} at-koşu; ebayi apranti işaretiyle eşleşen {eslesen:,} (%{100*eslesen/max(toplam,1):.0f}). Eşleşmeyenler apranti testlerinde dışarıda bırakıldı.','',
     'A/E = kazanma / piyasadan beklenen (1 = piyasa doğru). Çoklu karşılaştırma: |z|<3 zayıf kanıt.','']
kn=lambda r:r['known']
OUT+=tab('1) Apranti ve normal jokey (tüm koşular)','',kn,lambda r:'apranti' if r['ap'] else 'normal',['apranti','normal'])
OUT+=tab('2) Apranti ve normal jokey — handikap / diğer','',kn,lambda r:('handikap ' if r['hand'] else 'diğer ')+('apranti' if r['ap'] else 'normal'))
OUT+=tab('3) Kilo indirimi büyüklüğüne göre (apranti)','',lambda r:kn(r) and r['ap'],lambda r:('≤2,5 kg' if r['ind']<=2.5 else '3-3,5 kg' if r['ind']<=3.5 else '4+ kg'),['≤2,5 kg','3-3,5 kg','4+ kg'],minn=200)
OUT+=tab('4) Kilo sıraları: apranti × sahanın en hafif 3 atı (handikap, fark ≥8 kg)','',lambda r:kn(r) and r['hand'] and r['sp']>=8,lambda r:('apranti' if r['ap'] else 'normal')+(' · en hafif 3' if r['kr']>r['n']-3 else ' · en ağır 3' if r['kr']<=3 else ' · orta'))
OUT+=tab('5) Kilo farkı ≥8 kg: en ağırdan kaç kg altında (tüm koşular)','',lambda r:r['sp']>=8,lambda r:'0 (en ağır)' if r['fark']==0 else '0,5-3' if r['fark']<=3 else '3,5-7' if r['fark']<=7 else '7,5+',['0 (en ağır)','0,5-3','3,5-7','7,5+'])
OUT+=tab('6) Aynı test yalnızca Bursa (handikap, fark ≥8 kg)','',lambda r:r['hip']=='Bursa' and r['hand'] and r['sp']>=8,lambda r:'0 (en ağır)' if r['fark']==0 else '0,5-3' if r['fark']<=3 else '3,5-7' if r['fark']<=7 else '7,5+',['0 (en ağır)','0,5-3','3,5-7','7,5+'],minn=150)
OUT+=tab('7) Bursa: apranti × normal (handikap)','',lambda r:kn(r) and r['hip']=='Bursa' and r['hand'],lambda r:'apranti' if r['ap'] else 'normal',['apranti','normal'],minn=100)
for pz in ('Kum','Çim'):
    OUT+=tab(f'8) {pz}: kilo farkı ≥8 kg, en ağırdan altı (handikap)','',lambda r,pz=pz:r['pist']==pz and r['hand'] and r['sp']>=8,lambda r:'0 (en ağır)' if r['fark']==0 else '0,5-3' if r['fark']<=3 else '3,5-7' if r['fark']<=7 else '7,5+',['0 (en ağır)','0,5-3','3,5-7','7,5+'])
OUT+=tab('9) Apranti: gözden kaçan kazanan (ganyan≥10) payı: at başına','',kn,lambda r:'apranti' if r['ap'] else 'normal',['apranti','normal'])
S={'ap':[0,0],'no':[0,0]}
for r in rows:
    if r['known']:
        k='ap' if r['ap'] else 'no';S[k][0]+=1;S[k][1]+=(r['w'] and r['g']>=10)
OUT+=[f"Gözden kaçan kazanan oranı (at başına): apranti %{100*S['ap'][1]/max(S['ap'][0],1):.2f} ({S['ap'][1]}/{S['ap'][0]:,}), normal %{100*S['no'][1]/max(S['no'][0],1):.2f} ({S['no'][1]}/{S['no'][0]:,}).",'']
open(os.path.join(K,'veri','apranti_kilo_testi.md'),'w',encoding='utf-8').write('\n'.join(OUT)+'\n')
print('\n'.join(OUT))
