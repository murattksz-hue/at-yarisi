"""TAM AGF tespiti (saf fonksiyonlar, ağ yok). agf_kayit.py kullanır.
Sorun (25.11.2026): AGF ilk yayında KISMİ geliyor (atların çoğu %0); 'ILK' dosyası ilk görünme saatini verir ama sabah AGF'si olarak yanlış,
ve tahmin dondurma ILK'e bağlı olduğundan AGF'li model kısmi AGF'yle dondurulabiliyordu. TAM = altılıya giren her koşuda atların >=%90'ının AGF'si dolu ilk görüntü.
Kapanışta bütün koşular %100 dolu; ilk yayından ~20-25 dk sonra tamamlanıyor (23.11: Bursa 09:23, Şanlıurfa 09:28 TSİ)."""
import re
ESIK=0.9
def altili_yarislar(b):
    """Program CSV bayt/metninden altılıya giren koşu numaraları. İşaret: "N. 6'LI GANYAN Bu koşudan başlar" (başlangıç koşudan 6 koşu). Bulunamazsa None."""
    s=b.decode('utf-8-sig','replace') if isinstance(b,(bytes,bytearray)) else b
    kosu=None; bas=[]
    for l in s.splitlines():
        m=re.match(r'^(\d+)\. Kosu',l)
        if m: kosu=int(m.group(1))
        if kosu and re.search(r"6'LI GANYAN\s*Bu ko[sş]udan ba[sş]lar",l,re.I): bas.append(kosu)
    return sorted({k for b0 in bas for k in range(b0,b0+6)}) if bas else None
def _agf_tjk(b):
    s=b.decode('utf-8-sig','replace') if isinstance(b,(bytes,bytearray)) else b
    D={};k=None
    for l in s.splitlines():
        m=re.match(r'^(\d+)\. Kosu',l)
        if m: k=int(m.group(1)); D[k]=[]; continue
        p=l.rstrip('\n').split(';')
        if k and re.match(r'^\d+$',p[0]) and len(p)>10 and 'Koşmaz' not in p[1]:
            v=[float(x) for x in re.findall(r'%([\d.]+)\(',p[10])]; D[k].append(max(v) if v else 0.0)
    return D
def _tamam(D,yar):
    """D: {koşu: [at AGF'leri]}. yar biliniyorsa o koşuların hepsi, bilinmiyorsa AGF'si olan koşuların hepsi (en az 6) >=ESIK dolu olmalı."""
    if yar:
        hedef=[k for k in yar if k in D and D[k]]
        if not hedef: return False
    else:
        hedef=[k for k,v in D.items() if v and any(x>0 for x in v)]
        if len(hedef)<6: return False
    return all(sum(x>0 for x in D[k])/len(D[k])>=ESIK for k in hedef)
def tam_tjk(b,yar=None):
    return _tamam(_agf_tjk(b),yar)
def _f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return 0.0
def tam_ebayi(S,yar=None):
    """S: {koşu(str): {at: [AGF1,AGF2,GANYAN,KOSMAZ]}}"""
    D={}
    for k,A in S.items():
        try: kn=int(k)
        except Exception: continue
        D[kn]=[max(_f(v[0]),_f(v[1])) for v in A.values() if not v[3]]
    return _tamam(D,yar)

BEKLEME_DK=15
def olgun(kd,hip,simdi_utc,bekleme=BEKLEME_DK):
    """TAM AGF görüntüsü oturdu mu? 26.11 ölçümü: TAM anındaki AGF kapanışa göre ort. 1,8-5,5 puan oynak, ~15-20 dk sonra 0,3 puana iniyor.
    Dondurma bu yüzden TAM'dan (iki kaynaktan geç olanından) en az bekleme dk sonra yapılır. Saat bilgisi yoksa True (beklemeden)."""
    import json,os
    try: d=json.load(open(os.path.join(kd,'ilk_zaman.json'),encoding='utf-8')).get(hip,{})
    except Exception: return True
    ts=[]
    for k in ('tjk_tam','ebayi_tam'):
        m=re.match(r'(\d\d)(\d\d)',str(d.get(k,'')))
        if m: ts.append(int(m.group(1))*60+int(m.group(2)))
    if not ts: return True
    return simdi_utc.hour*60+simdi_utc.minute>=max(ts)+bekleme
def en_son_tam_csv(kd,hip):
    """O hipodromun en son TAM (dolu) TJK görüntüsünün yolu; yoksa None. Önbellek/boş görüntüler tam_tjk ile elenir."""
    import glob,os
    yar=None
    tf=os.path.join(kd,f"TAM_{hip}.csv")
    if os.path.exists(tf): yar=altili_yarislar(open(tf,'rb').read())
    for yol in sorted(glob.glob(os.path.join(kd,f"{hip}_[0-9][0-9][0-9][0-9]UTC.csv")),reverse=True):
        try:
            b=open(yol,'rb').read()
            if tam_tjk(b,altili_yarislar(b) or yar): return yol
        except Exception: continue
    return None
