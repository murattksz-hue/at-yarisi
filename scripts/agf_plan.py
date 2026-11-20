"""Koşu günü kayıt planı (kullanıcı kuralı, 19.11). agf_dongu.sh her dakika çağırır; zamanı gelen işi bir kez yapar.
  1) 09:15–10:30: ilk AGF tüm hipodromlar için kaydedilene kadar 10 dakikada bir agf_kayit (+ AGF gelince analiz/dondurma)
  2) 12:00: bir kontrol kaydı
  3) her koşudan 1 saat önce: bir kayıt
  4) her koşudan sonra (başlangıç + 15 dk): sonuç kontrolü (canli_takip → veri/canli_takip*.csv)
Durum: veri/plan/<tarih>.json. Koşu saatleri: ebayi program kosular/<HIP>.json. Çıkış kodu 3 = günün bütün işleri bitti."""
import sys,os,json,subprocess,datetime
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TZ=datetime.timezone(datetime.timedelta(hours=3)); simdi=datetime.datetime.fromisoformat(os.environ['PLAN_SIMDI']).replace(tzinfo=TZ) if os.environ.get('PLAN_SIMDI') else datetime.datetime.now(TZ); g=simdi.date()
DENEME=bool(os.environ.get('PLAN_DENEME'))   # deneme: işleri çalıştırmaz, yalnızca yazar
EBK={'IZMIR':'İzmir','ISTANBUL':'İstanbul','SANLIURFA':'Şanlıurfa','ELAZIG':'Elazığ','DIYARBAKIR':'Diyarbakır','ADANA':'Adana','BURSA':'Bursa','ANKARA':'Ankara','KOCAELI':'Kocaeli','ANTALYA':'Antalya'}
tmp=os.path.join(K,'veri','plan'); os.makedirs(tmp,exist_ok=True); PF=os.path.join(tmp,f'{g.isoformat()}.json')   # git'te: GitHub Actions çalıştırmaları arasında korunur
P=json.load(open(PF)) if os.path.exists(PF) else {}
def kaydet(): json.dump(P,open(PF,'w'),ensure_ascii=False,indent=0)
def eb(p):
    try: return json.loads(subprocess.run(['curl','-sS','-f','--max-time','60','-A','Mozilla/5.0','https://ebayi.org/s/d/'+p],capture_output=True).stdout.decode('utf-8'))
    except Exception: return None
ALINDI=[False]
def calis(*a):
    if a[0] in ('agf_kayit.py','agf_sonrasi_analiz.py'):
        if ALINDI[0]: return          # bu turda kayıt zaten alındı
        if a[0]=='agf_kayit.py': ALINDI[0]=True
    if DENEME: print('   [deneme] çalışırdı:',*a); return
    subprocess.run([sys.executable,'-I',os.path.join(K,'scripts',a[0]),*a[1:]])
if 'kosular' not in P:
    Y=eb(f"program/{g:%Y%m%d}/yarislar.json")
    if Y is None: sys.exit(0)
    P['kosular']={}
    for y in Y:
        if y.get('KEY') not in EBK: continue
        L=eb(f"program/{g:%Y%m%d}/kosular/{y['KEY']}.json") or []
        P['kosular'][EBK[y['KEY']]]={str(k['NO']):k['SAAT'] for k in L if k.get('SAAT')}
    P['yapilan']=[]; kaydet()
KS=P['kosular']
if not KS: sys.exit(3)   # bugün Türkiye'de koşu yok
yap=set(P['yapilan']); hm=simdi.strftime('%H:%M'); dk=lambda t:int(t[:2])*60+int(t[3:])
def is_(anahtar,fn):
    if anahtar in yap: return
    print(f"{hm} {anahtar}",flush=True); fn(); yap.add(anahtar); P['yapilan']=sorted(yap); kaydet()
