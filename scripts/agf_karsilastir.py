"""Koşudan 1 saat önce TJK ve ebayi AGF'lerini karşılaştırır, günlük raporu yazar.
Kullanım: agf_karsilastir.py YYYY-AA-GG [Hipodrom KosuNo]
  Hipodrom ve koşu verilirse: o koşu için en son TJK program CSV'si ile en son ebayi görüntüsü (agf_kayit.py'nin
  az önce aldığı) karşılaştırılır → veri/agf_kayit/<tarih>/karsilastirma.json
  Her çağrıda: veri/agf_kayit/<tarih>/GUNLUK.md yeniden üretilir (sabah ilk yayın: hangi kaynak önce + karşılaştırmalar).
agf_plan.py çağırır: sabah kontrolünden sonra (yalnızca rapor) ve her koşunun -60 dk kaydından sonra."""
import sys,os,re,glob,json,datetime
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TZ=datetime.timezone(datetime.timedelta(hours=3))
g=sys.argv[1]; kd=os.path.join(K,'veri','agf_kayit',g); os.makedirs(kd,exist_ok=True)
KF=os.path.join(kd,'karsilastirma.json'); KR=json.load(open(KF,encoding='utf-8')) if os.path.exists(KF) else {}

def tr_saat(utc):   # '0912' veya '0912 UTC' → '12:12' (İstanbul)
    m=re.match(r'(\d\d)(\d\d)',utc or ''); return f"{(int(m.group(1))+3)%24:02d}:{m.group(2)}" if m else None

def tjk_kosu(yol,no):   # {at_no: (ad, [AGF %, ...])} — sıra: 1. altılı, 2. altılı
    A={}; ic=False
    for l in open(yol,encoding='utf-8-sig',errors='replace'):
        m=re.match(r'^(\d+)\. Kosu',l)
        if m: ic=(m.group(1)==str(no)); continue
        p=l.rstrip('\n').split(';')
        if ic and re.match(r'^\d+$',p[0]) and len(p)>10 and 'Koşmaz' not in p[1]:
            A[p[0]]=(p[1].strip(),[float(x) for x in re.findall(r'%([\d.]+)\(',p[10])])
    return A

def eb_kosu(yol,no):   # {ad: [AGF1, AGF2]} (None = o altılıda yok)
    S=json.load(open(yol,encoding='utf-8')).get(str(no),{})
    f=lambda x: float(str(x).replace(',','.')) if x not in (None,'') else None
    return {ad:[f(v[0]),f(v[1])] for ad,v in S.items() if not v[3]}

def eslestir(tjk_ad,eb_adlar):   # TJK adı ekleri taşır ("DOĞANHAN KG DB SK"), ebayi taşımaz ("DOĞANHAN")
    uy=[a for a in eb_adlar if tjk_ad==a or tjk_ad.startswith(a+' ')]
    return max(uy,key=len) if uy else None

def son(desen):
    L=sorted(glob.glob(os.path.join(kd,desen))); return L[-1] if L else None

def favori(d):
    d={k:v for k,v in d.items() if v is not None}; return max(d,key=d.get) if d else None

def karsilastir(h,no):
    ft,fe=son(f"{h}_*UTC.csv"),son(f"{h}_*UTC_ebayi.json")
    R={'hipodrom':h,'kosu':int(no),'zaman':datetime.datetime.now(TZ).strftime('%H:%M'),
       'tjk_goruntu':tr_saat(os.path.basename(ft).split('_')[-1]) if ft else None,
       'ebayi_goruntu':tr_saat(os.path.basename(fe).split('_')[-2]) if fe else None,'altililar':[]}
    if not ft or not fe: R['not']='TJK veya ebayi görüntüsü yok'; return R
    T,E=tjk_kosu(ft,no),eb_kosu(fe,no)
    ilk_t=os.path.join(kd,f"TAM_{h}.csv"); ilk_e=os.path.join(kd,f"TAM_{h}_ebayi.json")   # sabah AGF: TAM (dolu), yoksa ILK
    if not os.path.exists(ilk_t): ilk_t=os.path.join(kd,f"ILK_{h}.csv")
    if not os.path.exists(ilk_e): ilk_e=os.path.join(kd,f"ILK_{h}_ebayi.json")
    IT=tjk_kosu(ilk_t,no) if os.path.exists(ilk_t) else {}; IE=eb_kosu(ilk_e,no) if os.path.exists(ilk_e) else {}
    # ebayi'de AGF1 dolu olan koşu 1. altılıdadır; TJK sütunundaki değerler de aynı sırayla gelir
    var=[i for i in (0,1) if any(v[i] is not None for v in E.values())] or [0]
    for j,i in enumerate(var):
        atlar=[]
        for at_no,(ad,ag) in sorted(T.items(),key=lambda x:int(x[0])):
            ea=eslestir(ad,E); t=ag[j] if j<len(ag) else None; e=E[ea][i] if ea else None
            atlar.append({'at':at_no,'ad':ad,'tjk':t,'ebayi':e,'fark':round(e-t,2) if None not in (e,t) else None})
        ft_=favori({a['at']:a['tjk'] for a in atlar}); fe_=favori({a['at']:a['ebayi'] for a in atlar})
        st=lambda k:[a['at'] for a in sorted([a for a in atlar if a[k] is not None],key=lambda a:-a[k])][:3]
        fk=[abs(a['fark']) for a in atlar if a['fark'] is not None]
        sab_t=favori({n:(ag[j] if j<len(ag) else None) for n,(_,ag) in IT.items()})
        sab_e=favori({n:(IE[x][i] if (x:=eslestir(ad,IE)) else None) for n,(ad,_) in T.items()})
        R['altililar'].append({'altili':i+1,'favori_tjk':ft_,'favori_ebayi':fe_,'ayni_favori':ft_==fe_,
            'ilk3_ayni':st('tjk')==st('ebayi'),'max_fark':max(fk) if fk else None,
            'eslesmeyen':[a['ad'] for a in atlar if a['ebayi'] is None and a['tjk'] is not None],
            'sabah_favori_tjk':sab_t,'sabah_favori_ebayi':sab_e,'atlar':atlar})
    return R

