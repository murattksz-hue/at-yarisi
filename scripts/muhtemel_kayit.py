"""beygir.com/muhtemeller anlık görüntüsü (robots.txt izin veriyor; /api/ kullanılmaz). Ganyan, ikili, sıralı ikili, çifte muhtemelleri.
Sayfa metni sıkıştırılarak veri/muhtemel_kayit/<tarih>/<SSDD>UTC.txt.gz olarak saklanır; içerik değişmediyse saklanmaz."""
import os,re,gzip,html,hashlib,subprocess,datetime,glob
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
g=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).date()
b=subprocess.run(['curl','-sSL','--max-time','90','-A','at-yarisi-analiz/1.0','https://www.beygir.com/muhtemeller'],capture_output=True).stdout.decode('utf-8','replace')
t=re.sub(r'<script.*?</script>|<style.*?</style>','',b,flags=re.S); x=re.sub(r'\n\s*\n+','\n',re.sub(r'[ \t]+',' ',html.unescape(re.sub(r'<[^>]+>','\n',t))))
if 'muhtemelleri' not in x: print('muhtemel sayfası alınamadı'); raise SystemExit
kd=os.path.join(K,'veri','muhtemel_kayit',g.isoformat()); os.makedirs(kd,exist_ok=True)
h=hashlib.md5(x.encode()).hexdigest(); son=sorted(glob.glob(os.path.join(kd,'*.txt.gz')))
if son and hashlib.md5(gzip.open(son[-1],'rt',encoding='utf-8').read().encode()).hexdigest()==h: print('muhtemeller değişmemiş'); raise SystemExit
f=os.path.join(kd,datetime.datetime.now(datetime.timezone.utc).strftime('%H%M')+'UTC.txt.gz')
with gzip.open(f,'wt',encoding='utf-8') as o: o.write(x)
print('muhtemeller kaydedildi:',os.path.basename(f),os.path.getsize(f)//1024,'KB')
