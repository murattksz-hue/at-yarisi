"""Galop verisi pegadrom.com'dan (kaynak: TJK idman kayıtları; robots.txt izin veriyor).
Kullanım: galop_pegadrom.py YYYY-AA-GG Hipodrom kosu_sayisi cikti.json
Çıktı: at adı -> {idmanlar:[...], son idman alanları (analiz3 uyumlu)}"""
import sys,re,html,json,subprocess,time,unicodedata
g,hip,n,out=sys.argv[1],sys.argv[2],int(sys.argv[3]),sys.argv[4]
kod=unicodedata.normalize('NFKD',hip.replace('ı','i').replace('İ','I')).encode('ascii','ignore').decode().upper()
def sn(x):
    m=re.match(r'(\d+)\.(\d+)\.(\d+)',x or ''); return int(m.group(1))*60+int(m.group(2))+int(m.group(3))/100 if m else None
R={}
for k in range(1,n+1):
    u=f"https://www.pegadrom.com/galoplar?tarih={g}&hip={kod}&kosu={k}"
    t=subprocess.run(['curl','-sS','--max-time','60','-A','at-yarisi-analiz/1.0',u],capture_output=True).stdout.decode('utf-8','replace'); time.sleep(2)
    for b in re.findall(r'<button[^>]*data-galop-detail-popup="1"[^>]*>',t):
        a={m.group(1):html.unescape(m.group(2)) for m in re.finditer(r'data-detail-([a-z-]+)="([^"]*)"',b)}
        ad=a.get('title','').replace(' - Galop Detay','').strip()
        if not ad: continue
        sp={int(m.group(1)):sn(m.group(2)) for m in re.finditer(r'(\d{3,4}):\s*([\d.]+)',a.get('split',''))}
        R.setdefault(ad,{'kosu':k,'idmanlar':[]})['idmanlar'].append(dict(tarih=a.get('date'),hipodrom=a.get('hip'),pist=a.get('pist'),zemin=a.get('zemin'),
            tur=a.get('idman-turu'),efor=a.get('caba') or a.get('galop-durum'),jokey=a.get('jokey'),sure=a.get('time'),mesafe=a.get('distance'),split={str(kk):v for kk,v in sp.items()},puan=a.get('score')))
    print(f"koşu {k}: toplam {len(R)} at",flush=True)
for ad,d in R.items():   # analiz3 uyumu: en son idman
    import datetime
    L=sorted(d['idmanlar'],key=lambda x:datetime.datetime.strptime(x['tarih'],'%d.%m.%Y'),reverse=True); d['idmanlar']=L
    s=L[0]; d.update(tarih=s['tarih'],pist=s['pist'],tur=s['tur'],hipodrom=s['hipodrom'],jokey=s['jokey'],zaman=s['split'],efor=s['efor'])
json.dump(R,open(out,'w'),ensure_ascii=False,indent=0)
print('BİTTİ',len(R),'at,',sum(len(d['idmanlar']) for d in R.values()),'idman')
