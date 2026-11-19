"""AGF anlık görüntüsü. Kullanım: agf_kayit.py [GG.AA.YYYY]
O günün Türkiye hipodromlarının program CSV'sini (AGF sütunu) çeker; AGF bir önceki görüntüden farklıysa
veri/agf_kayit/<tarih>/<hipodrom>_<SSDD>UTC.csv olarak saklar. AGF'nin ilk dolu olduğu görüntü ayrıca
veri/agf_kayit/<tarih>/ILK_<hipodrom>.csv olarak saklanır (kullanıcı gözlemi: sabah ilk AGF daha isabetli olabilir; test edilecek)."""
import sys,os,re,glob,subprocess,urllib.parse,datetime,hashlib
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
g=datetime.datetime.strptime(sys.argv[1],'%d.%m.%Y').date() if len(sys.argv)>1 else datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).date()
TR={'İstanbul','Ankara','İzmir','Bursa','Adana','Kocaeli','Elazığ','Diyarbakır','Şanlıurfa','Antalya'}
tq=urllib.parse.quote(g.strftime('%d/%m/%Y'),safe='')
ana=subprocess.run(['curl','-sS','--max-time','90',f"https://www.tjk.org/TR/YarisSever/Info/Page/GunlukYarisProgrami?QueryParameter_Tarih={tq}"],capture_output=True).stdout.decode('utf-8','replace')
hips=[a for _,a in re.findall(r'data-sehir-id="(\d+)" href="[^"]+">\s*([^<(]+?)\s*[(<]',ana) if a in TR]
kd=os.path.join(K,'veri','agf_kayit',g.isoformat()); os.makedirs(kd,exist_ok=True); saat=datetime.datetime.now(datetime.timezone.utc).strftime('%H%M')
def agf_kismi(b):   # yalnızca at satırlarının AGF sütunu (değişim karşılaştırması için)
    return [l.split(';')[10] for l in b.decode('utf-8-sig','replace').splitlines() if re.match(r'^\d+;',l) and len(l.split(';'))>10]
for h in hips:
    u=f"https://medya-cdn.tjk.org/raporftp/TJKPDF/{g.year}/{g.isoformat()}/CSV/GunlukYarisProgrami/{g.strftime('%d.%m.%Y')}-{urllib.parse.quote(h)}-GunlukYarisProgrami-TR.csv"
    b=subprocess.run(['curl','-sS','-f','--max-time','90',u],capture_output=True).stdout
    if not b: print(h,': CSV yok'); continue
    a=agf_kismi(b); dolu=sum(bool(re.match(r'%[\d.]+',x)) for x in a)
    onceki=sorted(f for f in glob.glob(os.path.join(kd,f"{h}_*UTC.csv")))
    if onceki and agf_kismi(open(onceki[-1],'rb').read())==a: print(f"{h}: AGF değişmemiş ({dolu}/{len(a)} at dolu)"); continue
    open(os.path.join(kd,f"{h}_{saat}UTC.csv"),'wb').write(b)
    ilk=os.path.join(kd,f"ILK_{h}.csv")
    if dolu>0 and not os.path.exists(ilk): open(ilk,'wb').write(b); print(f"{h}: İLK AGF kaydedildi ({saat} UTC, {dolu}/{len(a)} at)")
    else: print(f"{h}: yeni görüntü {saat} UTC ({dolu}/{len(a)} at dolu)")
