"""Son dakika piyasa özeti (koşudan ~10 dk önce). Kullanım: son_dakika_ozet.py <YYYY-AA-GG> <hipodrom> <koşu_no>   (agf_plan.py −10 dk adımında çağırır)
Girdiler (yalnızca okur): veri/tahminler/<tarih>_<hip>[_agfsiz].json (dondurulmuş v9), veri/agf_kayit/<tarih>/<hip>_<HHMM>UTC_ebayi.json (AGF1/AGF2/ganyan/koşmaz), veri/plan/<tarih>.json (koşu saati),
veri/tahminler_birlesik/<tarih>.json (varsa BİRLEŞİK). Çıktı: veri/son_dakika/<tarih>/<hip>_<koşu>.md (yeni dosya).
İçerik: at başına bizim olasılıklar (v9 AGF'li, AGF'siz, varsa BİRLEŞİK), piyasa (şimdi, AGF), sabaha ve −60 dk'ya göre AGF/ganyan değişimi, işaretler; bizim ve piyasanın favorisi farklı mı; para girişi olan atlar.
İşaretler (YALNIZCA bilgi, test edilmedi): 💰 ganyan −60 dk'ya göre >=%30 düştü (g60/g_şimdi >=1,4), 📈 AGF sabaha göre +%30 ve +3 puan, 📉 AGF sabaha göre −%30 ve −3 puan, ⚖ bizim olasılığımız piyasanın >=1,3 katı (değer adayı; kanıtlanmış değil)."""
import os,sys,re,json,glob,datetime,csv
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import kosu_tipi   # -I ile script dizini sys.path'te olmaz
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gun,hip,kno=sys.argv[1:4]
ak=lambda s:re.sub(r'\W','',str(s).upper())
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
def yukle(p):
    try: return json.load(open(p,encoding='utf-8'))
    except Exception: return None
plan=yukle(os.path.join(K,'veri','plan',f'{gun}.json')) or {'kosular':{}}
saat=plan['kosular'].get(hip,{}).get(kno)
if not saat: sys.exit('koşu saati yok')
tr=datetime.timezone(datetime.timedelta(hours=3)); t=datetime.datetime.fromisoformat(gun).replace(hour=int(saat[:2]),minute=int(saat[3:]),tzinfo=tr).astimezone(datetime.timezone.utc)
kd=os.path.join(K,'veri','agf_kayit',gun)
S=[]   # (utc dakika, yol)
for p in glob.glob(os.path.join(kd,f'{hip}_[0-9][0-9][0-9][0-9]UTC_ebayi.json')):
    b=os.path.basename(p)[len(hip)+1:len(hip)+5]; S.append((int(b[:2])*60+int(b[2:]),p))
S.sort(); tdk=t.hour*60+t.minute
if not S: sys.exit('eBayi görüntüsü yok')
def once(dk):
    c=[x for x in S if x[0]<=dk]; return c[-1] if c else None
simdi=S[-1]; s60=once(tdk-60) or S[0]; sab=None
tam=os.path.join(kd,f'TAM_{hip}_ebayi.json')
sabah=yukle(tam) if os.path.exists(tam) else (yukle(S[0][1]) if S else None)
try:   # TAM'dan 15 dk sonraki (AGF'nin oturduğu) ilk görüntü sabah referansı olsun; yoksa TAM
    iz=yukle(os.path.join(kd,'ilk_zaman.json')).get(hip,{}); ts=[int(iz[k][:2])*60+int(iz[k][2:4]) for k in ('tjk_tam','ebayi_tam') if k in iz]
    ref=[x for x in S if ts and x[0]>=max(ts)+15]
    if ref: sabah=yukle(ref[0][1])
except Exception: pass
def oku(snap,kno):
    d=(snap or {}).get(kno) or {}; out={}
    for a,v in d.items():
        if v[3]: continue
        x=[y for y in (f(v[0]),f(v[1])) if y is not None and y>0]
        out[ak(a)]=dict(ad=a,agf=(sum(x)/len(x) if x else None),gan=f(v[2]))
    return out
