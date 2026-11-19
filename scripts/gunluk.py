"""Tek komutla günlük analiz. Kullanım: python3 scripts/gunluk.py GG.AA.YYYY [galopsuz|tjkgalop]
Türkiye hipodromlarının programını, CSV'sini, hava tahminini ve galoplarını (pegadrom; tjkgalop ile TJK) indirir, analizi çalıştırır.
Çıktı: analizler/YYYY-AA-GG_<hipodrom>.txt"""
import sys,os,re,subprocess,urllib.parse,datetime,json
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); g=datetime.datetime.strptime(sys.argv[1],'%d.%m.%Y').date()
mod=sys.argv[2] if len(sys.argv)>2 else 'pegadrom'
if mod=='galop': mod='pegadrom'
TR={'İstanbul','Ankara','İzmir','Bursa','Adana','Kocaeli','Elazığ','Diyarbakır','Şanlıurfa','Antalya'}
era='today' if g==datetime.date.today() else ('tomorrow' if g>datetime.date.today() else 'past')
tmp=os.path.join(K,'.gunluk',g.isoformat()); os.makedirs(tmp,exist_ok=True)
def get(u,out):
    r=subprocess.run(['curl','-sS','-f','--max-time','90','-o',out,u],capture_output=True); return r.returncode==0
# 1) eksik sonuçları indir (son 10 gün) ve hız puanı tablosunu güncelle
SDIR=os.path.join(K,'veri','sonuc'); yeni=0
for d in range(1,11):
    t_=g-datetime.timedelta(days=d)
    for h_ in TR:
        fn=os.path.join(SDIR,f"{t_.isoformat()}_{h_}.csv")
        if os.path.exists(fn) or os.path.exists(os.path.join(K,'.gunluk','yok',os.path.basename(fn))): continue
        u=f"https://medya-cdn.tjk.org/raporftp/TJKPDF/{t_.year}/{t_.isoformat()}/CSV/GunlukYarisSonuclari/{t_.strftime('%d.%m.%Y')}-{urllib.parse.quote(h_)}-GunlukYarisSonuclari-TR.csv"
        if get(u,fn): yeni+=1
        else:
            if os.path.exists(fn): os.remove(fn)
            if t_<g-datetime.timedelta(days=1):   # dünden eskiyse yarış yok kabul et, bir daha sorma
                os.makedirs(os.path.join(K,'.gunluk','yok'),exist_ok=True); open(os.path.join(K,'.gunluk','yok',os.path.basename(fn)),'w').close()
if yeni:   # koşmayan atlar çıkarılmış temiz kopyadan tabloları güncelle
    subprocess.run([sys.executable,'-I',os.path.join(K,'scripts','sonuc_temizle.py')])
    TDIR=os.path.join(K,'veri','sonuc_temiz')
    subprocess.run([sys.executable,'-I',os.path.join(K,'scripts','hiz_tablosu.py'),TDIR,os.path.join(K,'veri','hiz_puani.json')])
    subprocess.run([sys.executable,'-I',os.path.join(K,'scripts','jokey_tablo.py'),TDIR,os.path.join(K,'veri','jokey_tablo.json')])
    subprocess.run([sys.executable,'-I',os.path.join(K,'scripts','maiden_analiz.py'),TDIR,os.path.join(K,'veri','maiden_analiz.json')],stdout=subprocess.DEVNULL)
    subprocess.run([sys.executable,'-I',os.path.join(K,'scripts','kosu_turu_analiz.py'),TDIR,os.path.join(K,'veri','kosu_turu_analiz.json')],stdout=subprocess.DEVNULL)
print('yeni sonuç dosyası:',yeni)
tarih=urllib.parse.quote(g.strftime('%d/%m/%Y'),safe='')
ana=os.path.join(tmp,'ana.html'); get(f"https://www.tjk.org/TR/YarisSever/Info/Page/GunlukYarisProgrami?QueryParameter_Tarih={tarih}",ana)
t=open(ana,encoding='utf-8').read()
for sid,ad in re.findall(r'data-sehir-id="(\d+)" href="[^"]+">\s*([^<(]+?)\s*[(<]',t):
    if ad not in TR: continue
    enc=urllib.parse.quote(ad); h=os.path.join(tmp,ad+'.html'); c=os.path.join(tmp,ad+'.csv')
    get(f"https://www.tjk.org/TR/YarisSever/Info/Sehir/GunlukYarisProgrami?SehirId={sid}&QueryParameter_Tarih={tarih}&SehirAdi={enc}&Era={era}",h)
    if not get(f"https://medya-cdn.tjk.org/raporftp/TJKPDF/{g.year}/{g.isoformat()}/CSV/GunlukYarisProgrami/{g.strftime('%d.%m.%Y')}-{enc}-GunlukYarisProgrami-TR.csv",c):
        print(ad,': CSV alınamadı'); continue
    subprocess.run([sys.executable,'-I',os.path.join(K,'scripts','soy_kayit.py'),h])   # soy: baba, anne, anne babası
    # AGF hareketi için saat damgalı kopya (gün içinde her çalıştırmada bir anlık görüntü)
    kd=os.path.join(K,'veri','agf_kayit',g.isoformat()); os.makedirs(kd,exist_ok=True)
    import shutil; shutil.copy(c,os.path.join(kd,f"{ad}_{datetime.datetime.utcnow().strftime('%H%M')}UTC.csv"))
    idm=os.path.join(tmp,ad+'_idman.json')
    nk=sum(1 for l in open(c,encoding='utf-8-sig') if re.match(r'^\d+\. Kosu',l))
    if mod=='pegadrom': subprocess.run([sys.executable,'-I',os.path.join(K,'scripts','galop_pegadrom.py'),g.isoformat(),ad,str(nk),idm])
    elif mod=='tjkgalop': subprocess.run([sys.executable,'-I',os.path.join(K,'scripts','idman.py'),h,idm,era])
    if not os.path.exists(idm): open(idm,'w').write('{}')
    hv=os.path.join(tmp,ad+'_hava.json')
    r_=subprocess.run([sys.executable,'-I',os.path.join(K,'scripts','hava.py'),'tahmin',g.strftime('%d.%m.%Y'),ad],capture_output=True,text=True)
    open(hv,'w').write(r_.stdout.strip().splitlines()[-1] if r_.returncode==0 and r_.stdout.strip() else '{}')
    out=os.path.join(K,'analizler',f"{g.isoformat()}_{ad}.txt"); os.makedirs(os.path.dirname(out),exist_ok=True)
    js=os.path.join(tmp,ad+'_olasilik.json')
    yeni_tur=subprocess.run([sys.executable,'-I',os.path.join(K,'scripts','kosu_turleri.py'),'kontrol',c,g.isoformat()],capture_output=True,text=True).stdout
    with open(out,'w') as f:
        if yeni_tur.strip(): f.write(yeni_tur+'\n'); print(yeni_tur.strip())
        f.flush()
        subprocess.run([sys.executable,'-I',os.path.join(K,'scripts','analiz3.py'),h,c,os.path.join(K,'veri','model.json'),
            os.path.join(K,'veri','irk_zemin_mesafe_profil.json'),ad,idm,os.path.join(K,'veri','kosu_turu_jokey.json'),hv],stdout=f,env=dict(os.environ,ANALIZ_JSON=js))
        f.flush()
        if os.path.exists(js): subprocess.run([sys.executable,'-I',os.path.join(K,'scripts','kupon.py'),js,'1','300'],stdout=f)
    print(ad,'->',out)
