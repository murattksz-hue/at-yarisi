"""Model AGF favorisinden gerçekten iyi mi? Koşu-eşli bootstrap ile %95 güven aralığı.
Kullanım: guven_araligi.py            (veri/canli_takip.csv ve veri/canli_takip_agfsiz.csv'yi okur)
Ölçüler (koşu başına, model - AGF):
  1) log kaybı farkı: log_model - log_agf   (negatif = model daha iyi)
  2) ilk tercih isabeti farkı: model ilk seçimi 1. bitti mi - AGF favorisi 1. bitti mi (pozitif = model daha iyi)
Aralık sıfırı içeriyorsa fark gürültüdür; "iyi" demek için aralığın tamamı sıfırın bir yanında olmalı.
Çıktı: ekrana ve veri/agf_kayit/GUVEN_ARALIGI.md (Actions bu klasörü commit'ler). Yalnızca okur, mevcut CSV'lere yazmaz."""
import os,csv,random,statistics
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def sayi(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
def boot(x,n=5000,seed=1):
    r=random.Random(seed); m=len(x)
    o=sorted(sum(x[r.randrange(m)] for _ in range(m))/m for _ in range(n))
    return o[int(0.025*n)],o[int(0.975*n)]
def yorum(lo,hi,iyi_negatif):
    if lo<=0<=hi: return 'fark yok (aralık sıfırı içeriyor)'
    model_iyi=(hi<0) if iyi_negatif else (lo>0)
    return 'model daha iyi' if model_iyi else 'AGF daha iyi'
L=['# Model - AGF güven aralığı (koşu-eşli bootstrap, %95)','']
for ad in ('canli_takip.csv','canli_takip_agfsiz.csv'):
    p=os.path.join(K,'veri',ad)
    if not os.path.exists(p): continue
    R=list(csv.DictReader(open(p,encoding='utf-8')))
    ll=[sayi(r['log_model'])-sayi(r['log_agf']) for r in R if sayi(r.get('log_model')) is not None and sayi(r.get('log_agf')) is not None]
    hit=[(sayi(r['model_1_bitis'])==1)-(sayi(r['agf_favori_bitis'])==1) for r in R if sayi(r.get('model_1_bitis')) is not None and sayi(r.get('agf_favori_bitis')) is not None]
    L.append(f'## {ad} ({len(R)} koşu)'); L.append('')
    for isim,x,neg in (('log kaybı farkı (negatif = model iyi)',ll,True),('ilk tercih isabeti farkı (pozitif = model iyi)',hit,False)):
        if len(x)<10: L.append(f'- {isim}: yetersiz veri ({len(x)} koşu)'); continue
        lo,hi=boot(x); L.append(f'- {isim}: ort {statistics.mean(x):+.4f}  %95 aralık [{lo:+.4f}, {hi:+.4f}]  → {yorum(lo,hi,neg)}  (n={len(x)})')
    L.append('')
L.append('Not: az koşuyla aralık geniş çıkar; bu doğal. Koşu sayısı arttıkça daralır.')
s='\n'.join(L)+'\n'; print(s)
open(os.path.join(K,'veri','agf_kayit','GUVEN_ARALIGI.md'),'w',encoding='utf-8').write(s)
