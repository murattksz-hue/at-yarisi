"""yenibeygir 'Blt' (Bülten Ortalama Puanı) ya da AGF sayılarını CSV'ye EKLER (yenibeygir aynı sütunu önce 'Blt', AGF yayınlanınca 'AGF' diye gösterebilir; başlık `sutun` sütununa yazılır). Kullanım: yenibeygir_blt_kayit.py <html_dosyası> <tarih YYYY-AA-GG> <hipodrom>
Bu betik ağa çıkmaz: html'yi elle bir kez indir (curl, tek istek) ve ver. Otomatik/zamanlı çekim EKLEME (site şartları madde 4 izinsiz otomatik taramayı yasaklıyor).
Yalnızca sayılar ve at adı tutulur (sayfa içeriği kopyalanmaz). Çıktı: veri/yenibeygir_el_kayit/blt_<tarih>.csv (zaman_tr sütunuyla eklenir)."""
import sys,os,re,csv,html,datetime
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
yol,tarih,hip=sys.argv[1:4]
t=open(yol,encoding='utf-8',errors='replace').read()
tb=[m.start() for m in re.finditer(r'<table class="kosanAtlar">',t)]
TR=datetime.timezone(datetime.timedelta(hours=3)); an=datetime.datetime.now(TR).strftime('%H:%M')
out=[]
for i,s in enumerate(tb):
    onc=t[(tb[i-1] if i else 0):s]
    k=re.findall(r'(\d+)\s*\.\s*</?[^>]*>\s*(\d\d:\d\d)',re.sub(r'\s+',' ',onc))
    kosu,saat=(k[-1] if k else (str(i+1),''))
    pm=re.findall(r'yarisPara">(?:&#x20BA;|₺)?([\d\.]+)',onc); para=pm[-1].replace('.','') if pm else ''
    e=t.find('</table>',s); blok=t[s:e]
    bh=re.search(r'<th[^>]*>\s*(Blt|AGF)\s*</th>',blok); sutun=bh.group(1) if bh else '?'
    for r in re.findall(r'<tr>\s*<td>\s*<span[^>]*>\s*(\S*)\s*</span>\s*</td>\s*<td class="atno">\s*(\d+)\s*</td>.*?class="atisimlink"[^>]*>(.*?)</a>',blok,flags=re.S):
        out.append((an,tarih,hip,kosu,para,r[1],html.unescape(r[2]).strip(),r[0],sutun))
if not out: sys.exit('satır bulunamadı')
d=os.path.join(K,'veri','yenibeygir_el_kayit'); os.makedirs(d,exist_ok=True); fn=os.path.join(d,f'blt_{tarih}.csv'); yeni=not os.path.exists(fn)
w=csv.writer(open(fn,'a',newline='',encoding='utf-8'))
if yeni: w.writerow(['zaman_tr','tarih','hipodrom','kosu','ikramiye_tl','at_no','at_adi','blt','sutun'])
w.writerows(out)
S={}
for r in out: S.setdefault(r[3],[]).append(int(r[7]) if r[7].isdigit() else 0)
print('yazıldı',fn,len(out),'satır;', {k:(len(v),sum(v)) for k,v in S.items()})
