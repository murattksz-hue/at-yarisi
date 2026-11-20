"""Bir atın bütün koşuları (veri/at_gecmisi/<yıl>/<gün>.csv.gz). Kullanım: at_bilgi.py "AT ADI" [son_n]"""
import sys,os,gzip,csv,io,glob
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ad=sys.argv[1].upper(); n=int(sys.argv[2]) if len(sys.argv)>2 else 15
R=[r for f in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','*','*.csv.gz'))) for r in csv.DictReader(io.TextIOWrapper(gzip.open(f),encoding='utf-8')) if r['at'].upper()==ad]
if not R: sys.exit('bulunamadı')
r0=R[-1]; print(f"{r0['at']} ({r0['yas']}) {r0['baba']} - {r0['anne']} ({r0['annebaba']}) | koşu {len(R)}, 1. {sum(r['sonuc']=='1' for r in R)}, ilk 3 {sum(r['sonuc'] in ('1','2','3') for r in R)}")
for r in R[-n:]: print(f"{r['tarih']} {r['hip']:9} {r['kosu']:>2}.k {r['tur'][:14]:14} {r['mesafe']}{r['pist'][:1]} {r['sonuc']:>2}/{r['kosan']:<2} gny {r['ganyan']:>6} AGF {r['agf']:>5} {r['jokey'][:16]:16} {r['kilo']}kg hp{r['hp']} {r['derece']}")