def rapor():
    iz=os.path.join(kd,'ilk_zaman.json'); IZ=json.load(open(iz,encoding='utf-8')) if os.path.exists(iz) else {}
    L=[f"# AGF günlük kayıt – {g}","","## Sabah ilk AGF (hangi kaynak önce yayınladı)","",
       "| Hipodrom | TJK | ebayi | İlk |","|---|---|---|---|"]
    for h,v in sorted(IZ.items()):
        t,e=v.get('tjk'),v.get('ebayi')   # 'HHMM UTC'; aynı turda alınanlar aynı saati taşır
        ilk='aynı kontrolde' if t and e and t==e else ('TJK' if t and (not e or t<e) else 'ebayi' if e else '—')
        L.append(f"| {h} | {tr_saat(t) or '—'} | {tr_saat(e) or '—'} | {ilk} |")
    L+=["","Saatler İstanbul saatidir ve kontrol turunun saatidir (kontroller 5 dk arayla).","",
        "## Koşudan 1 saat önce TJK – ebayi karşılaştırması","",
        "| Hipodrom | Koşu | Saat | Altılı | Favori TJK | Favori ebayi | Aynı favori | İlk 3 aynı | Maks fark | Sabah→şimdi favori TJK | Sabah→şimdi favori ebayi |",
        "|---|---|---|---|---|---|---|---|---|---|---|"]
    farkli=[]
    for k in sorted(KR,key=lambda k:(KR[k]['hipodrom'],KR[k]['kosu'])):
        r=KR[k]
        if not r['altililar']: L.append(f"| {r['hipodrom']} | {r['kosu']} | {r['zaman']} | — | {r.get('not','')} | | | | | | |")
        for a in r['altililar']:
            L.append(f"| {r['hipodrom']} | {r['kosu']} | {r['zaman']} | {a['altili']}. | {a['favori_tjk'] or '—'} | {a['favori_ebayi'] or '—'} | "
                     f"{'✓' if a['ayni_favori'] else '✗'} | {'✓' if a['ilk3_ayni'] else '✗'} | {a['max_fark'] if a['max_fark'] is not None else '—'} | "
                     f"{a['sabah_favori_tjk'] or '—'}→{a['favori_tjk'] or '—'} | {a['sabah_favori_ebayi'] or '—'}→{a['favori_ebayi'] or '—'} |")
            fa=[x for x in a['atlar'] if x['fark']]
            if fa: farkli.append(f"- {r['hipodrom']} {r['kosu']}. koşu ({a['altili']}. altılı; TJK görüntüsü {r['tjk_goruntu']}, ebayi {r['ebayi_goruntu']}): "+
                                 ", ".join(f"{x['at']} {x['ad']} TJK %{x['tjk']} / ebayi %{x['ebayi']}" for x in fa))
            if a['eslesmeyen']: farkli.append(f"- {r['hipodrom']} {r['kosu']}. koşu: ebayi'de eşleşmeyen at: {', '.join(a['eslesmeyen'])}")
    if farkli: L+=["","### Farklı çıkan atlar",""]+farkli
    open(os.path.join(kd,'GUNLUK.md'),'w',encoding='utf-8').write('\n'.join(L)+'\n')

if len(sys.argv)>=4:
    h,no=sys.argv[2],sys.argv[3]; R=karsilastir(h,no); KR[f"{h}-{no}"]=R
    json.dump(KR,open(KF,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    for a in R['altililar']: print(f"{h} {no}. koşu {a['altili']}. altılı: favori TJK {a['favori_tjk']} / ebayi {a['favori_ebayi']}, maks fark {a['max_fark']}")
    if not R['altililar']: print(f"{h} {no}. koşu: {R.get('not')}")
rapor()