N=oku(yukle(simdi[1]),kno); O60=oku(yukle(s60[1]),kno); OS=oku(sabah,kno)
def kol(yol,kno):
    A=yukle(yol); 
    if not A: return {}
    for k in A:
        if str(k['kosu'])==kno: return {ak(a['ad']):a['p'] for a in k['atlar']}
    return {}
P9=kol(os.path.join(K,'veri','tahminler',f'{gun}_{hip}.json'),kno); P9s=kol(os.path.join(K,'veri','tahminler',f'{gun}_{hip}_agfsiz.json'),kno)
PB={}
B=yukle(os.path.join(K,'veri','tahminler_birlesik',f'{gun}.json'))
if B:
    for k in B.get('hipodromlar',{}).get(hip,{}).get('kosular',[]):
        if str(k['kosu'])==kno: PB={ak(a['ad']):a['p_birlesik'] for a in k['atlar']}
if not N: sys.exit('bu koşu için eBayi verisi yok')
agfs=[v['agf'] for v in N.values() if v['agf']]
piyasa={k:(v['agf']/sum(agfs) if (v['agf'] and sum(1 for x in N.values() if x['agf'])>=0.7*len(N)) else None) for k,v in N.items()}
if all(v is None for v in piyasa.values()):   # AGF yok (altılı dışı): ganyan
    inv={k:1/v['gan'] for k,v in N.items() if v['gan'] and 1<v['gan']<500}; s=sum(inv.values()) or 1
    piyasa={k:inv.get(k,0)/s for k in N}; kaynak='ganyan'
else: kaynak='AGF'
rows=[];flag={}
for k,v in sorted(N.items(),key=lambda kv:-(piyasa.get(kv[0]) or 0)):
    fl=[]
    g0=O60.get(k,{}).get('gan'); g1=v['gan']
    if g0 and g1 and g0/g1>=1.4: fl.append('💰')
    a0=OS.get(k,{}).get('agf'); a1=v['agf']
    if a0 and a1 and a1>=1.3*a0 and a1-a0>=3: fl.append('📈')
    if a0 and a1 and a1<=0.7*a0 and a0-a1>=3: fl.append('📉')
    ours=PB.get(k) or P9.get(k)
    if ours and piyasa.get(k) and ours>=1.3*piyasa[k] and piyasa[k]<0.25: fl.append('⚖')
    rows.append((k,v,fl))
def top(d): 
    d={k:x for k,x in d.items() if x is not None}; return max(d,key=d.get) if d else None
favs={'piyasa':top(piyasa),'v9 AGF\'li':top(P9),'v9 AGF\'siz':top(P9s),'BİRLEŞİK':top(PB)}
ad=lambda k:N[k]['ad'] if k in N else '—'
L=[f'# Son dakika özeti — {hip} {kno}. koşu ({saat}), {gun}','',f'Görüntü: {simdi[0]//60:02d}:{simdi[0]%60:02d} UTC (koşuya {tdk-simdi[0]} dk); karşılaştırma: −60 dk ≈ {s60[0]//60:02d}:{s60[0]%60:02d} UTC, sabah = TAM/ilk görüntü. Piyasa kaynağı: {kaynak}. İşaretler yalnızca bilgi, test edilmedi.','',
   '| At | Piyasa % | Sabah AGF | Ganyan −60 → şimdi | v9 AGF\'li % | v9 AGF\'siz % | BİRLEŞİK % | İşaret |','|---|---|---|---|---|---|---|---|']
fm=lambda x:'—' if x is None else f'{100*x:.0f}'
for k,v,fl in rows:
    g0=O60.get(k,{}).get('gan'); a0=OS.get(k,{}).get('agf'); g1=v['gan']
    gtxt=('—' if g0 is None else f'{g0:g}')+' → '+('—' if g1 is None else f'{g1:g}')
    L.append(f"| {v['ad'][:18]} | {fm(piyasa.get(k))} | {'—' if a0 is None else f'{a0:.1f}'} | {gtxt} | {fm(P9.get(k))} | {fm(P9s.get(k))} | {fm(PB.get(k))} | {' '.join(fl)} |")
