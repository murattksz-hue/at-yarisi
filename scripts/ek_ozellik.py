"""Kullanıcının analizlerini MODEL ÖZELLİĞİ olarak üretir (veri/at_gecmisi, kronolojik, yalnızca o günden önceki koşular).
Anahtar 'YYYY-AA-GG_Hipodrom|koşuNo|AT ADI' → [sinif_fark, ilk_kez_hip, ilk_kez_mesafe, en_uzun, en_kisa, mesafe_degisim(m/100), soy_bant_ae(log), form_iyi_x_mesafe_yeni,
  annebaba_bant_ae(log), baba_hatti_bant_ae(log), grup_dusus (son 3 koşunun koşu türü seviyesi − bugünkü; tür seviyesi = o türün o güne kadarki ort. HP), kotu_form_x_grup_dusus]
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
ABS=collections.defaultdict(lambda:[0.0,0.0]); BHS=collections.defaultdict(lambda:[0.0,0.0]); TUR=collections.defaultdict(lambda:[0.0,0]); TK={}
def ad_(x): return (x or '').upper().split(' (')[0].strip()
BB={}
for A_ in R.values():
    for r_ in A_: BB.setdefault(ad_(r_['at']),ad_(r_['baba']))
_kat=os.path.join(K,'veri','aygir_katalog_2026.json')
if os.path.exists(_kat):
    for k_,v_ in json.load(open(_kat,encoding='utf-8')).items():
        if v_.get('baba') and v_['baba']!='None': BB.setdefault(ad_(k_),ad_(v_['baba']))
def tseviye(t): x=TUR.get(t); return x[0]/x[1] if x and x[1]>=5 else None
gunler=sorted({k[0] for k in R}); bekle=[]
for g in gunler:
    for key in sorted([k for k in R if k[0]==g],key=lambda k:(k[1],int(k[2] or 0))):
        A=R[key]; hv=[f(a['hp']) for a in A if (f(a['hp']) or 0)>0]; kal=sum(hv)/len(hv) if len(hv)>=4 else None
        m=f(A[0]['mesafe']) or 0
        for a in A:
            P=GEC[a['kod']]; grp=a['grup'] or ''; irk='Arap' if grp.endswith('A') else 'İngiliz'
            sw,se=SOY[(irk,bant(m),a['baba'])]; soy=math.log((sw+2)/(se+2))
            aw,ae_=ABS[(irk,bant(m),ad_(a['annebaba']))]; abs_=math.log((aw+2)/(ae_+2))
            bw,be=BHS[(irk,bant(m),BB.get(ad_(a['baba'])))]; bhs=math.log((bw+2)/(be+2))
            if not P: OUT[f"{key[0]}_{key[1]}|{key[2]}|{a['at']}"]=[None,0,0,0,0,0,soy,0,abs_,bhs,None,0]; continue
            ts=tseviye(a['tur']); tp=[tseviye(p['tur']) for p in P[-3:]]; tp=[x for x in tp if x]
            gd=(sum(tp)/len(tp)-ts) if (tp and ts) else None
            kotu=sum((f(p['sonuc']) or 99) for p in P[-3:])/len(P[-3:])>=5
            ms=[f(p['mesafe']) or 0 for p in P]; Pk=[KAL.get((p['tarih'],p['hip'],p['kosu'])) for p in P[-3:]]; Pk=[x for x in Pk if x]
            iyi=sum(1 for p in P[-3:] if (f(p['sonuc']) or 99)<=3)>=2; yeni=m not in ms
            OUT[f"{key[0]}_{key[1]}|{key[2]}|{a['at']}"]=[round(sum(Pk)/len(Pk)-kal,2) if (Pk and kal) else None, int(a['hip'] not in {p['hip'] for p in P}),
                int(yeni), int(m>max(ms)+100), int(m<min(ms)-100), round((m-ms[-1])/100,1), round(soy,3), int(iyi and yeni),
                round(abs_,3), round(bhs,3), round(gd,2) if gd is not None else None, round(gd,2) if (gd is not None and kotu and gd>0) else 0]
        bekle.append((key,A,kal,m))
    for key,A,kal,m in bekle:   # gün bitince geçmişe ekle (aynı gün sızıntısı yok)
        n=len(A)
        for a in A:
            GEC[a['kod']].append(a); grp=a['grup'] or ''; irk='Arap' if grp.endswith('A') else 'İngiliz'
            SOY[(irk,bant(m),a['baba'])][0]+=a['sonuc']=='1'; SOY[(irk,bant(m),a['baba'])][1]+=1/n
            ABS[(irk,bant(m),ad_(a['annebaba']))][0]+=a['sonuc']=='1'; ABS[(irk,bant(m),ad_(a['annebaba']))][1]+=1/n
            bbx=BB.get(ad_(a['baba']))
            if bbx: BHS[(irk,bant(m),bbx)][0]+=a['sonuc']=='1'; BHS[(irk,bant(m),bbx)][1]+=1/n
        if kal: KAL[key]=kal; TUR[A[0]['tur']][0]+=kal; TUR[A[0]['tur']][1]+=1
    bekle=[]
json.dump(OUT,open(sys.argv[1],'w'),ensure_ascii=False); print(len(OUT),'kayıt')
