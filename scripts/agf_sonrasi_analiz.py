"""AGF yayınlanınca analiz (kullanıcı kuralı: "AGF'ler yayınlanmadan başlama").
Kullanım: agf_sonrasi_analiz.py [GG.AA.YYYY]   (agf_dongu.sh her turda çağırır)
Bir hipodromun ilk AGF'si (veri/agf_kayit/<tarih>/ILK_<hip>.csv) kaydedildiyse ve o hipodromun tahmini henüz dondurulmadıysa:
  1) gunluk.py ile analiz (AGF'li model) → analizler/<tarih>_<hip>.txt, tahmin → veri/tahminler/<tarih>_<hip>.json
  2) aynı girdilerle AGF'siz model (AGFSIZ_ZORLA=1) → analizler/<tarih>_<hip>_agfsiz.txt, veri/tahminler/<tarih>_<hip>_agfsiz.json
AGF'si olmayan hipodrom için hiçbir şey yapılmaz. Altılıya girmeyen koşuların (AGF'si hiç olmayan) beklenmez. Bir kez dondurulan tahmin bir daha değiştirilmez."""
import sys,os,json,shutil,subprocess,datetime
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
g=datetime.datetime.strptime(sys.argv[1],'%d.%m.%Y').date() if len(sys.argv)>1 else datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).date()
kd=os.path.join(K,'veri','agf_kayit',g.isoformat()); td=os.path.join(K,'veri','tahminler'); tmp=os.path.join(K,'.gunluk',g.isoformat())
hazir=[f[4:-4] for f in sorted(os.listdir(kd)) if f.startswith('ILK_') and f.endswith('.csv')] if os.path.isdir(kd) else []
bekleyen=[h for h in hazir if not os.path.exists(os.path.join(td,f"{g.isoformat()}_{h}.json"))]
if not bekleyen: sys.exit(0)
print(f"{datetime.datetime.now():%H:%M} AGF yayınlandı, analiz: {', '.join(bekleyen)}",flush=True)
for h in bekleyen:   # eski (önceki çalıştırmadan kalma) çıktı kullanılmasın
    for e in (f"{h}_olasilik.json",f"{h}.csv",f"{h}.html"):
        if os.path.exists(os.path.join(tmp,e)): os.remove(os.path.join(tmp,e))
subprocess.run([sys.executable,'-I',os.path.join(K,'scripts','gunluk.py'),g.strftime('%d.%m.%Y')],stdout=subprocess.DEVNULL)
for h in bekleyen:
    js=os.path.join(tmp,f"{h}_olasilik.json")
    if not os.path.exists(js): print(h,': analiz çıktısı yok'); continue
    J=json.load(open(js,encoding='utf-8'))
    # altılıya girmeyen koşuların (ör. 1. koşu) AGF'si hiç olmaz: AGF'si olan koşular AGF'li modelle analiz edildiyse dondur
    import re as _re
    agfli_kosu=set()
    for l in open(os.path.join(tmp,f"{h}.csv"),encoding='utf-8-sig'):
        c=l.split(';'); m=_re.match(r'^(\d+)\. Kosu',c[0])
        if m: cur=m.group(1); continue
        if c[0].isdigit() and len(c)>10 and '%' in c[10]: agfli_kosu.add(cur)
    eksik=[r['kosu'] for r in J if str(r['kosu']) in agfli_kosu and r.get('model')!='agfli']
    if not agfli_kosu or eksik: print(h,': AGF henüz yok ya da analizde kullanılmadı, beklenecek',eksik); continue
    shutil.copy(js,os.path.join(td,f"{g.isoformat()}_{h}.json"))
    a=[os.path.join(tmp,f"{h}.html"),os.path.join(tmp,f"{h}.csv"),os.path.join(K,'veri','model.json'),os.path.join(K,'veri','irk_zemin_mesafe_profil.json'),h,
       os.path.join(tmp,f"{h}_idman.json"),os.path.join(K,'veri','kosu_turu_jokey.json'),os.path.join(tmp,f"{h}_hava.json")]
    js2=os.path.join(tmp,f"{h}_olasilik_agfsiz.json")
    with open(os.path.join(K,'analizler',f"{g.isoformat()}_{h}_agfsiz.txt"),'w') as f:
        subprocess.run([sys.executable,'-I',os.path.join(K,'scripts','analiz3.py'),*a],stdout=f,env=dict(os.environ,ANALIZ_JSON=js2,AGFSIZ_ZORLA='1'))
    if os.path.exists(js2): shutil.copy(js2,os.path.join(td,f"{g.isoformat()}_{h}_agfsiz.json"))
    print(h,': tahminler donduruldu (AGF\'li + AGF\'siz)',flush=True)
