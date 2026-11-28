"""Son dakika piyasa özeti (koşudan ~10 dk önce). Kullanım: son_dakika_ozet.py <YYYY-AA-GG> <hipodrom> <koşu_no>   (agf_plan.py −10 dk adımında çağırır)
Girdiler (yalnızca okur): veri/tahminler/<tarih>_<hip>[_agfsiz].json (dondurulmuş v9), veri/agf_kayit/<tarih>/<hip>_<HHMM>UTC_ebayi.json (AGF1/AGF2/ganyan/koşmaz), veri/plan/<tarih>.json (koşu saati),
veri/tahminler_birlesik/<tarih>.json (varsa BİRLEŞİK). Çıktı: veri/son_dakika/<tarih>/<hip>_<koşu>.md (yeni dosya).
İçerik: at başına bizim olasılıklar (v9 AGF'li, AGF'siz, varsa BİRLEŞİK), piyasa (şimdi, AGF), sabaha ve −60 dk'ya göre AGF/ganyan değişimi, işaretler; bizim ve piyasanın favorisi farklı mı; para girişi olan atlar.
İşaretler (YALNIZCA bilgi, test edilmedi): 💰 ganyan −60 dk'ya göre >=%30 düştü (g60/g_şimdi >=1,4), 📈 AGF sabaha göre +%30 ve +3 puan, 📉 AGF sabaha göre −%30 ve −3 puan, ⚖ bizim olasılığımız piyasanın >=1,3 katı (değer adayı; kanıtlanmış değil), 🎯 uzun at (piyasa <%10) + bu mesafede atın geçmişi uyumlu (bantta >=4 koşu, ilk-3 >=%50) + babası bu bantta olumlu (26.11 genişletilmiş veriyle test: A/E ≈0,98, avantaj YOK; yalnızca bilgi)."""
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
R10=(yukle(os.path.join(K,'veri','tahminler_10dk',f'{gun}.json')) or {}).get('kosular',{}).get(f'{hip}|{kno}')
if R10: PB={ak(a['ad']):a['p_birlesik10'] for a in R10['atlar']}   # −10 dk BİRLEŞİK (sabahki BİRLEŞİK değil)
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
    if R10:
        _t=next((a.get('tercih') for a in R10['atlar'] if ak(a['ad'])==k),None)
        if _t and _t.get('hedef') and piyasa.get(k) is not None and piyasa[k]<0.10: fl.append('🎯')
    ours=PB.get(k) or P9.get(k)
    if ours and piyasa.get(k) and ours>=1.3*piyasa[k] and piyasa[k]<0.25: fl.append('⚖')
    rows.append((k,v,fl))
def top(d): 
    d={k:x for k,x in d.items() if x is not None}; return max(d,key=d.get) if d else None
favs={'piyasa':top(piyasa),'v9 AGF\'li':top(P9),'v9 AGF\'siz':top(P9s),'BİRLEŞİK':top(PB)}
ad=lambda k:N[k]['ad'] if k in N else '—'
L=[f'# Son dakika özeti — {hip} {kno}. koşu ({saat}), {gun}','',f'Görüntü: {simdi[0]//60:02d}:{simdi[0]%60:02d} UTC (koşuya {tdk-simdi[0]} dk); karşılaştırma: −60 dk ≈ {s60[0]//60:02d}:{s60[0]%60:02d} UTC, sabah = TAM/ilk görüntü. Piyasa kaynağı: {kaynak}. İşaretler yalnızca bilgi, test edilmedi.','',
   '| At | Piyasa % | Sabah AGF | Ganyan −60 → şimdi | v9 AGF\'li % | v9 AGF\'siz % | BİRLEŞİK % | Hip. sicil (start/gal/ilk3) | Mesafe sicili ±200 m | Uzun ≥1900 / Kısa ≤1500 | Mesafe tipi (at / baba / anne babası) | İşaret |','|---|---|---|---|---|---|---|---|---|---|---|---|']
