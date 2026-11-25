"""Sürpriz kazananları AYIRIR ve ayrı analiz eder (yalnızca veri/kazanan_profil.csv'yi OKUR, yeni dosya yazar).
Kullanım: surpriz_ayri.py [YYYY-AA-GG]   (tarih verilmezse bütün günler)
Sürpriz tanımları (hepsi etiketlenir, bir at birden çok tanıma girebilir):
  G   kesin ganyan >= 10                (mevcut kazanan_profil tanımı)
  A10 kapanış AGF < %10  (~ilk 4 dışı)   | AS10 sabah AGF < %10   | A5 kapanış AGF < %5 (büyük sürpriz)
Çıktı: veri/agf_kayit/surpriz_ayri.csv (bütün günler, tanım sütunlarıyla)
       veri/agf_kayit/<tarih>/SURPRIZ.md (o günün sürpriz kartları + toplam karşılaştırma)
'Olası notlar' kural tabanlıdır, KESİN NEDEN değildir; örnek az olduğundan yorum değil gözlem olarak oku."""
import os,csv,sys,collections
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
R=list(csv.DictReader(open(os.path.join(K,'veri','kazanan_profil.csv'),encoding='utf-8')))
import re
_ILK={}
def ilk_dolu(r):
    """O koşuda ILK (ilk yayın) görüntüsünde AGF'si >0 olan at oranı. İlk yayın kısmi olabilir (AGF yeni açılırken çoğu at %0). Bilinmiyorsa None."""
    yol=os.path.join(K,'veri','agf_kayit',r['tarih'],f"ILK_{r['hip']}.csv")
    if yol not in _ILK:
        D={};k=None
        if os.path.exists(yol):
            for l in open(yol,encoding='utf-8-sig',errors='replace'):
                m=re.match(r'^(\d+)\. Kosu',l)
                if m: k=m.group(1);D[k]=[];continue
                p=l.rstrip('\n').split(';')
                if k and re.match(r'^\d+$',p[0]) and len(p)>10 and 'Koşmaz' not in p[1]:
                    v=re.findall(r'%([\d.]+)\(',p[10]); D[k].append(float(v[0]) if v else 0.0)
        _ILK[yol]=D
    L=_ILK[yol].get(str(r['kosu']))
    return (sum(x>0 for x in L)/len(L)) if L else None
def sabah_gecerli(r):
    d=ilk_dolu(r)
    return d is None or d>=0.8
def tanim(r):
    t=[]
    if r.get('surpriz')=='1': t.append('G')
    a_son,a_sabah=f(r.get('agf_son')),f(r.get('agf_sabah'))
    if a_son is not None and a_son<10: t.append('A10')
    if a_sabah is not None and a_sabah<10 and sabah_gecerli(r): t.append('AS10')
    if a_son is not None and a_son<5: t.append('A5')
    return t
def notlar(r):
    n=[]; g=lambda k:f(r.get(k))
    if g('start') is not None and g('start')<=3: n.append(f"iç kulvar (start {int(g('start'))})")
    if r.get('jokey_degisti')=='1': n.append('jokey değişti')
    md=g('mesafe_fark')
    if md is not None and abs(md)>=400: n.append(f"mesafe {md:+.0f} m")
    elif md is not None and abs(md)>=200: n.append(f"mesafe {md:+.0f} m (küçük değişim)")
    if r.get('pist_degisti')=='1': n.append('pist yüzeyi değişti')
    if r.get('hip_degisti')=='1': n.append('hipodrom değişti')
    ao,ag=g('agf_sabah'),g('agf_son')
    if not sabah_gecerli(r): n.append(f"sabah AGF kısmi (ilk yayında atların %{100*ilk_dolu(r):.0f}'i dolu): AGF hareketi/AS10 güvenilmez")
    elif ao is not None and ag is not None:
        if ag-ao>=3: n.append(f"AGF yükseldi {ao:.1f}→{ag:.1f} (para girişi?)")
        elif ag-ao<=-1: n.append(f"AGF düştü {ao:.1f}→{ag:.1f}")
    g30,gs=g('g30'),g('g_son')
    if g30 and gs and g30/gs>=1.4: n.append(f"ganyan son 30 dk'da {g30:g}→{gs:g} (💰)")
    if r.get('sessiz')=='1': n.append('AGF sessiz (🤫)')
    ms,ss=g('model_agfli_sira'),g('model_agfsiz_sira')
    if ss is not None and ms is not None and ss<ms: n.append(f"AGF'siz model daha üstte ({int(ss)}. / AGF'li {int(ms)}.)")
    og,os_=g('onceki_ganyan'),g('onceki_sira')
    if og is not None and os_ is not None and og<3 and os_>=4: n.append(f"önceki koşuda favoriydi (ganyan {og:g}) ve {int(os_)}. bitti")
    if r.get('ilk_kez_hip')=='1': n.append('ilk kez bu hipodromda')
    if r.get('ilk_kez_mesafe')=='1': n.append('ilk kez bu mesafe')
    return n
S=[]
for r in R:
    t=tanim(r)
    if t: S.append((r,t))
