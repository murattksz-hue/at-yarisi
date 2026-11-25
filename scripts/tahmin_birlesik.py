"""BİRLEŞİK günlük tahmin (test için, KOŞUDAN ÖNCE kaydedilir). Kullanım: tahmin_birlesik.py [YYYY-AA-GG]
Girdiler (yalnızca okur): veri/tahminler/<tarih>_<hip>[_agfsiz].json (dondurulmuş v9, DEĞİŞMEZ), veri/agf_kayit/<tarih>/<hip>_*UTC_ebayi.json (son görüntü: AGF1/AGF2/ganyan/koşmaz),
veri/plan/<tarih>.json (koşu saatleri), veri/at_gecmisi (baş-başa geçmişi, <tarih>'ten ÖNCE).
Çıktı: veri/tahminler_birlesik/<tarih>.json ve .md (yeni dosyalar; dondurulmuş tahminlere ve Actions CSV'lerine yazmaz).
Kollar (hepsi kaydedilir, akşam hepsi puanlanır): v9 AGF'li, v9 AGF'siz, piyasa (AGF; AGF yoksa ganyan^1,05), BİRLEŞİK = piyasa + b*baş-başa skoru (b=0,5).
BİRLEŞİK yalnızca TEST EDİLMİŞ bileşenleri kullanır (AGF kapanışta kalibre, A/E ~1,0; baş-başa lideri A/E 1,13 z +7,3, logit kazancı +0,0017). Ağırlıkları bu çalışmada ayarlanmadı."""
import os,sys,json,glob,gzip,csv,io,re,math,datetime,collections
import numpy as np
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TR=datetime.timezone(datetime.timedelta(hours=3))
gun=sys.argv[1] if len(sys.argv)>1 else datetime.datetime.now(TR).date().isoformat()
B_H2H=0.5; K_GANYAN=1.05
def anahtar(s): return re.sub(r'\W','',str(s).upper())
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
# ---- baş-başa geçmişi (gün'den önce)
H=collections.defaultdict(lambda:[0,0])
R=collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','202[4-9]','*.csv.gz'))):
    if os.path.basename(fn)[:10]>=gun: continue
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
for key in sorted(R):
    pos={anahtar(r['at']):int(r['sonuc']) for r in R[key] if r['sonuc'].strip().isdigit()}
    ks=list(pos)
    for a in ks:
        for b in ks:
            if a!=b:
                H[(a,b)][1]+=1
                if pos[a]<pos[b]: H[(a,b)][0]+=1
def h2h(adlar):
    n=len(adlar); ks=[anahtar(a) for a in adlar]; out=[]
    for i,a in enumerate(ks):
        t=0.0;c=0
        for j,b in enumerate(ks):
            if i!=j:
                w,m=H[(a,b)]
                if m>0: t+=(2*w-m)/(m+1); c+=1
        out.append((t/max(n-1,1),c))
    return out
def softmax(u):
    u=np.array(u,float); u=u-u.max(); e=np.exp(u); return e/e.sum()
plan=json.load(open(os.path.join(K,'veri','plan',f'{gun}.json'),encoding='utf-8')) if os.path.exists(os.path.join(K,'veri','plan',f'{gun}.json')) else {'kosular':{}}
SONUC={'tarih':gun,'olusturma_tr':datetime.datetime.now(TR).isoformat(timespec='seconds'),'surum':'birlesik_v1',
       'not':"Dondurulmuş v9 tahminleri DEĞİŞTİRİLMEDİ, burada aynen alınmıştır. Piyasa=AGF (son eBayi görüntüsü). Baş-başa: geçmiş yalnızca bugünden önceki koşulardan.",
       'ayarlar':{'b_h2h':B_H2H,'k_ganyan':K_GANYAN},'hipodromlar':{}}
