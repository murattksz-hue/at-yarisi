"""AGF yayınlanınca analiz (kullanıcı kuralı: "AGF'ler yayınlanmadan başlama").
Kullanım: agf_sonrasi_analiz.py [GG.AA.YYYY]   (agf_dongu.sh her turda çağırır)
Bir hipodromun ilk AGF'si (veri/agf_kayit/<tarih>/ILK_<hip>.csv) kaydedildiyse ve o hipodromun tahmini henüz dondurulmadıysa:
  1) gunluk.py ile analiz (AGF'li model) → analizler/<tarih>_<hip>.txt, tahmin → veri/tahminler/<tarih>_<hip>.json
  2) aynı girdilerle AGF'siz model (AGFSIZ_ZORLA=1) → analizler/<tarih>_<hip>_agfsiz.txt, veri/tahminler/<tarih>_<hip>_agfsiz.json
AGF'si olmayan hipodrom için hiçbir şey yapılmaz. Bir kez dondurulan tahmin bir daha değiştirilmez."""
import sys,os,json,shutil,subprocess,datetime
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
g=datetime.datetime.strptime(sys.argv[1],'%d.%m.%Y').date() if len(sys.argv)>1 else datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).date()
kd=os.path.join(K,'veri','agf_kayit',g.isoformat()); td=os.path.join(K,'veri','tahminler'); tmp=os.path.join(K,'.gunluk',g.isoformat())
hazir=[f[4:-4] for f in sorted(os.listdir(kd)) if f.startswith('ILK_') and f.endswith('.csv')] if os.path.isdir(kd) else []
bekleyen=[h for h in hazir if not os.path.exists(os.path.join(td,f"{g.isoformat()}_{h}.json"))]
if not bekleyen: sys.exit(0)
print(f"{datetime.datetime.now():%H:%M} AGF yayınlandı, analiz: {', '.join(bekleyen)}",flush=True)
subprocess.run([sys.executable,'-I',os.path.join(K,'scripts','gunluk.py'),g.strftime('%d.%m.%Y')],stdout=subprocess.DEVNULL)
for h in bekleyen:
    js=os.path.join(tmp,f"{h}_olasilik.json")
    if not os.path.exists(js): print(h,': analiz çıktısı yok'); continue
    J=json.load(open(js,encoding='utf-8'))
    if not J or any(r.get('model')!='agfli' for r in J): print(h,': AGF henüz tam değil, beklenecek'); continue
    shutil.copy(js,os.path.join(td,f"{g.isoformat()}_{h}.json"))
    a=[os.path.join(tmp,f"{h}.html"),os.path.join(tmp,f"{h}.csv"),os.path.join(K,'veri','model.json'),os.path.join(K,'veri','irk_zemin_mesafe_profil.json'),h,
       os.path.join(tmp,f"{h}_idman.json"),os.path.join(K,'veri','kosu_turu_jokey.json'),os.path.join(tmp,f"{h}_hava.json")]
    js2=os.path.join(tmp,f"{h}_olasilik_agfsiz.json")
    with open(os.path.join(K,'analizler',f"{g.isoformat()}_{h}_agfsiz.txt"),'w') as f:
        subprocess.run([sys.executable,'-I',os.path.join(K,'scripts','analiz3.py'),*a],stdout=f,env=dict(os.environ,ANALIZ_JSON=js2,AGFSIZ_ZORLA='1'))
    if os.path.exists(js2): shutil.copy(js2,os.path.join(td,f"{g.isoformat()}_{h}_agfsiz.json"))
    print(h,': tahminler donduruldu (AGF\'li + AGF\'siz)',flush=True)
