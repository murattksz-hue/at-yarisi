"""Hata raporu: sürprizler neden geldi / bizim modeller neyi kaçırdı, büyük hatalar. Kullanım: hata_raporu.py [YYYY-AA-GG]  (tarih verilmezse bugün; gün sonu agf_plan.py çağırır)
Yalnızca OKUR: veri/kazanan_profil.csv, veri/canli_takip.csv, veri/canli_takip_agfsiz.csv. Yazar: veri/hata_raporu/<tarih>.md (yeni dosya).
Notlar kural tabanlıdır ('olası'), kesin neden değildir; örnek az. Segment taban oranları BILGI.md'den (surpriz_nerede: at sayısına göre ganyan>=10 sürpriz oranı)."""
import os,sys,csv,datetime,collections
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TR=datetime.timezone(datetime.timedelta(hours=3))
gun=sys.argv[1] if len(sys.argv)>1 else datetime.datetime.now(TR).date().isoformat()
def oku(p): return list(csv.DictReader(open(os.path.join(K,p),encoding='utf-8'))) if os.path.exists(os.path.join(K,p)) else []
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
KP=oku('veri/kazanan_profil.csv'); CT=oku('veri/canli_takip.csv'); CS=oku('veri/canli_takip_agfsiz.csv')
TABAN={'5-8':0.088,'9-11':0.154,'12-14':0.237,'15+':0.300}     # at sayısına göre ganyan>=10 sürpriz oranı (2024+, BILGI.md)
def bin_(n): return '5-8' if n<=8 else '9-11' if n<=11 else '12-14' if n<=14 else '15+'
CTd={(r['tarih'],r['hipodrom'],r['kosu']):r for r in CT}; CSd={(r['tarih'],r['hipodrom'],r['kosu']):r for r in CS}
def kisim(rows):
    n=len(rows);
    return n
gunler=sorted({r['tarih'] for r in KP})
L=[f'# Hata raporu — {gun}','','_Olası notlar kural tabanlıdır, kesin neden değildir; örnek az._','','## Günlük özet (19 Kasım\'dan beri)','',
   '| Gün | Koşu | İlk seçim doğru: AGF\'li | AGF\'siz | AGF favorisi | Sürpriz (ganyan≥10) |','|---|---|---|---|---|---|']
T=collections.Counter()
for g in gunler:
    ct=[r for r in CT if r['tarih']==g]; cs=[r for r in CS if r['tarih']==g]; kp=[r for r in KP if r['tarih']==g]
    if not ct: continue
    a=sum(r['model_1_bitis']=='1' for r in ct); s=sum(r['model_1_bitis']=='1' for r in cs); fv=sum(r['agf_favori_bitis']=='1' for r in ct); su=sum(r['surpriz']=='1' for r in kp)
    L.append(f'| {g} | {len(ct)} | {a} ({100*a/len(ct):.0f}%) | {s} ({100*s/max(len(cs),1):.0f}%) | {fv} ({100*fv/len(ct):.0f}%) | {su}/{len(kp)} |')
    T['n']+=len(ct);T['a']+=a;T['s']+=s;T['f']+=fv;T['su']+=su;T['kp']+=len(kp)
if T['n']: L.append(f"| **Toplam** | {T['n']} | {T['a']} ({100*T['a']/T['n']:.0f}%) | {T['s']} ({100*T['s']/T['n']:.0f}%) | {T['f']} ({100*T['f']/T['n']:.0f}%) | {T['su']}/{T['kp']} |")
L.append('')
# ---- (a) günün sürprizleri
kp=[r for r in KP if r['tarih']==gun]
S=[r for r in kp if r['surpriz']=='1' or (f(r['agf_son']) is not None and f(r['agf_son'])<10)]
L+=[f'## (a) {gun} sürprizleri ({len(S)}): ganyan ≥10 ya da kapanış AGF <%10','']
fiil=sum(r['surpriz']=='1' for r in kp)
if kp:
    beklenen=sum(TABAN[bin_(int(f(r['kosan']) or 9))] for r in kp)
    L+=[f"Segment kıyası: {len(kp)} koşuda ganyan≥10 sürpriz **{fiil}** (%{100*fiil/len(kp):.0f}); at sayısına göre taban oranlarla beklenen **{beklenen:.1f}** (%{100*beklenen/len(kp):.0f}).",'']
