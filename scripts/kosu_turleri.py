"""Koşu türü ve ek şart kodu sözlüğü. Kullanım:
  kosu_turleri.py kur sonuc_dizini            -> veri/kosu_turleri.json'u sonuçlardan kurar
  kosu_turleri.py kontrol program.csv TARİH   -> yeni tür/kod varsa sözlüğe ekler ve yazdırır"""
import sys,os,re,glob,json
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); J=os.path.join(K,'veri','kosu_turleri.json')
TANIM={'DHÖW':'Devlet Harası, Özel veya WAHO kayıtlı Arap atları (TJK Genel Hükümler 2026)','Dişi':'Sadece dişiler','E':'Sadece erkekler',
 'Y1':'Apranti koşusu (Y0-Y1 yamaklar)','Y2':'Apranti koşusu (Y0-Y2)','Y3':'Apranti koşusu (Y0-Y3)','ULS':'Uluslararası','ULS-W':'Uluslararası, WAHO kayıtlı',
 'Maiden':'Hiç birincilik kazanmamış atlar','Şartlı 19':'Koşu kazanmamışlar (maiden gibi, bölünmez)','Şartlı 27':'Hiç start almamışlar',
 'G1':'Grup 1 (açık)','G2':'Grup 2 (açık)','G3':'Grup 3 (açık)'}
def tur(s):
    S=s.upper()
    for pat,f in [(r'\bG ?([123])\b',lambda m:'G'+m.group(1)),(r'KV-? ?(\d+)',lambda m:'KV-'+m.group(1)),(r'SATI\w* ?(\d+)?',lambda m:('Satış '+(m.group(1) or '')).strip()),
                  (r'MA[İI]DEN',lambda m:'Maiden'),(r'ŞARTLI ?-?(\d+)',lambda m:'Şartlı '+m.group(1)),(r'HAND[İI]KAP ?(\d+)',lambda m:'Handikap '+m.group(1)),(r'AÇIK|ACIK',lambda m:'Açık')]:
        m=re.search(pat,S)
        if m: return f(m)
    return s.split('/')[0].strip()
def kodlar(s): return [k.strip() for k in re.findall(r'/\s*([A-ZÇĞİÖŞÜa-zçğıöşü0-9-]+)',s)]
def basliklar(f):
    for l in open(f,encoding='utf-8-sig'):
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]): yield c[1].strip()
if sys.argv[1]=='kur':
    D={'turler':{},'kodlar':{}}
    for f in sorted(glob.glob(sys.argv[2]+'/*.csv')):
        g=os.path.basename(f)[:10]
        for s in basliklar(f):
            t=D['turler'].setdefault(tur(s),dict(ilk=g,sayi=0,tanim=TANIM.get(tur(s),''))); t['sayi']+=1
            for k in kodlar(s): d=D['kodlar'].setdefault(k,dict(ilk=g,sayi=0,tanim=TANIM.get(k,'tanım bulunamadı'))); d['sayi']+=1
    json.dump(D,open(J,'w'),ensure_ascii=False,indent=1); print(len(D['turler']),'tür,',len(D['kodlar']),'kod')
else:
    D=json.load(open(J,encoding='utf-8')); yeni=[]
    for s in basliklar(sys.argv[2]):
        if tur(s) not in D['turler']: D['turler'][tur(s)]=dict(ilk=sys.argv[3],sayi=0,tanim=''); yeni.append(('tür',tur(s),s))
        D['turler'][tur(s)]['sayi']+=0
        for k in kodlar(s):
            if k not in D['kodlar']: D['kodlar'][k]=dict(ilk=sys.argv[3],sayi=0,tanim='tanım bulunamadı'); yeni.append(('kod',k,s))
    json.dump(D,open(J,'w'),ensure_ascii=False,indent=1)
    for a,b,s in yeni: print(f"YENİ KOŞU {a.upper()}: {b}  (koşu adı: {s}) - tanımı araştırılacak")
