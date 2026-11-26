"""Sürprizlerin ortak noktaları: ganyanı ≥10 olan atlardan KAZANANLARI kaybedenlerden ayıran ne? (veri/at_gecmisi, 2024+, gerçek sonuçlar)
Beklenen = piyasa (kesin ganyandan normalize olasılık). A/E = gerçek galibiyet / beklenen. A/E>1 → piyasa bu grubu küçümsüyor.
Kalıcılık: ilk dönem (2024-01..2025-06) ve son dönem (2025-07..) ayrı A/E. Çıktı: veri/surpriz_ortak.json"""
import os,glob,gzip,csv,io,json,collections,math,datetime
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
R=collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','202[4-9]','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
BABA=collections.defaultdict(lambda:[0.0,0.0]); SON={}; S=collections.defaultdict(lambda:[0.0,0.0,0,0.0,0.0,0.0,0.0])  # W,E,n, W1,E1, W2,E2
def kova(ad,v): return f"{ad}: {v}"
for key in sorted(R,key=lambda k:(k[0],k[1],int(k[2] or 0))):
    A=R[key]; t=key[0]; G=[f(a['ganyan']) for a in A]
    ok=all(g and g>1 for g in G) and sum(a['sonuc']=='1' for a in A)==1
    if ok:
        q=[1/g for g in G]; s=sum(q); q=[x/s for x in q]
        AG=[f(a['agf']) or 0 for a in A]; agf_s={i:r+1 for r,i in enumerate(sorted(range(len(A)),key=lambda i:-AG[i]))}
        gny_s={i:r+1 for r,i in enumerate(sorted(range(len(A)),key=lambda i:G[i]))}
        HP=[f(a['hp']) or 0 for a in A]; hp_s={i:1+sum(1 for j in range(len(A)) if HP[j]>HP[i]) for i in range(len(A))}   # eşitlikte sıra yok (satırlar sonuca göre sıralı olduğundan sıralı sort bağı sızıntı yapıyordu, 26.11 düzeltme)
        for i,a in enumerate(A):
            if G[i]<10: continue
            p=SON.get(a['kod']); B=['TÜM gny≥10']
            if p:
                g=(datetime.date.fromisoformat(t)-datetime.date.fromisoformat(p['tarih'])).days
                B.append(kova('ara',('≤7g' if g<=7 else '8-14g' if g<=14 else '15-28g' if g<=28 else '29-60g' if g<=60 else '>60g')))
                B.append(kova('jokey',('değişti' if p['jokey']!=a['jokey'] else 'aynı')))
                md=(f(A[i].get('mesafe')) or 0)-(f(p['mesafe']) or 0); B.append(kova('mesafe',('kısaldı' if md<=-200 else 'uzadı' if md>=200 else 'aynı±100')))
                B.append(kova('pist',('değişti' if p['pist']!=a['pist'] else 'aynı'))); B.append(kova('hipodrom',('değişti' if p['hip']!=a['hip'] else 'aynı')))
                os_=f(p['sonuc']) or 99; B.append(kova('önceki sıra',('1-3' if os_<=3 else '4-6' if os_<=6 else '7+')))
                og=f(p['ganyan']) or 0; B.append(kova('önceki ganyan',('<5' if og<5 else '5-10' if og<10 else '10-30' if og<30 else '30+')))
                kd=(f(a['kilo']) or 0)-(f(p['kilo']) or 0); B.append(kova('kilo',('indi ≥2' if kd<=-2 else 'çıktı ≥2' if kd>=2 else 'aynı±1,5')))
                tk0=set((p['taki'] or '').split()); tk1=set((a['taki'] or '').split()); B.append(kova('takı',('yeni takı eklendi' if tk1-tk0 else 'takı çıkarıldı' if tk0-tk1 else 'aynı')))
                B.append(kova('tür',('aynı tür' if p['tur']==a['tur'] else 'tür değişti')))
            else: B.append('ara: ilk koşu (kayıtta önceki yok)')
            st=f(a['start']) or 0; B.append(kova('start',('1-3' if st<=3 else '4-7' if st<=7 else '8+')))
            if all(x>0 for x in AG): B.append(kova('AGF sırası vs ganyan sırası (AGFli koşu)',('AGF daha önde' if agf_s[i]<gny_s[i]-1 else 'AGF daha geride' if agf_s[i]>gny_s[i]+1 else 'benzer')))
            if all(x>0 for x in AG): B.append(kova('AGF payı / ganyan olasılığı',('AGF ≥2× ganyan' if AG[i]/100>=2*q[i] else 'AGF 1,3-2×' if AG[i]/100>=1.3*q[i] else 'AGF ≤0,7×' if AG[i]/100<=0.7*q[i] else 'yakın')))
            B.append(kova('HP sırası',('1-3' if hp_s[i]<=3 else '4-6' if hp_s[i]<=6 else '7+')))
            B.append(kova('yaş',(a['yas'] or '?').split()[0]))
            irk='Arap' if (a['grup'] or '').endswith('A') else 'İngiliz' if (a['grup'] or '').endswith('İ') else '?'
            B.append(kova('ırk',irk))
            bw,be=BABA[a['baba']]
            B.append(kova('babanın geçmiş A/E',('az veri (<20 beklenen yok)' if be<2 else '≥1,3' if bw/be>=1.3 else '1,0-1,3' if bw/be>=1.0 else '0,7-1,0' if bw/be>=0.7 else '<0,7')))
            B.append(kova('ganyan',('10-20' if G[i]<20 else '20-40' if G[i]<40 else '40+')))
            w=float(a['sonuc']=='1'); ilk=t<'2025-07'
            for b in B:
                x=S[b]; x[0]+=w; x[1]+=q[i]; x[2]+=1
                if ilk: x[3]+=w; x[4]+=q[i]
                else: x[5]+=w; x[6]+=q[i]
    if ok:
        for i,a in enumerate(A): BABA[a['baba']][0]+=a['sonuc']=='1'; BABA[a['baba']][1]+=q[i]
    for a in A: SON[a['kod']]=a
out={}
print(f"{'grup':48} {'at':>7} {'kazandı':>7} {'beklenen':>8} {'A/E':>5} {'z':>5} | ilk dön A/E | son dön A/E")
for b in sorted(S,key=lambda b:(b.split(':')[0],b)):
    W,E,n,W1,E1,W2,E2=S[b]
    if n<300: continue
    z=(W-E)/math.sqrt(E) if E>0 else 0; out[b]=dict(at=n,kazandi=int(W),beklenen=round(E,1),ae=round(W/E,2),z=round(z,2),ae_ilk=round(W1/E1,2) if E1 else None,ae_son=round(W2/E2,2) if E2 else None)
    isr='  ◀' if abs(z)>=2.5 and E1 and E2 and (W1/E1-1)*(W2/E2-1)>0 else ''
    print(f"{b:48} {n:7} {int(W):7} {E:8.1f} {W/E:5.2f} {z:5.1f} | {W1/E1 if E1 else 0:5.2f} | {W2/E2 if E2 else 0:5.2f}{isr}")
json.dump(out,open(os.path.join(K,'veri','surpriz_ortak.json'),'w'),ensure_ascii=False,indent=1)