gunler=[sys.argv[1]] if len(sys.argv)>1 else sorted({r['tarih'] for r,_ in S})
# --- toplu CSV
OUT=os.path.join(K,'veri','agf_kayit'); os.makedirs(OUT,exist_ok=True)
alan=['tarih','hip','kosu','at','tur','mesafe','pist','kosan','kesin','agf_sabah','agf_son','agf_son_sira','g60','g30','g_son','model_agfli_sira','model_agfsiz_sira','hp_sira','start','jokey_degisti','mesafe_fark','pist_degisti','hip_degisti','onceki_sira','onceki_ganyan','para','sessiz']
with open(os.path.join(OUT,'surpriz_ayri.csv'),'w',encoding='utf-8',newline='') as fh:
    w=csv.writer(fh); w.writerow(alan+['tanim','olasi_notlar'])
    for r,t in sorted(S,key=lambda x:(x[0]['tarih'],x[0]['hip'],int(x[0]['kosu']))):
        w.writerow([r.get(a,'') for a in alan]+['+'.join(t),' ; '.join(notlar(r))])
# --- toplam karşılaştırma (sürpriz G vs diğer kazananlar) bütün günlerde
def oran(rows,fn):
    v=[fn(r) for r in rows]; v=[x for x in v if x is not None]
    return (f"%{100*sum(v)/len(v):.0f} ({sum(v)}/{len(v)})" if v else '—')
ozellik=[('jokey değişti',lambda r:r.get('jokey_degisti')=='1'),('iç kulvar (start ≤3)',lambda r:None if f(r['start']) is None else f(r['start'])<=3),
         ('💰 para girişi',lambda r:(r.get('para')=='1') if r.get('para') in('0','1') else None),('🤫 AGF sessiz',lambda r:(r.get('sessiz')=='1') if r.get('sessiz') in('0','1') else None),
         ('AGF\'li model ilk 3\'te',lambda r:(f(r['model_agfli_sira'])<=3) if f(r['model_agfli_sira']) is not None else None),
         ('AGF\'siz model ilk 3\'te',lambda r:(f(r['model_agfsiz_sira'])<=3) if f(r['model_agfsiz_sira']) is not None else None),
         ('pist yüzeyi değişti',lambda r:(r.get('pist_degisti')=='1') if r.get('pist_degisti') in('0','1') else None),
         ('mesafe ≥200 m değişti',lambda r:(abs(f(r['mesafe_fark']))>=200) if f(r['mesafe_fark']) is not None else None)]
digerleri=[r for r in R if not tanim(r)]
sur_G=[r for r in R if 'G' in tanim(r)]; sur_A=[r for r in R if 'A10' in tanim(r)]
for gun in gunler:
    kartlar=[(r,t) for r,t in S if r['tarih']==gun]
    kazanan=[r for r in R if r['tarih']==gun]
    L=[f"# Sürpriz kazananlar — {gun}","",f"Kayıtlı kazanan: {len(kazanan)} · sürpriz (herhangi bir tanım): {len(kartlar)}. "
       "Tanımlar: **G** ganyan ≥10 · **A10** kapanış AGF <%10 · **AS10** sabah AGF <%10 · **A5** kapanış AGF <%5.","",
       "_Olası notlar kural tabanlıdır, kesin neden değildir; örnek az._",""]
    for r,t in sorted(kartlar,key=lambda x:(x[0]['hip'],int(x[0]['kosu']))):
        L+= [f"## {r['hip']} {r['kosu']}. koşu — {r['at']}  `{'+'.join(t)}`","",
             f"- {r['tur']} · {r['mesafe']} m · {r['pist']} · {r['kosan']} koşan · kesin ganyan **{r['kesin']}** (ganyan sırası {r['ganyan_sira']})",
             f"- AGF sabah {r['agf_sabah']} ({r['agf_sabah_sira']}.) → son {r['agf_son']} ({r['agf_son_sira']}.) · ganyan −60 dk {r['g60'] or '—'} → −30 dk {r['g30'] or '—'} → son {r['g_son'] or '—'}",
             f"- Model sırası: AGF'li {r['model_agfli_sira']}. (%{100*f(r['model_agfli_p']):.0f}) · AGF'siz {r['model_agfsiz_sira']}. · HP sırası {r['hp_sira']}. · start {r['start']} · KGS {r['kgs']}",
             f"- Önceki koşu: {r['onceki_tarih']} · {r['onceki_sira']}. bitti ({r['onceki_kosan']} at, ganyan {r['onceki_ganyan']}) · jokey değişti {r['jokey_degisti']} · mesafe {r['mesafe_fark']} m · pist değişti {r['pist_degisti']}",
             f"- **Olası notlar:** {' ; '.join(notlar(r)) or 'belirgin bir işaret yok'}",""]
    if not kartlar: L+=["Bu gün sürpriz kazanan yok (ya da henüz kayıt yok).",""]
    L+=["## Bütün günler: sürpriz kazananlar ve diğerleri","",f"Sürpriz **G**: {len(sur_G)} · **A10**: {len(sur_A)} · diğer kazananlar: {len(digerleri)}","",
        "| Özellik | Sürpriz G | Sürpriz A10 | Diğer kazananlar |","|---|---|---|---|"]
    for ad,fn in ozellik: L.append(f"| {ad} | {oran(sur_G,fn)} | {oran(sur_A,fn)} | {oran(digerleri,fn)} |")
    L+=["","Not: örnek küçük; yorum için `BILGI.md` ve geçmiş veriyle (surpriz_ortak, surpriz_nerede) birlikte oku."]
    d=os.path.join(OUT,gun); os.makedirs(d,exist_ok=True)
    open(os.path.join(d,'SURPRIZ.md'),'w',encoding='utf-8').write('\n'.join(L)+'\n')
print('sürpriz kaydı:',len(S),'satır |',', '.join(gunler[-3:]))
