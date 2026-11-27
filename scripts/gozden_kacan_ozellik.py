"""Gözden kaçan kazananların (piyasa p<%10 olan atlar) genel özellikleri. Kullanım: gozden_kacan_ozellik.py   → veri/gozden_kacan_ozellik.md (elle ya da gün sonu)
Amaç: bu atları tahmin etmek değil, nasıl atlar olduklarını anlamak. Uzun atlar (kapanış ganyanından normalize piyasa olasılığı <%10) arasında her özellik değerinin payı, kazanma oranı ve piyasaya göre A/E'si (gerçek / beklenen), z ve iki yarıdaki A/E.
Kaynak: veri/at_gecmisi (2020–2026; özellikler yalnızca koşudan ÖNCEKİ geçmişten). Özellikler: yaş, cinsiyet, start, kilo (ortalamadan), HP (ortalamadan), son koşudan beri gün, jokey değişti, mesafe farkı, pist/hipodrom değişti, son koşudaki sıra, koşan at sayısı, çeşit, hipodrom, ay, ilk koşu."""
import os,glob,gzip,csv,io,re,math,collections
import numpy as np
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys; sys.path.insert(0,os.path.join(K,'scripts')); import kosu_tipi
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
R=collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','*','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
import datetime
seen={}   # kod -> görülen zeminler
last={}   # kod -> (tarih, jokey, mesafe, pist, hip, sira)
rows=[]   # (tarih, p, kazandı, {özellik: değer})
def d(t): return datetime.date.fromisoformat(t)
for key in sorted(R):
    rs=R[key]; g=[f(r['ganyan']) for r in rs]
    ok=len(rs)>=5 and not any(x is None or x<=1 for x in g) and sum(r['sonuc'].strip()=='1' for r in rs)==1
    if ok:
        iv=[1/x for x in g]; sv=sum(iv); n=len(rs); hp=[f(r['hp']) or 0 for r in rs]; kl=[f(r['kilo']) or 0 for r in rs]; hm=np.mean(hp); km=np.mean(kl)
        aile=kosu_tipi.aile(kosu_tipi.tur(rs[0]['tur'] or ''))
        for i,r in enumerate(rs):
            p=iv[i]/sv
            if p>=0.10: continue
            L=last.get(r['kod']); t=r['yas'].split(); ym=re.match(r'(\d+)y',t[0]) if t else None
            st=f(r['start']); F={}
            F['yaş']=('2' if ym and ym.group(1)=='2' else '3' if ym and ym.group(1)=='3' else '4' if ym and ym.group(1)=='4' else '5+' if ym else '?')
            F['cinsiyet']={'e':'genç erkek','a':'aygır','d':'genç dişi','k':'kısrak','g':'iğdiş'}.get(t[2] if len(t)>2 else '','?')
            F['start']=('iç (1-3)' if st and st<=3 else 'orta (4-7)' if st and st<=7 else 'dış (8+)' if st else '?')
            F['kilo (ortalamadan)']=('hafif (≤−1,5)' if kl[i]-km<=-1.5 else 'ağır (≥+1,5)' if kl[i]-km>=1.5 else 'orta')
            kr=1+sum(x>kl[i] for x in kl)   # sahada kilo sırası; eşitlikte sıra yok kuralı
            F['kilo sırası (sahada)']=('en ağır at' if kr==1 else 'üst 3 (2-3. ağır)' if kr<=3 else 'orta' if kr<=n-3 else 'alt 3 (en hafif 3)') if n>=8 else 'koşu <8 at'
            sv_=seen.get(r['kod']); pz=(r['pist'] or '').strip()
            F['zemin geçişi']=('ilk koşu (geçmiş yok)' if not sv_ else 'daha önce bu zeminde koşmuş' if pz in sv_ else 'ilk kez kuma (önce çim/sentetik)' if pz=='Kum' else 'ilk kez çime (önce kum/sentetik)' if pz=='Çim' else 'ilk kez sentetiğe' if pz=='Sentetik' else '?')
            F['HP (ortalamadan)']=('yüksek (≥+4)' if hp[i]-hm>=4 else 'düşük (≤−4)' if hp[i]-hm<=-4 else 'orta')
            F['koşan at sayısı']='5-8' if n<=8 else '9-11' if n<=11 else '12-14' if n<=14 else '15+'
            F['çeşit']=aile; F['hipodrom']=r['hip']; F['ay']=key[0][5:7]
            if L:
                gun=(d(key[0])-d(L[0])).days; F['son koşudan beri']='≤14 gün' if gun<=14 else '15-35 gün' if gun<=35 else '36-90 gün' if gun<=90 else '90+ gün'
                F['jokey']='aynı' if L[1]==r['jokey'] else 'değişti'
                md=f(r['mesafe'])-L[2] if f(r['mesafe']) and L[2] else None
                F['mesafe farkı']='?' if md is None else 'kısaldı (≤−200)' if md<=-200 else 'uzadı (≥+200)' if md>=200 else 'aynı (±<200)'
                F['pist/hipodrom']='aynı' if (L[3]==r['pist'] and L[4]==r['hip']) else 'değişti'
                F['son koşudaki sıra']='1-3' if L[5]<=3 else '4-6' if L[5]<=6 else '7+'
            else:
                F['son koşudan beri']='ilk koşu (geçmiş yok)'; F['jokey']='ilk koşu (geçmiş yok)'; F['mesafe farkı']='ilk koşu (geçmiş yok)'; F['pist/hipodrom']='ilk koşu (geçmiş yok)'; F['son koşudaki sıra']='ilk koşu (geçmiş yok)'
            rows.append((key[0],p,r['sonuc'].strip()=='1',F))
    for r in rs:
        if (r['pist'] or '').strip(): seen.setdefault(r['kod'],set()).add(r['pist'].strip())
        if r['sonuc'].strip().isdigit():
            last[r['kod']]=(key[0],r['jokey'],f(r['mesafe']),r['pist'],r['hip'],int(r['sonuc']))
