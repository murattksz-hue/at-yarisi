"""Kupon değerlendirme: kupondaki her ayağı resmî sonuçtan tuttu/yattı olarak çıkarır. Kullanım:
  kupon_degerlendir.py <YYYY-AA-GG> <Hipodrom> --ayak "<koşu_no>:AT1,AT2,..." [--ayak ...] [--ad "kupon adı"]
Örnek (27.11 İzmir 4'lü ganyan):
  kupon_degerlendir.py 2026-11-27 İzmir --ayak "3:AÇANAY,PATARA,GÜLNARLI,BİBAHANIM,DENİZOVA,ÖKE HATUN" --ayak "4:CANVELO" --ayak "5:DENİZ KESTANESİ" --ayak "6:SARSALA,TURBO KING,ÖZGÜNSULTAN,KIVIRCIK MEMET,BAY TAYLAN,COŞKUNTAY"
Ekuri atları ayrı yaz (ikisini de). Kaynak: ebayi.org resmî sonuç JSON (sonuclar/<YYYYMMDD>/full/<HIP>.json). Yalnızca okur, ağa tek GET atar.
Kural: kupon sonucu cümlesi bu betiğin çıktısından alınır, hafızadan yazılmaz."""
import sys,re,json,subprocess,argparse
EB={'İzmir':'IZMIR','İstanbul':'ISTANBUL','Şanlıurfa':'SANLIURFA','Elazığ':'ELAZIG','Diyarbakır':'DIYARBAKIR','Adana':'ADANA','Bursa':'BURSA','Ankara':'ANKARA','Kocaeli':'KOCAELI','Antalya':'ANTALYA'}
ak=lambda s:re.sub(r'\W','',str(s).upper().replace('İ','I').replace('ı','I'))
ap=argparse.ArgumentParser(); ap.add_argument('tarih'); ap.add_argument('hip'); ap.add_argument('--ayak',action='append',required=True); ap.add_argument('--ad',default='kupon')
a=ap.parse_args()
kod=EB.get(a.hip,a.hip.upper())
o=subprocess.run(['curl','-sS','--max-time','60','-A','Mozilla/5.0',f"https://ebayi.org/s/d/sonuclar/{a.tarih.replace('-','')}/full/{kod}.json"],capture_output=True).stdout.decode('utf-8','replace')
try: J=json.loads(o)
except Exception: sys.exit('sonuç alınamadı (ebayi JSON okunamadı)')
S={}
for k in J.get('kosular',[]):
    at=[x for x in k.get('atlar',[]) if str(x.get('SONUC') or '').isdigit() and not x.get('KOSMAZ')]
    if at: S[str(k['NO'])]=sorted(at,key=lambda x:int(x['SONUC']))
sonuc=[];ok=True
print(f'# {a.ad}: {a.tarih} {a.hip}')
for i,s in enumerate(a.ayak,1):
    no,_,liste=s.partition(':'); no=no.strip(); secim=[ak(x) for x in liste.split(',') if x.strip()]
    r=S.get(no)
    if not r: print(f'Ayak {i} (koşu {no}): sonuç YOK'); ok=None; sonuc.append(None); continue
    w=r[0]; tut=ak(w['AD']) in secim
    print(f"Ayak {i} (koşu {no}): {'TUTTU' if tut else 'YATTI'} | kazanan {w['AD'].strip()} (ganyan {w.get('GANYAN')}) | seçim {len(secim)} at" + ('' if tut else f" | 2. {r[1]['AD'].strip()}, 3. {r[2]['AD'].strip()}" if len(r)>2 else ''))
    sonuc.append(tut)
    if not tut and ok is not None: ok=False
tut=sum(1 for x in sonuc if x); bit=sum(1 for x in sonuc if x is not None)
print(f"Özet: {tut}/{len(sonuc)} ayak tuttu" + (f" ({bit} ayak sonuçlandı)" if bit!=len(sonuc) else '') + ' | kupon ' + ('TUTTU' if ok else 'YATTI' if ok is False else 'BELİRSİZ (sonuç eksik)'))