fm=lambda x:'—' if x is None else f'{100*x:.0f}'
def _tip_txt(k):
    if not R10: return '—'
    _m=next((a.get('mesafe_sicil') for a in R10['atlar'] if ak(a['ad'])==k),None) or {}
    _g=lambda x:x if x else '—'
    return f"{_g(_m.get('tip'))} / {_g(_m.get('baba_tip'))} / {_g(_m.get('annebaba_tip'))}"
def _ms_txt(k,anahtar):
    if not R10: return '—'
    _m=next((a.get('mesafe_sicil') for a in R10['atlar'] if ak(a['ad'])==k),None)
    _v=(_m or {}).get(anahtar)
    return '—' if not _v or not _v[0] else f'{_v[0]}/{_v[1]}/{_v[2]}'
def _sic_txt(k):
    if not R10: return '—'
    _s=next((a.get('sicil') for a in R10['atlar'] if ak(a['ad'])==k),None)
    return '—' if not _s or not _s[0] else f'{_s[0]}/{_s[1]}/{_s[2]}'
for k,v,fl in rows:
    g0=O60.get(k,{}).get('gan'); a0=OS.get(k,{}).get('agf'); g1=v['gan']
    gtxt=('—' if g0 is None else f'{g0:g}')+' → '+('—' if g1 is None else f'{g1:g}')
    L.append(f"| {v['ad'][:18]} | {fm(piyasa.get(k))} | {'—' if a0 is None else f'{a0:.1f}'} | {gtxt} | {fm(P9.get(k))} | {fm(P9s.get(k))} | {fm(PB.get(k))} | {_sic_txt(k)} | {_ms_txt(k,'bugun')} | {_ms_txt(k,'uzun')} / {_ms_txt(k,'kisa')} | {_tip_txt(k)} | {' '.join(fl)} |")
L+=['','**Favoriler:** '+' · '.join(f"{n}: {ad(k) if k else '—'}" for n,k in favs.items()),'']
farkli={n for n,k in favs.items() if k and k!=favs['piyasa'] and favs['piyasa']}
L.append('Bizim kollarla piyasa favorisi **ayrışıyor**: '+', '.join(sorted(farkli)) if farkli else 'Bizim kollar piyasa favorisiyle **aynı atta birleşiyor** (ya da tahmin yok).')
_ps=sum(x for x in piyasa.values() if x is not None and x<0.10); _r='yüksek' if _ps>0.31 else 'orta' if _ps>0.198 else 'düşük'; _kl={'düşük':3,'orta':4,'yüksek':5}[_r]
_pr=PB or P9 or piyasa; _top=[ak(x) for x in R10['secim_liste']] if R10 else sorted(_pr,key=lambda k:-(_pr.get(k) or 0))[:_kl]; _r=R10['surpriz_riski'] if R10 else _r; _kl=len(_top)
L.append(f"**Açık koşu riski: {_r}** (piyasada %10 altı atların payı %{100*_ps:.0f}) → liste {_kl} at: "+', '.join(ad(k) for k in _top)+'. Geçmişte bu uzunlukta kazanan listede ~%76–81.')
if R10:   # mesafe tercihi: atın kendisi ve babasının yavruları hangi mesafeyi seviyor (bugünkü bant [..] içinde); n küçükse gösterge değil
    _tm={ak(a['ad']):a.get('tercih') for a in R10['atlar']}; _ls=[]; B5=('≤1200','1300-1400','1500-1700','1800-2100','2200+')
    for _k in [ak(x) for x in R10['secim_liste']]:
        t=_tm.get(_k)
        if not t or 'kendi_mesafe_hepsi' not in t: continue
        bg=t['baslik'].get('mesafe','?'); kh=t['kendi_mesafe_hepsi']; bh=t['baba_mesafe_hepsi']
        mk=lambda b:('['+b+']' if b==bg else b)
        kendi=' | '.join(f"{mk(b)} {kh[b][1]}/{kh[b][2]}/{kh[b][0]}" for b in B5 if kh[b][0])
        baba=' | '.join(f"{mk(b)} {bh[b][2]}" for b in B5 if b in bh)
        _ls.append(f"- {ad(_k)[:16]}: kendi (birinci/ilk3/koşu) {kendi or 'geçmiş yok'}"+(f" || baba {str(t['baba'])[:14]} A/E {baba}" if baba else ''))
    if _ls: L+=['','**Mesafe tercihi (listedeki atlar; [köşeli] = bugünkü mesafe; n küçükse gösterge değil):**']+_ls
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
        if h: L.append(f"- Tarihsel ({key}, 2024+): {h['kosu']} koşu, ort. {h['alan']:.1f} at, favori kazandı %{h['favori']:.0f}, ganyan≥10 olan (gözden kaçan) kazanan %{h['s10']:.0f}"); break
    KR=[r for r in csv.DictReader(open(os.path.join(K,'veri','kosu_tipi_kayit.csv'),encoding='utf-8'))] if os.path.exists(os.path.join(K,'veri','kosu_tipi_kayit.csv')) else []
    ay=[r for r in KR if r['irk']==ti['irk'] and r['tur']==ti['tur']] or [r for r in KR if r['irk']==ti['irk'] and r['aile']==ti['aile']]
    if ay:
        pc=lambda c:(lambda v:'—' if not v else f"%{100*sum(x=='1' for x in v)/len(v):.0f}")([r[c] for r in ay if r[c]!=''])
        L.append(f"- Canlı sicilimiz (aynı çeşit, {len(ay)} koşu{', gösterge değil' if len(ay)<10 else ''}): favori kazandı {pc('fav_kazandi')}, gözden kaçan kazanan %{100*sum(r['surpriz']=='1' for r in ay)/len(ay):.0f}, v9 AGF'li ilk tuttu {pc('v9_agfli_ilk')}, AGF'siz {pc('v9_agfsiz_ilk')}, BİRLEŞİK_10 {pc('b10_ilk')}")
    L.append('')
