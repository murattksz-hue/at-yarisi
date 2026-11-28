"""Geçmiş koşulardan hangi koşuların riskli olduğunu öğrenir: segment bazında (hipodrom, çeşit+ırk, mesafe bandı, at sayısı, zemin, kombinasyon) favori kazanma, gözden kaçan kazanan (ganyan>=10) ve kazananın piyasa ilk 3 dışından gelme oranları.
Kullanım: kosu_riski_gecmis.py [YYYY-AA-GG sınır tarihi, varsayılan bugün] -> veri/kosu_riski/gecmis_segment.json ve gecmis_segment.md
Kaynak: veri/at_gecmisi 2022+ (kapanış ganyanı, >=5 at, tek kazanan). Yalnızca sınır tarihinden ÖNCEKİ koşular. Yalnızca okur."""
import os,sys,glob,gzip,csv,io,json,collections,datetime
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(K,'scripts')); import kosu_tipi as KT
SINIR=sys.argv[1] if len(sys.argv)>1 else datetime.date.today().isoformat()
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
atb=lambda n:'5-8 at' if n<=8 else '9-11 at' if n<=11 else '12-14 at' if n<=14 else '15+ at'
S=collections.defaultdict(lambda:[0,0,0,0])   # n, favori kazandı, kazanan ganyan>=10, kazanan piyasa ilk 3 dışı
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','202[2-6]','*.csv.gz'))):
    R=collections.defaultdict(list)
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')):
        if r['tarih']<SINIR: R[(r['tarih'],r['hip'],r['kosu'])].append(r)
    for key,rs in R.items():
        g=[f(r['ganyan']) for r in rs]
        if len(rs)<5 or any(x is None or x<=1 for x in g) or sum(r['sonuc'].strip()=='1' for r in rs)!=1: continue
        wi=[i for i,r in enumerate(rs) if r['sonuc'].strip()=='1'][0]
        sira=1+sum(1 for x in g if x<g[wi]); fav=min(range(len(rs)),key=lambda i:g[i])==wi
        t=KT.tur(rs[0]['tur'] or ''); aile=KT.aile(t); irk='Arap' if (rs[0]['grup'] or '').strip().endswith('A') else 'İngiliz'
        mb=KT.mesafe_band(rs[0]['mesafe']); a=atb(len(rs)); h=rs[0]['hip']; z=(rs[0]['pist'] or '').strip()
        for k in (f'hip:{h}',f'cesit:{irk} {aile}',f'mesafe:{mb}',f'at:{a}',f'zemin:{z}',f'kombo:{h}|{irk} {aile}|{a}'):
            x=S[k]; x[0]+=1; x[1]+=fav; x[2]+=g[wi]>=10; x[3]+=sira>3
od=os.path.join(K,'veri','kosu_riski'); os.makedirs(od,exist_ok=True)
J={k:v for k,v in S.items() if v[0]>=50}
json.dump(J,open(os.path.join(od,'gecmis_segment.json'),'w',encoding='utf-8'),ensure_ascii=False)
tab=lambda ks:[f'| {k} | {S[k][0]:,} | %{100*S[k][1]/S[k][0]:.0f} | %{100*S[k][2]/S[k][0]:.0f} | %{100*S[k][3]/S[k][0]:.0f} |' for k in ks]
tum=[k for k in J if not k.startswith('kombo:')]; kombo=[k for k in J if k.startswith('kombo:') and J[k][0]>=150]
L=['# Geçmişten öğrenilen koşu riski (segment bazında)','',f'Kaynak at_gecmisi 2022–{SINIR}, ganyan ve tek kazanan tam koşular. Risk ölçüsü: **kazananın piyasa ilk 3 dışından gelmesi** ve **gözden kaçan kazanan (ganyan >=10)**. Genel ortalama bu iki ölçüde yaklaşık %31 ve %14.','',
   '## Tek boyutlu segmentler','','| Segment | Koşu | Favori kazandı | Ganyan>=10 kazanan | İlk 3 dışı kazanan |','|---|---|---|---|---|']+tab(sorted(tum,key=lambda k:-J[k][3]/J[k][0]))
L+=['','## En riskli kombinasyonlar (hipodrom | ırk çeşit | at sayısı, >=150 koşu)','','| Segment | Koşu | Favori kazandı | Ganyan>=10 kazanan | İlk 3 dışı kazanan |','|---|---|---|---|---|']+tab(sorted(kombo,key=lambda k:-J[k][3]/J[k][0])[:20])
L+=['','## En güvenli kombinasyonlar','','| Segment | Koşu | Favori kazandı | Ganyan>=10 kazanan | İlk 3 dışı kazanan |','|---|---|---|---|---|']+tab(sorted(kombo,key=lambda k:J[k][3]/J[k][0])[:15])
open(os.path.join(od,'gecmis_segment.md'),'w',encoding='utf-8').write('\n'.join(L)+'\n')
print('\n'.join(L[:30]))