for r in sorted(S,key=lambda r:(r['hip'],int(r['kosu']))):
    nots=[]
    hs=f(r['hp_sira']); ms=f(r['model_agfli_sira']); ss=f(r['model_agfsiz_sira']); ao=f(r['agf_sabah']); ag=f(r['agf_son'])
    if hs is not None and hs<=3: nots.append(f'HP sırası {int(hs)}. (HP üstündeydi, piyasa küçümsemiş; geçmişte HP ilk 3 uzun atlar piyasadan fazla kazanıyor)')
    if hs is not None and hs>=6: nots.append(f'HP sırası {int(hs)}. (HP geride)')
    if ms is not None and ms>=5: nots.append(f"AGF'li model {int(ms)}. sıraya koymuş (kaçırdık)")
    if ss is not None and ms is not None and ss<ms-1: nots.append(f"AGF'siz model daha üstte ({int(ss)}.)")
    if r['jokey_degisti']=='1': nots.append('jokey değişti')
    if r['onceki_sira'] and f(r['onceki_sira']) and f(r['onceki_sira'])>=4: nots.append(f"önceki koşuda {int(f(r['onceki_sira']))}. bitirmişti")
    if f(r['mesafe_fark']) and abs(f(r['mesafe_fark']))>=400: nots.append(f"mesafe {f(r['mesafe_fark']):+.0f} m")
    if f(r['start']) is not None and f(r['start'])<=3: nots.append(f"iç kulvar (start {int(f(r['start']))})")
    if r['sessiz']=='1': nots.append('AGF sessiz (🤫)')
    if f(r['g30']) and f(r['g_son']) and f(r['g30'])/f(r['g_son'])>=1.4: nots.append(f"ganyan son 30 dk'da {f(r['g30']):g}→{f(r['g_son']):g} (💰)")
    L.append(f"- **{r['hip']} {r['kosu']}. koşu — {r['at']}**: ganyan {r['kesin']}, AGF {r['agf_son']}%, {r['kosan']} at, model {r['model_agfli_sira']}./{r['model_agfsiz_sira']}. | " + ('; '.join(nots) or 'belirgin işaret yok'))
if not S: L.append('Bu gün sürpriz kazanan yok ya da henüz kayıt yok.')
L.append('')
# ---- (b) büyük hatalar
L+=[f'## (b) {gun} büyük hatalar','','Kazananın AGF\'li model sırası ≥4 ya da ilk seçimimiz ≥5. bitmiş koşular:','']
H=[]
for r in CT:
    if r['tarih']!=gun: continue
    ms=f(r['kazanan_model_sira']); mb=f(r['model_1_bitis'])
    if (ms is not None and ms>=4) or (mb is not None and mb>=5): H.append(r)
for r in sorted(H,key=lambda r:(r['hipodrom'],int(r['kosu']))):
    L.append(f"- {r['hipodrom']} {r['kosu']}: kazanan **{r['kazanan']}** (modelin sırası {r['kazanan_model_sira']}, olasılık %{100*(f(r['kazanan_p']) or 0):.0f}) | ilk seçimimiz {r['model_1']} {r['model_1_bitis']}. bitti | AGF favorisi {r['agf_favori']} {r['agf_favori_bitis']}. bitti")
if not H: L.append('Büyük hata yok ya da henüz kayıt yok.')
n_g=sum(1 for r in CT if r['tarih']==gun)
L+=['',f'Büyük hata sayısı: **{len(H)}/{n_g}** koşu.','']
# ---- (c) toplam: hangi hata tipi
HT=[r for r in CT if f(r['kazanan_model_sira']) is not None and f(r['kazanan_model_sira'])>=4]
fav_kaybetti=[r for r in CT if f(r['agf_favori_bitis']) is not None and f(r['agf_favori_bitis'])>=2]
L+=['## (c) Toplam (19 Kasım\'dan beri)','',f"- Kazananın model sırası ≥4: {len(HT)}/{len(CT)} koşu (%{100*len(HT)/max(len(CT),1):.0f}).",
    f"- AGF favorisi kazanamadı: {len(fav_kaybetti)}/{len([r for r in CT if r['agf_favori_bitis']])} koşu.",
    f"- Sürpriz (ganyan≥10) toplam {T['su']}/{T['kp']} (%{100*T['su']/max(T['kp'],1):.0f}), beklenen taban ~%16.",'',
    '_Bu rapor yorum değil gözlemdir; sağlam sonuçlar için `BILGI.md` ve geçmiş verili testlere bak._']
od=os.path.join(K,'veri','hata_raporu'); os.makedirs(od,exist_ok=True)
open(os.path.join(od,f'{gun}.md'),'w',encoding='utf-8').write('\n'.join(L)+'\n')
print('yazıldı: veri/hata_raporu/%s.md | sürpriz %d | büyük hata %d/%d'%(gun,len(S),len(H),n_g))
