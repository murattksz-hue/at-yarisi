"""Günlük analiz için at geçmişi notları (veri/at_gecmisi, yalnızca analiz gününden ÖNCEKİ koşular).
gecmis(tarih) → {AT ADI: [koşular...]} ; notlar(kosular, hip, mesafe, alan_hp_ort) → kısa metin.
Etiketler testli bulgulara dayanır (BILGI.md): ilk kez hipodrom (A/E 1,00), ilk kez bu uzunluk (formu iyiyse A/E 1,08), sınıf farkı
(yükseliş ≥5: A/E 0,92; sürprizde 0,80), mesafe bandı kaydı (piyasa fiyatlıyor, bilgi)."""
import os,glob,gzip,csv,io,collections
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def _f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
def gecmis(tarih):
    G=collections.defaultdict(list); KH=collections.defaultdict(list)
    for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','*','*.csv.gz'))):
        if os.path.basename(fn)[:10]>=tarih: continue
        rows=list(csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')))
        for r in rows: KH[(r['tarih'],r['hip'],r['kosu'])].append(_f(r['hp']) or 0)
        for r in rows: G[r['at'].upper()].append(r)
    KAL={k:(sum(x for x in v if x>0)/len([x for x in v if x>0])) for k,v in KH.items() if len([x for x in v if x>0])>=4}
    return G,KAL
def bant(m): return 'kısa' if m<=1400 else 'orta' if m<=1900 else 'uzun'
def notlar(R,KAL,hip,mesafe,alan_hp):
    if not R: return 'geçmiş: kayıt yok (ilk koşu ya da veri dışı)'
    t=[f"geçmiş {len(R)} koşu, {sum(r['sonuc']=='1' for r in R)} birinci"]
    B=collections.OrderedDict()
    for r in R: x=B.setdefault(bant(_f(r['mesafe']) or 0),[0,0]); x[0]+=1; x[1]+=r['sonuc'] in ('1','2','3')
    t.append(' '.join(f"{b} {x[1]}/{x[0]} ilk3" for b,x in B.items()))
    if hip not in {r['hip'] for r in R}: t.append(f"İLK KEZ {hip}")
    mm=max(_f(r['mesafe']) or 0 for r in R)
    if mesafe and mesafe>mm+100:
        iyi=sum(1 for r in R[-3:] if (_f(r['sonuc']) or 99)<=3)>=2
        t.append(f"İLK KEZ bu uzunluk (önceki en uzun {int(mm)}m{', formu iyi: testte A/E 1,08' if iyi else ''})")
    ms=[_f(r['mesafe']) or 0 for r in R]
    if mesafe and mesafe not in ms: t.append(f"İLK KEZ {int(mesafe)}m (testte A/E 1,03; formu iyiyse 1,06)")
    if mesafe and ms and mesafe<min(ms)-100: t.append(f"EN KISA mesafesi (önceki en kısa {int(min(ms))}m)")
    if mesafe and ms:
        d=mesafe-ms[-1]
        if abs(d)>=200: t.append(f"son koşuya göre {'+' if d>0 else ''}{int(d)}m {'uzadı' if d>0 else 'kısaldı'}")
    P=[KAL.get((r['tarih'],r['hip'],r['kosu'])) for r in R[-3:]]; P=[p for p in P if p]
    if P and alan_hp:
        fk=sum(P)/len(P)-alan_hp
        t.append(f"sınıf: rakipler son 3 koşusuna göre {'DAHA ZAYIF' if fk>=5 else 'DAHA GÜÇLÜ (testte A/E 0,92)' if fk<=-5 else 'benzer'} ({fk:+.0f} HP)")
    s=R[-1]; t.append(f"son: {s['tarih'][5:]} {s['hip']} {s['sonuc']}/{s['kosan']} {s['mesafe']}{(s['pist'] or '?')[:1]}")
    return ' | '.join(t)
_SM=None
def soy_not(baba,irk,mesafe):
    """Babanın bu ırk+mesafe bandındaki geçmişi (veri/soy_mesafe.json, ≥40 koşu)."""
    global _SM
    import json
    if _SM is None:
        p=os.path.join(K,'veri','soy_mesafe.json'); _SM=json.load(open(p,encoding='utf-8')) if os.path.exists(p) else {}
    if not mesafe or not baba: return ''
    v=_SM.get(f"{irk}|{bant(mesafe)}",{}).get(baba)
    return f"soy {baba[:14]} {bant(mesafe)}: %{v['kazanma']} kazanma, ilk3 %{v['ilk3']} ({v['kosu']} koşu, A/E {v['ae_alan']})" if v else ''
def ek_vektor(R,KAL,hip,mesafe,alan_hp,baba,irk):
    """Model özellikleri (scripts/ek_ozellik.py ile aynı tanım): [sinif, ilk_hip, ilk_mes, en_uzun, en_kisa, mes_deg, soy_bant, iyi_yeni_mes]"""
    global _SM
    import json,math
    if _SM is None:
        p=os.path.join(K,'veri','soy_mesafe.json'); _SM=json.load(open(p,encoding='utf-8')) if os.path.exists(p) else {}
    v=_SM.get(f"{irk}|{bant(mesafe or 0)}",{}).get(baba)
    soy=math.log((v['birinci']+2)/(v['birinci']/v['ae_alan']+2)) if v and v.get('ae_alan') else 0.0
    if not R: return [None,0,0,0,0,0,soy,0]
    ms=[_f(r['mesafe']) or 0 for r in R]; m=mesafe or 0
    P=[KAL.get((r['tarih'],r['hip'],r['kosu'])) for r in R[-3:]]; P=[p for p in P if p]
    iyi=sum(1 for r in R[-3:] if (_f(r['sonuc']) or 99)<=3)>=2; yeni=m not in ms
    return [(sum(P)/len(P)-alan_hp) if (P and alan_hp) else None, int(hip not in {r['hip'] for r in R}), int(yeni), int(m>max(ms)+100), int(m<min(ms)-100), (m-ms[-1])/100, soy, int(iyi and yeni)]
_KH=None
def kan_not(baba,kb,irk,mesafe):
    """Baba hattı (babanın babası) ve anne babası: bu ırk+bantta (veri/kan_hatti.json, ≥60 koşu)."""
    global _KH
    import json
    if _KH is None:
        p=os.path.join(K,'veri','kan_hatti.json'); _KH=json.load(open(p,encoding='utf-8')) if os.path.exists(p) else {}
    if not mesafe: return ''
    g=f"{irk}|{bant(mesafe)}"; ad=lambda s:(s or '').upper().split(' (')[0].strip(); t=[]
    bb=_KH.get('baba_babasi',{}).get(ad(baba)); v=_KH.get('baba_hatti',{}).get(g,{}).get(bb) if bb else None
    if v: t.append(f"baba hattı {bb[:14]} {bant(mesafe)}: %{v['kazanma']} kazanma ({v['kosu']} koşu, A/E {v['ae_alan']})")
    v=_KH.get('annebaba',{}).get(g,{}).get(ad(kb))
    if v: t.append(f"anne babası {ad(kb)[:14]} {bant(mesafe)}: %{v['kazanma']} kazanma ({v['kosu']} koşu, A/E {v['ae_alan']})")
    return ' | '.join(t)
