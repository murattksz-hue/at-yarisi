"""Kullanıcının analizlerini MODEL ÖZELLİĞİ olarak üretir (veri/at_gecmisi, kronolojik, yalnızca o günden önceki koşular).
Anahtar 'YYYY-AA-GG_Hipodrom|koşuNo|AT ADI' → [sinif_fark, ilk_kez_hip, ilk_kez_mesafe, en_uzun, en_kisa, mesafe_degisim(m/100), soy_bant_ae(log), form_iyi_x_mesafe_yeni]
Soy-bant A/E da kronolojik (o güne kadarki babanın ırk+bant galibiyet/beklenen)."""
import os,glob,gzip,csv,io,collections,json,sys,math
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
def bant(m): return 'kısa' if m<=1400 else 'orta' if m<=1900 else 'uzun'
R=collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','*','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
GEC=collections.defaultdict(list); KAL={}; SOY=collections.defaultdict(lambda:[0.0,0.0]); OUT={}
gunler=sorted({k[0] for k in R}); bekle=[]
for g in gunler:
    for key in sorted([k for k in R if k[0]==g],key=lambda k:(k[1],int(k[2] or 0))):
        A=R[key]; hv=[f(a['hp']) for a in A if (f(a['hp']) or 0)>0]; kal=sum(hv)/len(hv) if len(hv)>=4 else None
        m=f(A[0]['mesafe']) or 0
        for a in A:
            P=GEC[a['kod']]; grp=a['grup'] or ''; irk='Arap' if grp.endswith('A') else 'İngiliz'
            sw,se=SOY[(irk,bant(m),a['baba'])]; soy=math.log((sw+2)/(se+2))
            if not P: OUT[f"{key[0]}_{key[1]}|{key[2]}|{a['at']}"]=[None,0,0,0,0,0,soy,0]; continue
            ms=[f(p['mesafe']) or 0 for p in P]; Pk=[KAL.get((p['tarih'],p['hip'],p['kosu'])) for p in P[-3:]]; Pk=[x for x in Pk if x]
            iyi=sum(1 for p in P[-3:] if (f(p['sonuc']) or 99)<=3)>=2; yeni=m not in ms
            OUT[f"{key[0]}_{key[1]}|{key[2]}|{a['at']}"]=[round(sum(Pk)/len(Pk)-kal,2) if (Pk and kal) else None, int(a['hip'] not in {p['hip'] for p in P}),
                int(yeni), int(m>max(ms)+100), int(m<min(ms)-100), round((m-ms[-1])/100,1), round(soy,3), int(iyi and yeni)]
        bekle.append((key,A,kal,m))
    for key,A,kal,m in bekle:   # gün bitince geçmişe ekle (aynı gün sızıntısı yok)
        n=len(A)
        for a in A:
            GEC[a['kod']].append(a); grp=a['grup'] or ''; irk='Arap' if grp.endswith('A') else 'İngiliz'
            SOY[(irk,bant(m),a['baba'])][0]+=a['sonuc']=='1'; SOY[(irk,bant(m),a['baba'])][1]+=1/n
        if kal: KAL[key]=kal
    bekle=[]
json.dump(OUT,open(sys.argv[1],'w'),ensure_ascii=False); print(len(OUT),'kayıt')