# 1) sabah ilk AGF
kd=os.path.join(K,'veri','agf_kayit',g.isoformat())
ilk_tamam=all(os.path.exists(os.path.join(kd,f"ILK_{h}.csv")) for h in KS)
ilk_iki=ilk_tamam and all(os.path.exists(os.path.join(kd,f"ILK_{h}_ebayi.json")) for h in KS)   # iki kaynakta da ilk AGF alındı mı
if '09:15'<=hm<='10:30' and not ilk_iki and dk(hm)-P.get('son_sabah',-99)>=5:
    print(f"{hm} sabah AGF kontrolü",flush=True); P['son_sabah']=dk(hm); kaydet(); calis('agf_kayit.py'); ALINDI[0]=False; calis('agf_sonrasi_analiz.py')
# ilk AGF alındıktan sonra öğleye kadar 15 dk'da bir görüntü: TJK ile ebayi AGF'si ne zaman aynılaşıyor, sabah AGF nasıl oturuyor
if ilk_tamam and '09:15'<=hm<'12:00' and dk(hm)-P.get('son_sabah2',-99)>=15:
    P['son_sabah2']=dk(hm); kaydet(); calis('agf_kayit.py')
# ilk AGF'si kaydedilmiş ama tahmini dondurulmamış hipodrom varsa analiz 5 dakikada bir yeniden denenir
bekleyen=[h for h in KS if os.path.exists(os.path.join(kd,f"ILK_{h}.csv")) and not os.path.exists(os.path.join(K,'veri','tahminler',f"{g.isoformat()}_{h}.json"))]
if bekleyen and dk(hm)-P.get('son_analiz',-99)>=5:
    print(f"{hm} dondurulmamış: {', '.join(bekleyen)} → analiz",flush=True); P['son_analiz']=dk(hm); kaydet(); ALINDI[0]=False; calis('agf_sonrasi_analiz.py')
# 2) 12:00 kontrol
# Koşular erken başlarsa öğle kontrolü öne çekilir: min(12:00, ilk koşu − 90 dk); sabah ilk AGF alınmadan yapılmaz.
ilk_kosu=min(dk(t) for R in KS.values() for t in R.values()); ogle=min(12*60,ilk_kosu-90)
if dk(hm)>=ogle and (ilk_tamam or hm>'10:30'): is_('12:00 kontrol',lambda:(calis('agf_kayit.py'),ALINDI.__setitem__(0,False),calis('agf_sonrasi_analiz.py')))
# 3) koşudan 1 saat önce  4) koşudan sonra
for h,R in KS.items():
    for no,t in R.items():
        if dk(t)-60<=dk(hm)<dk(t): is_(f"{h} {no}. koşu -60dk kayıt",lambda:calis('agf_kayit.py'))
        # para girişi için koşuya yakın görüntüler (−30, −10, −3 dk); aynı dakikada birden çok iş tek kayıtla yapılır (ALINDI)
        for e in (30,10,3):
            if dk(t)-e<=dk(hm)<dk(t): is_(f"{h} {no}. koşu -{e}dk kayıt",lambda:calis('agf_kayit.py'))
        for e in (20,45):   # kazanan profili (sürpriz analizi); para takibinden sonra
            if dk(hm)>=dk(t)+e: is_(f"{h} {no}. koşu kazanan profili +{e}",lambda h=h,no=no:calis('kazanan_profil.py',g.isoformat(),h,no))
        for e in (15,40):   # sonuç geç gelirse ikinci deneme
            if dk(hm)>=dk(t)+e: is_(f"{h} {no}. koşu para takibi +{e}",lambda h=h,no=no:calis('para_takip.py',g.isoformat(),h,no))
        if dk(hm)>=dk(t)+15 and os.path.exists(os.path.join(K,'veri','tahminler',f"{g.isoformat()}_{h}.json")):
            is_(f"{h} {no}. koşu sonrası kontrol",lambda h=h:calis('canli_takip.py',g.strftime('%d.%m.%Y'),h))
son=max(dk(t) for R in KS.values() for t in R.values())
if dk(hm)>=son+15 and all(f"{h} {no}. koşu sonrası kontrol" in yap for h,R in KS.items() for no in R): sys.exit(3)
if dk(hm)>=son+120: sys.exit(3)