MD=[f'# BİRLEŞİK tahmin — {gun}','',f"Oluşturma: {SONUC['olusturma_tr']} (koşulardan ÖNCE). Kollar: v9 AGF'li · v9 AGF'siz · piyasa (AGF) · **BİRLEŞİK** (piyasa + baş-başa, b={B_H2H}). Dondurulmuş v9 değişmedi.",'']
for yol in sorted(glob.glob(os.path.join(K,'veri','tahminler',f'{gun}_*.json'))):
    ad=os.path.basename(yol)[len(gun)+1:-5]
    if ad.endswith('_agfsiz'): continue
    hip=ad
    A=json.load(open(yol,encoding='utf-8')); ys=os.path.join(K,'veri','tahminler',f'{gun}_{hip}_agfsiz.json')
    S={x['kosu']:x for x in json.load(open(ys,encoding='utf-8'))} if os.path.exists(ys) else {}
    eb=sorted(glob.glob(os.path.join(K,'veri','agf_kayit',gun,f'{hip}_????UTC_ebayi.json')))
    E=json.load(open(eb[-1],encoding='utf-8')) if eb else {}
    SONUC['hipodromlar'][hip]={'ebayi_goruntu':os.path.basename(eb[-1]) if eb else None,'kosular':[]}
    sifir=float(np.mean([sum(1 for x in k['atlar'] if not x.get('agf'))/max(len(k['atlar']),1) for k in A]))   # dondurulmuş v9 AGF'li girdide AGF'si 0 olan at oranı
    SONUC['hipodromlar'][hip]['v9_agfli_sifir_agf_orani']=round(sifir,3)
    if sifir>0.05:
        SONUC['hipodromlar'][hip]['uyari']="v9 AGF'li kısmi AGF'yle dondurulmuş (atların %"+str(round(100*sifir))+"'inde AGF 0): bu kol zayıf güvenilir, değerlendirmede ayrı raporla."
        MD.append(f"> ⚠ {hip}: v9 AGF'li tahmin kısmi AGF'yle dondurulmuş (atların %{round(100*sifir)}'inde AGF 0). Bu kolu ayrı değerlendir.")
        MD.append('')
    MD+= [f'## {hip}','','| Koşu | Saat | BİRLEŞİK (ilk 3) | v9 AGF\'li | v9 AGF\'siz | piyasa | mutabakat | güven | sürpriz % | sürpriz adayı |','|---|---|---|---|---|---|---|---|---|---|']
    for k in A:
        no=str(k['kosu']); eK={anahtar(a):v for a,v in E.get(no,{}).items()}
        atlar=[a for a in k['atlar'] if not (eK.get(anahtar(a['ad'])) and eK[anahtar(a['ad'])][3])]   # koşmaz çıkar
        if len(atlar)<2: continue
        adlar=[a['ad'] for a in atlar]
        # piyasa: AGF (AGF1/AGF2 ortalaması), yoksa ganyan^k
        agf=[]; gan=[]
        for a in atlar:
            v=eK.get(anahtar(a['ad']),[None,None,None,False]); x=[y for y in (f(v[0]),f(v[1])) if y is not None and y>0]
            agf.append(sum(x)/len(x) if x else 0.0); gan.append(f(v[2]) if v[2] not in (None,'') else None)
        if sum(agf)>0 and sum(1 for x in agf if x>0)>=0.7*len(agf):
            pm=softmax(np.log(np.maximum(agf,0.05))); kaynak='AGF'
        else:
            g=[x if (x and 1<x<500) else 500.0 for x in gan]; pm=softmax(K_GANYAN*np.log(1/np.array(g))); kaynak='ganyan'
        sc=h2h(adlar); sk=np.array([s for s,_ in sc])
        pc=softmax(np.log(pm)+B_H2H*sk)
        def kol(src):
            if not src: return None
            d={anahtar(a['ad']):a['p'] for a in src['atlar']}; v=np.array([d.get(anahtar(x),0.0) for x in adlar],float)
            return v/v.sum() if v.sum()>0 else None
        p9=kol(k); p9s=kol(S.get(k['kosu']))
        arms={'birlesik':pc,'v9_agfli':p9,'v9_agfsiz':p9s,'piyasa':pm}
        top=lambda p:int(np.argmax(p)) if p is not None else None
        tops={n:top(p) for n,p in arms.items()}
        mut=sum(1 for n,t in tops.items() if t==tops['birlesik'])    # birleşik seçimle aynı seçen kol sayısı (kendisi dahil)
        guven='net' if pc.max()>=0.40 else 'orta' if pc.max()>=0.28 else 'düşük'
        p_sur=float(pm[pm<0.10].sum()); p_buyuk=float(pm[pm<0.05].sum())
        oran=pc/pm; aday=[i for i in np.argsort(-oran) if pm[i]<0.10 and pc[i]>=0.05 and oran[i]>=1.3][:2]
        satir={'kosu':int(no),'saat':(plan['kosular'].get(hip,{}).get(no)),'baslik':k['baslik'],'piyasa_kaynak':kaynak,
               'atlar':[{'no':atlar[i]['no'],'ad':adlar[i],'agf':round(agf[i],2),'ganyan':gan[i],'h2h':round(float(sk[i]),3),'h2h_rakip':sc[i][1],
                         'p_birlesik':round(float(pc[i]),4),'p_piyasa':round(float(pm[i]),4),
                         'p_v9_agfli':round(float(p9[i]),4) if p9 is not None else None,'p_v9_agfsiz':round(float(p9s[i]),4) if p9s is not None else None} for i in range(len(atlar))],
               'secim':{n:(atlar[t]['no'] if t is not None else None) for n,t in tops.items()},'mutabakat':mut,'guven':guven,
               'surpriz_olasiligi':round(p_sur,3),'buyuk_surpriz_olasiligi':round(p_buyuk,3),
               'surpriz_adaylari':[{'no':atlar[i]['no'],'ad':adlar[i],'p_birlesik':round(float(pc[i]),3),'p_piyasa':round(float(pm[i]),3)} for i in aday]}
        SONUC['hipodromlar'][hip]['kosular'].append(satir)
        t3=np.argsort(-pc)[:3]; fm=lambda i:f"#{atlar[i]['no']} {adlar[i][:11]} %{pc[i]*100:.0f}"
        MD.append(f"| {no} | {satir['saat'] or '?'} | {' · '.join(fm(i) for i in t3)} | #{atlar[tops['v9_agfli']]['no'] if tops['v9_agfli'] is not None else '—'} | #{atlar[tops['v9_agfsiz']]['no'] if tops['v9_agfsiz'] is not None else '—'} | #{atlar[tops['piyasa']]['no']} | {mut}/4 | {guven} | %{p_sur*100:.0f} | {', '.join('#'+atlar[i]['no']+' '+adlar[i][:10] for i in aday) or '—'} |")
    MD.append('')
MD+=["_Sürpriz % = piyasaya (AGF) göre kazananın AGF %10 altı bir attan çıkma olasılığı. Sürpriz adayı: AGF %10 altı, birleşik olasılığı piyasanın ≥1,3 katı. Mutabakat: dört koldan kaçı BİRLEŞİK'le aynı atı seçti._"]
od=os.path.join(K,'veri','tahminler_birlesik'); os.makedirs(od,exist_ok=True)
json.dump(SONUC,open(os.path.join(od,f'{gun}.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
open(os.path.join(od,f'{gun}.md'),'w',encoding='utf-8').write('\n'.join(MD)+'\n')
print('yazıldı: veri/tahminler_birlesik/%s.{json,md}'%gun, '|', sum(len(v['kosular']) for v in SONUC['hipodromlar'].values()),'koşu')
