"""Koşu çeşidi ayrıştırma (saf fonksiyonlar). kosu_turu_analiz.py'deki adlandırmayla aynı: tür ('Şartlı 3', 'Handikap 15', 'KV-7', 'Maiden', 'Grup 2', 'Satış 1' ...), aile, ırk, yaş, mesafe, pist.
Anahtar (veri/kosu_turu_analiz.json ile aynı): f"{irk} {tur}" ve f"{irk} {aile}"."""
import re
def tur(s):
    S=s.upper()
    for pat,f in [(r'\bG ?([123])\b',lambda m:'Grup '+m.group(1)),(r'KV-? ?(\d+)',lambda m:'KV-'+m.group(1)),(r'SATI',lambda m:'Satış'),
                  (r'MA[İI]DEN',lambda m:'Maiden'),(r'ŞARTLI ?-?(\d+)',lambda m:'Şartlı '+m.group(1)),(r'HAND[İI]KAP ?(\d+)',lambda m:'Handikap '+m.group(1)),(r'AÇIK|ACIK',lambda m:'Açık'),
                  (r'\bLİSTE|LISTED',lambda m:'Listed')]:
        m=re.search(pat,S)
        if m: return f(m)
    return 'Diğer'
def aile(t):
    if t.startswith('Şartlı 19') or t.startswith('Şartlı 27') or t=='Maiden': return 'Maiden (kazanmamışlar)'
    for a in ('Şartlı','Handikap','KV','Grup','Satış','Açık','Listed'):
        if t.startswith(a): return a
    return 'Diğer'
def mesafe_band(m):
    try: m=int(m)
    except Exception: return '?'
    return '<1200' if m<1200 else '1200-1399' if m<1400 else '1400-1699' if m<1700 else '1700-1999' if m<2000 else '2000+'
def sinif(baslik):
    """Program başlığından ('1. Kosu :   15.00 ŞARTLI 2/DHÖW 3 Yaşlı Araplar 57.00kg 1400m Kum') koşu çeşidi."""
    t=tur(baslik); irk='Arap' if 'Arap' in baslik else 'İngiliz'
    my=re.search(r'(\d{3,4})\s*m\b',baslik); ym=re.search(r'\b(\d)\s*(?:Yaşlı|ve Yukarı)',baslik); pm=re.search(r'\b(Kum|Çim|Sentetik)\b',baslik)
    return dict(tur=t,aile=aile(t),irk=irk,yas=(ym.group(1)+('+' if 'Yukarı' in baslik[ym.start():ym.start()+14] else '')) if ym else '?',
                mesafe=my.group(1) if my else '',mesafe_band=mesafe_band(my.group(1)) if my else '?',pist=pm.group(1) if pm else '?')
def anahtar(irk,t): return f'{irk} {t}'
