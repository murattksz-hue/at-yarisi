"""ebayi.org (TJK'nın resmî internet bayisi, robots.txt: Allow /) sonuç JSON'larını indirir.
Kullanım: ebayi_indir.py hedef_dizin baslangic(YYYY-MM-DD) [bitis]
Her gün/hipodrom için: <hedef>/<YYYYMMDD>_<KEY>.json.gz (sonuclar/full: koşular, atlar, AGF, ganyan, sonuç, satış bedeli, anne babası, KGS, son 6, kodlar).
Yalnızca Türkiye hipodromları. İstekler arası 1 sn bekler; var olan dosyayı atlar; yarış olmayan günü .yok ile işaretler."""
import sys,os,json,gzip,time,datetime,urllib.request
TR={'ADANA','IZMIR','ISTANBUL','BURSA','ANKARA','SANLIURFA','ELAZIG','DIYARBAKIR','KOCAELI','ANTALYA'}
B='https://ebayi.org/s/d/'
def al(p):
    r=urllib.request.Request(B+p,headers={'User-Agent':'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(r,timeout=40) as f: return json.loads(f.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        if e.code==404: return None
        raise
hedef=sys.argv[1]; os.makedirs(hedef,exist_ok=True)
g=datetime.date.fromisoformat(sys.argv[2]); son=datetime.date.fromisoformat(sys.argv[3]) if len(sys.argv)>3 else datetime.date.today()-datetime.timedelta(days=1)
while g<=son:
    d=g.strftime('%Y%m%d'); yok=os.path.join(hedef,d+'.yok')
    if not os.path.exists(yok) and not any(f.startswith(d+'_') for f in os.listdir(hedef)):
        for deneme in range(4):
            try:
                Y=al(f'sonuclar/{d}/yarislar.json'); time.sleep(1); n=0
                for y in (Y or []):
                    if y.get('KEY') not in TR: continue
                    J=al(f"sonuclar/{d}/full/{y['KEY']}.json"); time.sleep(1)
                    if J: json.dump(J,gzip.open(os.path.join(hedef,f"{d}_{y['KEY']}.json.gz"),'wt',encoding='utf-8'),ensure_ascii=False); n+=1
                if n==0: open(yok,'w').close()
                print(d,n,flush=True); break
            except Exception as e:
                print(d,'hata',e,flush=True); time.sleep(10*(deneme+1))
    g+=datetime.timedelta(days=1)