except Exception as e: print('koşu çeşidi bilgisi eklenemedi:',e,file=sys.stderr)
od=os.path.join(K,'veri','son_dakika',gun); os.makedirs(od,exist_ok=True)
open(os.path.join(od,f'{hip}_{kno}.md'),'w',encoding='utf-8').write('\n'.join(L)+'\n'); print('\n'.join(L))
# ---- ANALİZ LİSTESİ (28.11, kullanıcı listesi): ayrı dosya veri/analiz_listesi/<gün>/<hip>_<koşu>.md (kart bozulmaz)
try:
    _AJ=((yukle(os.path.join(K,'veri','hipodrom_sicil',f'{gun}_analiz.json')) or {}).get(hip,{}) or {}).get(str(kno)) or {}
    _MJ=(yukle(os.path.join(K,'veri','hipodrom_sicil',f'{gun}_mesafe.json')) or {}).get(hip,{})
    _SJ=(yukle(os.path.join(K,'veri','hipodrom_sicil',f'{gun}.json')) or {}).get(hip,{})
    _a={ak(a):d for a,d in (_AJ.get('atlar') or {}).items()}; _m={ak(a):d for a,d in _MJ.items()}; _s={ak(a):d for a,d in _SJ.items()}
    _c30=once(tdk-30); O30=oku(yukle(_c30[1]),kno) if _c30 else {}
    _o=[x for x in S if 8*60+30<=x[0]<=9*60+5]; O12=oku(yukle(_o[-1][1]),kno) if _o else {}
    _f=lambda x,n=1:'—' if x is None else (f'{x:.{n}f}')
    _fv=lambda v:'—' if not v or not v[0] else '/'.join(str(i) for i in v)
    _sg=lambda x,n=1:'—' if x is None else f'{x:+.{n}f}'
    _sira=[(k,v) for k,v,_ in rows]
    _grup=_AJ.get('grup') or {}
    A=[f'# Analiz listesi — {hip} {kno}. koşu ({saat}), {gun}','',f'Görüntü {simdi[0]//60:02d}:{simdi[0]%60:02d} UTC (koşuya {tdk-simdi[0]} dk). Atlar piyasa sırasıyla. Veri: at_gecmisi (2020+), program CSV, eBayi görüntüleri. Yorum değil kayıt; test notları `ANALIZ_INDEKSI.md`den.','']
    _ikr=_grup.get('ikramiye'); A.extend([f"**Koşu:** {_grup.get('tur') or '—'} | {_grup.get('mesafe') or '—'} m {_grup.get('zemin') or '—'} | {_grup.get('at_sayisi') or '—'} at | 1. ikramiye {('%s TL'%format(_ikr,',').replace(',','.')) if _ikr else '—'}",''])
    A.extend(['## 0. Mevcut kart: piyasa, modeller (v9 AGF\'li/AGF\'siz, BİRLEŞİK_10 + sicil çarpanı), işaretler (💰📈📉⚖🤫🎯), açık koşu riski, mesafe tercihi, koşu çeşidi',''])
    A.extend([(x.replace('# ','### ',1) if x.startswith('# ') else x) for x in L]); A.append('')
    def tablo(baslik,not_,basliklar,satir):
        A.extend([f'## {baslik}',''])
        if not_: A.extend([f'_{not_}_',''])
        A.append('| At | '+' | '.join(basliklar)+' |'); A.append('|---|'+'---|'*len(basliklar))
        for k,v in _sira:
            d=_a.get(k,{}); A.append(f"| {v['ad'][:18]} | "+' | '.join(str(x) for x in satir(k,v,d))+' |')
        A.append('')
    tablo('1. Çim / kum / sentetik tablosu (tüm hipodromlar, start/gal/ilk 3)',f"Bugünkü zemin: {_grup.get('zemin') or '—'}.",['Kum','Çim','Sentetik'],lambda k,v,d:[_fv((d.get('zemin_sicil') or {}).get(z)) for z in ('Kum','Çim','Sentetik')])
    tablo('2. Çimden kuma / kumdan çime geçiş','Test (gozden_kacan_ozellik, uzun atlar): bu zemine ilk kez çıkan çim için A/E 1,14, kuma için 0,83 (zayıf kanıt).',['Son koşu zemini','Geçiş'],lambda k,v,d:[d.get('son_zemin') or '—',d.get('zemin_gecis') or '—'])
    tablo('3. Kilo avantajı','Test: kilo sırası piyasa ötesi bilgi vermedi (A/E ~1,0); apranti A/E 0,97; sahanın en ağır 3 atı apranti ise 0,84 (handikap, fark ≥8 kg).',['Kilo','Sahada sıra (1 = en ağır)','En ağırdan fark','Son koşuya göre kg','Apranti'],lambda k,v,d:[_f(d.get('kilo')),d.get('kilo_sira') or '—',_f((_grup.get('kilo_aralik') or [None,None])[1]-d['kilo']) if d.get('kilo') and _grup.get('kilo_aralik') else '—',_sg(d.get('kilo_fark_son')),'AP' if d.get('apranti') else '—'])
    tablo('4. Atın hipodrom sicili (bu hipodrom, start/gal/ilk 3)','Test: >=3 start ve galibiyet oranı >=%30 A/E 1,08; ilk 3 oranı >=%50 uzun atlarda 1,12. BİRLEŞİK_10 bu çarpanı uyguluyor.',['Sicil','Liste çarpanı'],lambda k,v,d:[_fv(_s.get(k)),next((a.get('sicil_carpan') for a in (R10 or {}).get('atlar',[]) if ak(a['ad'])==k),'—') if R10 else '—'])
    tablo('5. Soyların uzun / orta / kısa mesafe durumu','Bant: kısa <=1400, orta 1500-1799, uzun >=1800 m. Soy tipi yavruların piyasaya göre A/E değerinden (mesafe_tipi.py).',['At tipi','Baba (tip)','Anne babası (tip)'],lambda k,v,d:[(_m.get(k) or {}).get('tip') or '—',f"{(_m.get(k) or {}).get('baba') or '—'} ({(_m.get(k) or {}).get('baba_tip') or '—'})",f"{(_m.get(k) or {}).get('annebaba') or '—'} ({(_m.get(k) or {}).get('annebaba_tip') or '—'})"])
    tablo('6. Mesafe artmış mı azalmış mı; bu mesafede ne kadar koşmuş',f"Bugünkü mesafe {_grup.get('mesafe') or '—'} m. Test: ±200 m'de >=3 start galibiyet oranı >=%30 A/E 1,06; uzun atta bu mesafede hiç koşmamış 0,87.",['Son koşu mesafesi','Değişim (m)','Bu mesafede ±200 m (start/gal/ilk3)','Uzun / Kısa'],lambda k,v,d:[((d.get('son') or {}).get('mesafe') or '—'),('—' if d.get('mesafe_degisim') is None else ('artış '+_sg(d['mesafe_degisim'],0) if d['mesafe_degisim']>0 else 'azalış '+_sg(d['mesafe_degisim'],0) if d['mesafe_degisim']<0 else 'aynı')),_fv((_m.get(k) or {}).get('bugun')),f"{_fv((_m.get(k) or {}).get('uzun'))} / {_fv((_m.get(k) or {}).get('kisa'))}"])
    tablo('7. Çimi seven / kumu seven atlar','Tercih: >=3 start olan zeminlerde ilk 3 oranı en yüksek zemin, diğerinden >=15 puan önde.',['Tercih','Kum ilk3 oranı','Çim ilk3 oranı'],lambda k,v,d:[d.get('zemin_tercih') or '—']+[('—' if not (d.get('zemin_sicil') or {}).get(z,[0])[0] else f"%{100*d['zemin_sicil'][z][2]/d['zemin_sicil'][z][0]:.0f} ({d['zemin_sicil'][z][0]} start)") for z in ('Kum','Çim')])
    def _para(k):
        g=lambda O:(O.get(k) or {}).get('gan'); a,b,c=g(O60),g(O30),g(N); x=''
        if a and c and a/c>=1.3: x='GİRİŞ 💰'
        elif a and c and c/a>=1.3: x='ÇIKIŞ'
        return f"{_f(a)} → {_f(b)} → {_f(c)}",x or '—'
    tablo('8. Para girişleri / çıkışları (ganyan −60 → −30 → şimdi)','İşaret: ganyan −60 dk\'ya göre >=%30 düştü = GİRİŞ, >=%30 yükseldi = ÇIKIŞ (test edilmedi, bilgi).',['Ganyan','Yön'],lambda k,v,d:list(_para(k)))
    def _agf(k):
        a0=(OS.get(k) or {}).get('agf'); a1=(N.get(k) or {}).get('agf'); fl=''
        if a0 and a1 and a1>=1.3*a0 and a1-a0>=3: fl='📈 yükselen'
        elif a0 and a1 and a1<=0.7*a0 and a0-a1>=3: fl='📉 düşen'
        return f"{_f(a0)} → {_f(a1)}",_sg(None if a0 is None or a1 is None else a1-a0),fl or '—'
    tablo('9. AGF yükselen / düşen (sabah → şimdi, %)','Sabah = TAM+15 dk görüntü.',['AGF','Fark (puan)','Yön'],lambda k,v,d:list(_agf(k)))
    def _of(k):
        a0=(OS.get(k) or {}).get('agf'); a2=(O12.get(k) or {}).get('agf'); a1=(N.get(k) or {}).get('agf')
        return f"{_f(a0)} → {_f(a2)} → {_f(a1)}",_sg(None if a0 is None or a2 is None else a2-a0),_sg(None if a2 is None or a1 is None else a1-a2)
    tablo('10. Sabah AGF – öğleden sonra AGF (12:00 TR görüntüsü) – şimdi','Öğle görüntüsü yoksa "—".',['Sabah → öğle → şimdi','Öğle − sabah','Şimdi − öğle'],lambda k,v,d:list(_of(k)))
    tablo('11. Jokey değişimi','Test (tarihsel): jokey değişimi tek başına ayırt edici değil; apranti işaretli.',['Önceki jokey','Bugünkü jokey','Değişti mi'],lambda k,v,d:[d.get('onceki_jokey') or '—',d.get('jokey') or '—','—' if d.get('jokey_degisti') is None else ('EVET' if d['jokey_degisti'] else 'hayır')])
    tablo('12. At kalitesi: bu grupta denge',f"Grup HP ortalaması {_grup.get('hp_ort') or '—'}, std {_grup.get('hp_std') or '—'}, aralık {'–'.join(str(int(x)) for x in _grup['hp_aralik']) if _grup.get('hp_aralik') else '—'}, kilo aralığı {'–'.join(str(x) for x in _grup['kilo_aralik']) if _grup.get('kilo_aralik') else '—'}, {_grup.get('at_sayisi') or '—'} at. Test: HP sırası piyasa ötesi bilgi vermedi (HP ilk 3 sızıntısı geri çekildi).",['HP','HP sırası (1 = en yüksek)','Grup ortalamasına fark','Son koşuya göre HP'],lambda k,v,d:[_f(d.get('hp'),0),d.get('hp_sira') or '—',_sg(d.get('hp_fark_ort')),_sg(d.get('hp_fark_son'))])
    tablo('13. Atın temel bilgileri','Kulvar testi: iç kulvar (1-3) uzun atlarda göreli A/E 1,05; Bursa çimde iç kulvar A/E 1,10, kumda fark yok (tek seferlik tablo). Yaş-cinsiyet: e/d genç, a/k 4+, g iğdiş.',['Yaş / cinsiyet','Kulvar','KGS (gün)','Son 6 yarış','Takı','Antrenör','Ekuri'],lambda k,v,d:[d.get('yas') or '—',d.get('kulvar') or '—',d.get('kgs') or '—',d.get('son6') or '—',d.get('taki') or '—',d.get('antrenor') or '—','EKURİ' if d.get('ekuri') else '—'])
    tablo('14. Form ve sınıf','Tabela = son 8 koşunun ortalama bitiş sırası (düşük iyi). Test: tabela, sınıf düşüşü, ilk kez hipodrom/mesafe/yüzey piyasa ötesi bilgi vermedi (zayıf/etkisiz).',['Tabela (son 8 ort. sıra)','Son koşu (tarih, hip, sıra/at)','Tür: önceki → bugün','İlk kez (hip / mesafe / zemin)'],lambda k,v,d:[_f(d.get('ort_sira_8')),(f"{d['son']['tarih']} {d['son']['hip']} {d['son']['sira'] or '—'}/{d['son']['kosan']}" if d.get('son') else 'ilk koşu'),f"{d.get('son_tur') or '—'} → {d.get('bugun_tur') or '—'}",', '.join([x for x,t in (('hipodrom',not (_s.get(k) or [0])[0]),('mesafe',not ((_m.get(k) or {}).get('bugun') or [0])[0]),('zemin',str(d.get('zemin_gecis') or '').endswith('İLK KEZ)'))) if t]) or '—'])
    tablo('15. Baş-başa (h2h) skoru','Aynı koşudaki diğer atlara karşı geçmiş karşılaşma skoru (BİRLEŞİK_10 = piyasa + 0,5 x baş-başa). Test: h2h A/E 1,13 lider ama log-kazanç anlamsız.',['Baş-başa skoru','BİRLEŞİK % (sicil çarpanlı)'],lambda k,v,d:[next((a.get('h2h') for a in (R10 or {}).get('atlar',[]) if ak(a['ad'])==k),'—'),fm(PB.get(k))])
    ad_=os.path.join(K,'veri','analiz_listesi',gun); os.makedirs(ad_,exist_ok=True)
    open(os.path.join(ad_,f'{hip}_{kno}.md'),'w',encoding='utf-8').write('\n'.join(A)+'\n')
except Exception as e: print('analiz listesi eklenemedi:',e,file=sys.stderr)