L+=['','**Favoriler:** '+' · '.join(f"{n}: {ad(k) if k else '—'}" for n,k in favs.items()),'']
farkli={n for n,k in favs.items() if k and k!=favs['piyasa'] and favs['piyasa']}
L.append('Bizim kollarla piyasa favorisi **ayrışıyor**: '+', '.join(sorted(farkli)) if farkli else 'Bizim kollar piyasa favorisiyle **aynı atta birleşiyor** (ya da tahmin yok).')
_ps=sum(x for x in piyasa.values() if x is not None and x<0.10); _r='yüksek' if _ps>0.31 else 'orta' if _ps>0.198 else 'düşük'; _kl={'düşük':3,'orta':4,'yüksek':5}[_r]
_pr=PB or P9 or piyasa; _top=sorted(_pr,key=lambda k:-(_pr.get(k) or 0))[:_kl]
L.append(f"**Sürpriz riski: {_r}** (piyasada %10 altı atların payı %{100*_ps:.0f}) → liste {_kl} at: "+', '.join(ad(k) for k in _top)+'. Geçmişte bu uzunlukta kazanan listede ~%76–81.')
para=[ad(k) for k,v,fl in rows if '💰' in fl]
if para: L.append('Para girişi (💰): '+', '.join(para))
# koşu çeşidi: tarihsel taban oranları ve bizim canlı sicilimiz
try:
    _b=''
    for _k in (yukle(os.path.join(K,'veri','tahminler',f'{gun}_{hip}.json')) or []):
        if str(_k['kosu'])==kno: _b=_k.get('baslik','')
    ti=kosu_tipi.sinif(_b); KA=yukle(os.path.join(K,'veri','kosu_turu_analiz.json')) or {}
    L.append(f"**Koşu çeşidi:** {ti['irk']} {ti['tur']} · {ti['yas']} yaş · {ti['mesafe']} m {ti['pist']}")
    for ad,key in ((ti['tur'],f"{ti['irk']} {ti['tur']}"),(ti['aile'],f"{ti['irk']} {ti['aile']}")):
        h=KA.get(key)
        if h: L.append(f"- Tarihsel ({key}, 2024+): {h['kosu']} koşu, ort. {h['alan']:.1f} at, favori kazandı %{h['favori']:.0f}, ganyan≥10 sürpriz %{h['s10']:.0f}"); break
    KR=[r for r in csv.DictReader(open(os.path.join(K,'veri','kosu_tipi_kayit.csv'),encoding='utf-8'))] if os.path.exists(os.path.join(K,'veri','kosu_tipi_kayit.csv')) else []
    ay=[r for r in KR if r['irk']==ti['irk'] and r['tur']==ti['tur']] or [r for r in KR if r['irk']==ti['irk'] and r['aile']==ti['aile']]
    if ay:
        pc=lambda c:(lambda v:'—' if not v else f"%{100*sum(x=='1' for x in v)/len(v):.0f}")([r[c] for r in ay if r[c]!=''])
        L.append(f"- Canlı sicilimiz (aynı çeşit, {len(ay)} koşu{', gösterge değil' if len(ay)<10 else ''}): favori kazandı {pc('fav_kazandi')}, sürpriz %{100*sum(r['surpriz']=='1' for r in ay)/len(ay):.0f}, v9 AGF'li ilk tuttu {pc('v9_agfli_ilk')}, AGF'siz {pc('v9_agfsiz_ilk')}, BİRLEŞİK_10 {pc('b10_ilk')}")
    L.append('')
except Exception as e: print('koşu çeşidi bilgisi eklenemedi:',e,file=sys.stderr)
od=os.path.join(K,'veri','son_dakika',gun); os.makedirs(od,exist_ok=True)
open(os.path.join(od,f'{hip}_{kno}.md'),'w',encoding='utf-8').write('\n'.join(L)+'\n'); print('\n'.join(L))