tarihler=sorted({x[0] for x in rows}); orta=tarihler[len(tarihler)//2]
tum_n=len(rows); tum_w=sum(x[2] for x in rows); tum_e=sum(x[1] for x in rows)
S=collections.defaultdict(lambda:[0,0,0.0,0.0,0,0.0,0,0.0])
for t,p,w,F in rows:
    for k,v in F.items():
        a=S[(k,v)]; a[0]+=1; a[1]+=w; a[2]+=p; a[3]+=p*(1-p)
        if t<orta: a[4]+=w; a[5]+=p
        else: a[6]+=w; a[7]+=p
AE0=tum_w/tum_e
L=['# Gözden kaçan kazananların genel özellikleri','',f'Uzun atlar (piyasa olasılığı <%10): {tum_n:,} at-koşu, {tum_w} kazanan; genel A/E {tum_w/tum_e:.2f}. Kaynak at_gecmisi {tarihler[0]} – {tarihler[-1]}. Özellik değerine göre: payı (kazananlar içinde / tüm uzun atlar içinde), **göreli A/E** = (değerin A/E değeri) / (tüm uzun atların A/E değeri {AE0:.2f}); 1,00 = tipik uzun at, >1 = tipik uzun attan fazla kazanıyor. z: göreli farkın anlamlılığı, iki yarıda göreli A/E.','Amaç anlamak, tahmin etmek değil. Çok sayıda hücre bakıldığı için |z|≥2,5 olanların bir kısmı şans olabilir; iki yarıda da aynı yönde kalanlar daha güvenilir.','']
by=collections.defaultdict(list)
for (k,v),a in S.items(): by[k].append((v,a))
sig=[]
for k,lst in by.items():
    L+=[f'## {k}','','| Değer | Uzun at payı | Kazanan payı | göreli A/E | z | ilk yarı | ikinci yarı |','|---|---|---|---|---|---|---|']
    for v,a in sorted(lst,key=lambda x:-x[1][0]):
        if a[0]<150: continue
        ae=(a[1]/a[2] if a[2] else 0)/AE0; z=(a[1]-AE0*a[2])/math.sqrt(max(a[3]*AE0,1e-9)); a1=(a[4]/a[5] if a[5] else 0)/AE0; a2=(a[6]/a[7] if a[7] else 0)/AE0
        L.append(f'| {v} | %{100*a[0]/tum_n:.1f} | %{100*a[1]/max(tum_w,1):.1f} | {ae:.2f} | {z:+.1f} | {a1:.2f} | {a2:.2f} |')
        if abs(z)>=2.5 and ((a1-1)*(a2-1)>0): sig.append((abs(z),k,v,a[0],ae,z,a1,a2))
    L.append('')
sig.sort(reverse=True)
ust=['## Öne çıkanlar (tipik uzun ata göre; |z|≥2,5 ve iki yarıda aynı yönde)','','| Özellik | Değer | n | göreli A/E | z | ilk yarı | ikinci yarı |','|---|---|---|---|---|---|---|']+[f'| {k} | {v} | {n} | {ae:.2f} | {z:+.1f} | {a1:.2f} | {a2:.2f} |' for _,k,v,n,ae,z,a1,a2 in sig[:25]]+['']
open(os.path.join(K,'veri','gozden_kacan_ozellik.md'),'w',encoding='utf-8').write('\n'.join(L[:5]+ust+L[5:])+'\n')
print(tum_n,'at-koşu,',tum_w,'kazanan; genel uzun at A/E %.2f;'%AE0,len(sig),'öne çıkan'); print('\n'.join(ust[2:18]))
