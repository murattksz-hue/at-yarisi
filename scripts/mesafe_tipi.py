"""Atların, babaların ve anne babalarının MESAFE TİPİ (kısa / orta / uzun / karma): tüm sonuçlardan öğrenilir. Kullanım: mesafe_tipi.py [YYYY-AA-GG sınır tarihi, varsayılan: bugün]
Bantlar: kısa <=1400 m, orta 1500-1799 m, uzun >=1800 m. Kaynak: veri/at_gecmisi 2020+ (yalnızca sınır tarihinden ÖNCEKİ sonuçlar).
At tipi kuralı (>=3 start olan bantlar): ilk 3 oranı en yüksek bant, diğer bantların en iyisinden >=15 puan öndeyse o tip; tek banttan >=3 start varsa ilk 3 oranı >=%50 ise o tip, değilse belirsiz; belirgin fark yoksa karma; hiç bantta 3 start yoksa veri yetersiz.
Baba / anne babası tipi: yavruların bant başına piyasaya göre A/E (kazanma / kapanış ganyanından normalize beklenen), bant >=100 start; en yüksek A/E >=1,05 ve en düşük <=0,95 ise tip = en yüksek bant, aksi halde nötr.
Çıktılar: veri/mesafe_profil/at_tipi.json (2026'da koşmuş atlar: ad -> tip, baba, anne babası, bantlar), at_tipi.csv.gz (hepsi), baba_tipi.csv, annebaba_tipi.csv, mesafe_tipi.md. Yalnızca okur ve yeni dosya yazar."""
import os,sys,glob,gzip,csv,io,json,math,datetime,collections
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SINIR=sys.argv[1] if len(sys.argv)>1 else datetime.date.today().isoformat()
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
band=lambda m:'kisa' if m<=1400 else 'orta' if m<1800 else 'uzun'
B=('kisa','orta','uzun')
HZ=collections.defaultdict(lambda:{b:[0,0,0] for b in B})     # kod -> band -> [start, gal, ilk3]
ISIM={}; SOY={}; SON={}
SB=collections.defaultdict(lambda:{b:[0,0,0.0] for b in B}); SA=collections.defaultdict(lambda:{b:[0,0,0.0] for b in B})
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','*','*.csv.gz'))):
    R=collections.defaultdict(list)
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')):
        if r['tarih']<SINIR: R[(r['tarih'],r['hip'],r['kosu'])].append(r)
    for key,rs in R.items():
        m=int(f(rs[0]['mesafe']) or 0)
        if not m: continue
        b=band(m); g=[f(r['ganyan']) for r in rs]
        gecerli=len(rs)>=5 and not any(x is None or x<=1 for x in g) and sum(r['sonuc'].strip()=='1' for r in rs)==1
        sv=sum(1/x for x in g) if gecerli else None
        for i,r in enumerate(rs):
            s=r['sonuc'].strip()
            if not s.isdigit(): continue
            s=int(s); kd=r['kod']; z=HZ[kd][b]; z[0]+=1; z[1]+=s==1; z[2]+=s<=3
            ISIM[kd]=r['at'].strip(); SOY[kd]=((r['baba'] or '').strip(),(r['annebaba'] or '').strip()); SON[kd]=r['tarih']
            if gecerli:
                p=(1/g[i])/sv; w=s==1
                for tbl,ad in ((SB,SOY[kd][0]),(SA,SOY[kd][1])):
                    if ad: x=tbl[ad][b]; x[0]+=1; x[1]+=w; x[2]+=p
def at_tipi(d):
    ok={b:d[b] for b in B if d[b][0]>=3}
    if not ok: return 'veri yetersiz'
    t3={b:v[2]/v[0] for b,v in ok.items()}
    if len(ok)==1:
        b=next(iter(ok)); return b if t3[b]>=0.5 else 'belirsiz'
    sirali=sorted(t3.items(),key=lambda x:-x[1])
    return sirali[0][0] if sirali[0][1]-sirali[1][1]>=0.15 else 'karma'
def soy_tipi(d):
    r={b:(d[b][1]/d[b][2] if d[b][2]>0 and d[b][0]>=100 else None) for b in B}
    v={b:x for b,x in r.items() if x is not None}
    if len(v)<2: return 'veri yetersiz',r
    hi=max(v,key=v.get); lo=min(v,key=v.get)
    return (hi if v[hi]>=1.05 and v[lo]<=0.95 else 'nötr'),r
od=os.path.join(K,'veri','mesafe_profil'); os.makedirs(od,exist_ok=True)
aktif={}; tum=[]; sayim=collections.Counter(); sayim_aktif=collections.Counter()
for kd,d in HZ.items():
    t=at_tipi(d); sayim[t]+=1
    row=[kd,ISIM[kd],SOY[kd][0],SOY[kd][1],SON[kd],t]+[x for b in B for x in d[b]]
    tum.append(row)
    if SON[kd]>=f'{SINIR[:4]}-01-01':
        sayim_aktif[t]+=1; aktif[ISIM[kd]]={'tip':t,'baba':SOY[kd][0],'annebaba':SOY[kd][1],'bantlar':{b:d[b] for b in B}}
with gzip.open(os.path.join(od,'at_tipi.csv.gz'),'wt',encoding='utf-8',newline='') as fh:
    w=csv.writer(fh); w.writerow(['kod','at','baba','annebaba','son_start','tip']+[f'{b}_{x}' for b in B for x in ('start','gal','ilk3')]); w.writerows(tum)
json.dump(aktif,open(os.path.join(od,'at_tipi.json'),'w',encoding='utf-8'),ensure_ascii=False)
def yaz(tbl,ad,dosya):
    out=[]; stp=collections.Counter()
    for kisi,d in tbl.items():
        top=sum(d[b][0] for b in B)
        if top<300: continue
        t,r=soy_tipi(d); stp[t]+=1
        out.append([kisi,top,t]+[x for b in B for x in (d[b][0],round(r[b],2) if r[b] is not None else '')])
    out.sort(key=lambda x:-x[1])
    with open(os.path.join(od,dosya),'w',encoding='utf-8',newline='') as fh:
        w=csv.writer(fh); w.writerow([ad,'toplam_start','tip']+[f'{b}_{x}' for b in B for x in ('start','AE')]); w.writerows(out)
    return stp
sb=yaz(SB,'baba','baba_tipi.csv'); sa=yaz(SA,'anne_babasi','annebaba_tipi.csv')
L=['# Mesafe tipi (kısa <=1400 / orta 1500-1799 / uzun >=1800 m)','',f'Sınır tarihi {SINIR}, at_gecmisi 2020+. Atlar: {len(HZ):,}; {SINIR[:4]} yılında koşmuş: {sum(sayim_aktif.values()):,}.','',
   '| At tipi | Tüm atlar | Bu yıl koşan atlar |','|---|---|---|']+[f'| {t} | {sayim[t]:,} | {sayim_aktif[t]:,} |' for t in ('kisa','orta','uzun','karma','belirsiz','veri yetersiz')]
L+=['','| Soy tipi (>=300 yavru start, bant >=100 start) | Babalar | Anne babaları |','|---|---|---|']+[f'| {t} | {sb[t]} | {sa[t]} |' for t in ('kisa','orta','uzun','nötr','veri yetersiz')]
open(os.path.join(od,'mesafe_tipi.md'),'w',encoding='utf-8').write('\n'.join(L)+'\n')
print('\n'.join(L))
