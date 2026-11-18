"""Tek komutla günlük analiz. Kullanım: python3 scripts/gunluk.py GG.AA.YYYY [galop]
Türkiye hipodromlarının programını, CSV'sini (ve istenirse galopunu) indirir, v5 analizini çalıştırır.
Çıktı: analizler/YYYY-AA-GG_<hipodrom>.txt"""
import sys,os,re,subprocess,urllib.parse,datetime,json
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); g=datetime.datetime.strptime(sys.argv[1],'%d.%m.%Y').date()
galop=len(sys.argv)>2 and sys.argv[2]=='galop'
TR={'İstanbul','Ankara','İzmir','Bursa','Adana','Kocaeli','Elazığ','Diyarbakır','Şanlıurfa','Antalya'}
era='today' if g==datetime.date.today() else ('tomorrow' if g>datetime.date.today() else 'past')
tmp=os.path.join(K,'.gunluk',g.isoformat()); os.makedirs(tmp,exist_ok=True)
def get(u,out):
    r=subprocess.run(['curl','-sS','-f','--max-time','90','-o',out,u]); return r.returncode==0
tarih=urllib.parse.quote(g.strftime('%d/%m/%Y'),safe='')
ana=os.path.join(tmp,'ana.html'); get(f"https://www.tjk.org/TR/YarisSever/Info/Page/GunlukYarisProgrami?QueryParameter_Tarih={tarih}",ana)
t=open(ana,encoding='utf-8').read()
for sid,ad in re.findall(r'data-sehir-id="(\d+)" href="[^"]+">\s*([^<(]+?)\s*[(<]',t):
    if ad not in TR: continue
    enc=urllib.parse.quote(ad); h=os.path.join(tmp,ad+'.html'); c=os.path.join(tmp,ad+'.csv')
    get(f"https://www.tjk.org/TR/YarisSever/Info/Sehir/GunlukYarisProgrami?SehirId={sid}&QueryParameter_Tarih={tarih}&SehirAdi={enc}&Era={era}",h)
    if not get(f"https://medya-cdn.tjk.org/raporftp/TJKPDF/{g.year}/{g.isoformat()}/CSV/GunlukYarisProgrami/{g.strftime('%d.%m.%Y')}-{enc}-GunlukYarisProgrami-TR.csv",c):
        print(ad,': CSV alınamadı'); continue
    idm=os.path.join(tmp,ad+'_idman.json')
    if galop: subprocess.run([sys.executable,'-I',os.path.join(K,'scripts','idman.py'),h,idm,era])
    if not os.path.exists(idm): open(idm,'w').write('{}')
    hv=os.path.join(tmp,ad+'_hava.json')
    r_=subprocess.run([sys.executable,'-I',os.path.join(K,'scripts','hava.py'),'tahmin',g.strftime('%d.%m.%Y'),ad],capture_output=True,text=True)
    open(hv,'w').write(r_.stdout.strip().splitlines()[-1] if r_.returncode==0 and r_.stdout.strip() else '{}')
    out=os.path.join(K,'analizler',f"{g.isoformat()}_{ad}.txt"); os.makedirs(os.path.dirname(out),exist_ok=True)
    with open(out,'w') as f:
        subprocess.run([sys.executable,'-I',os.path.join(K,'scripts','analiz3.py'),h,c,os.path.join(K,'veri','model.json'),
            os.path.join(K,'veri','irk_zemin_mesafe_profil.json'),ad,idm,os.path.join(K,'veri','kosu_turu_jokey.json'),hv],stdout=f)
    print(ad,'->',out)
