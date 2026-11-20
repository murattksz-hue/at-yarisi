"""Atların koşu geçmişi veritabanı: her at, her koşu (gerçek ebayi sonuçları). Dosyalar: veri/at_gecmisi/<YYYY>/<YYYY-AA-GG>.csv.gz (git'te, gün başına bir dosya; yazılan gün bir daha değişmez).
Kullanım:
  at_gecmisi.py kur .gunluk/ebayi        → arşivdeki tüm sonuç JSON'larından baştan kurar
  at_gecmisi.py ekle YYYY-AA-GG [...]    → o günlerin sonuçlarını ebayi'den çekip ekler (tekrar yazmaz)
Satır: tarih, hipodrom, koşu no/saat/tür/grup/mesafe/pist, koşan sayısı, at kodu ve adı, yaş, baba, anne, anne babası,
jokey, antrenör, sahip, kilo, handikap puanı, start, takı, AGF, kesin ganyan, sıra, derece, fark. Koşmayanlar yazılmaz."""
import sys,os,glob,gzip,json,csv,io,urllib.request
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); DIR=os.path.join(K,'veri','at_gecmisi')
EBK={'ADANA':'Adana','IZMIR':'İzmir','ISTANBUL':'İstanbul','BURSA':'Bursa','ANKARA':'Ankara','SANLIURFA':'Şanlıurfa','ELAZIG':'Elazığ','DIYARBAKIR':'Diyarbakır','KOCAELI':'Kocaeli','ANTALYA':'Antalya'}
ALAN=['tarih','hip','kosu','saat','tur','grup','mesafe','pist','kosan','kod','at','yas','baba','anne','annebaba','jokey','antrenor','sahip','kilo','hp','start','taki','agf','ganyan','sonuc','derece','fark']
def satirlar(J,tarih,hip):
    for k in J.get('kosular',[]):
        A=[a for a in k.get('atlar',[]) if not a.get('KOSMAZ') and str(a.get('SONUC') or '').isdigit()]
        for a in A:
            yield dict(tarih=tarih,hip=hip,kosu=k.get('NO'),saat=k.get('SAAT'),tur=k.get('CINSDETAY_TR'),grup=k.get('GRUPKISA'),mesafe=k.get('MESAFE'),
                pist=k.get('PISTADI_TR'),kosan=len(A),kod=a.get('KOD'),at=a.get('AD'),yas=a.get('YAS'),baba=a.get('BABA'),anne=a.get('ANNE'),
                annebaba=a.get('ANNEBABA'),jokey=a.get('JOKEYADI'),antrenor=a.get('ANTRENORADI'),sahip=a.get('SAHIPADI'),kilo=a.get('KILO'),
                hp=a.get('HANDIKAP'),start=a.get('START'),taki=a.get('TAKI'),agf=a.get('AGF1'),ganyan=a.get('GANYAN'),sonuc=a.get('SONUC'),
                derece=a.get('DERECE'),fark=a.get('FARK'))
def gun_dosya(t): return os.path.join(DIR,t[:4],f"{t}.csv.gz")
def oku(t=None):
    F=[gun_dosya(t)] if t else sorted(glob.glob(os.path.join(DIR,'*','*.csv.gz'))); R=[]
    for f in F:
        if os.path.exists(f): R+=list(csv.DictReader(io.TextIOWrapper(gzip.open(f),encoding='utf-8')))
    return R
def yaz(R):
    G={}
    for r in R: G.setdefault(r['tarih'],[]).append(r)
    for t,L in G.items():
        L.sort(key=lambda r:(r['hip'],int(r['kosu'] or 0),int(r['sonuc'] or 99))); os.makedirs(os.path.dirname(gun_dosya(t)),exist_ok=True)
        with gzip.GzipFile(gun_dosya(t),'wb',mtime=0) as g:
            f=io.TextIOWrapper(g,encoding='utf-8',newline=''); w=csv.DictWriter(f,fieldnames=ALAN); w.writeheader(); w.writerows(L); f.flush(); f.detach()
    print(f"{len(G)} gün yazıldı: {len(R)} satır, {len({r['kod'] for r in R})} at, {len({(r['tarih'],r['hip'],r['kosu']) for r in R})} koşu")
def al(p):
    r=urllib.request.Request('https://ebayi.org/s/d/'+p,headers={'User-Agent':'Mozilla/5.0'})
    try: return json.loads(urllib.request.urlopen(r,timeout=40).read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        if e.code==404: return None
        raise
if sys.argv[1]=='kur':
    R=[]
    for f in sorted(glob.glob(sys.argv[2]+'/*.json.gz')):
        b=os.path.basename(f); t=f"{b[:4]}-{b[4:6]}-{b[6:8]}"; hip=EBK.get(b[9:-8],b[9:-8])
        R+=list(satirlar(json.load(gzip.open(f,'rt',encoding='utf-8')),t,hip))
    R=[{k:('' if v is None else v) for k,v in r.items()} for r in R]; yaz(R)
elif sys.argv[1]=='ekle':
    n=0
    for t in sys.argv[2:]:
        R=oku(t); var={(r['tarih'],r['hip'],r['kosu'],r['kod']) for r in R}; m=0
        d=t.replace('-','')
        for y in (al(f'sonuclar/{d}/yarislar.json') or []):
            if y.get('KEY') not in EBK: continue
            J=al(f"sonuclar/{d}/full/{y['KEY']}.json")
            for r in (satirlar(J,t,EBK[y['KEY']]) if J else []):
                r={k:('' if v is None else str(v)) for k,v in r.items()}
                if (r['tarih'],r['hip'],r['kosu'],r['kod']) not in var: R.append(r); var.add((r['tarih'],r['hip'],r['kosu'],r['kod'])); m+=1
        if m: yaz(R)
        n+=m
    print('eklenen satır:',n)
