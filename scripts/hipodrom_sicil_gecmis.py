"""Geçmiş koşulardaki her atın koşu ÖNCESİ hipodrom sicili. Kullanım: hipodrom_sicil_gecmis.py -> veri/hipodrom_sicil_gecmis.csv.gz
Satır = at-koşu (2020+). Sütunlar: tarih,hip,kosu,kod,at,sicil_start,sicil_galibiyet,sicil_ilk3,sicil_son_sira (bu hipodromdaki önceki start/galibiyet/ilk 3/son sıra, koşudan ÖNCEKİ geçmişten, kronolojik, sızıntı yok).
Analizlerde birleştirme anahtarı (tarih,hip,kosu,kod). Yalnızca okur; yazar veri/hipodrom_sicil_gecmis.csv.gz."""
import os,glob,gzip,csv,io,collections
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R=collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','*','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'].zfill(2))].append(r)
st={}   # (kod,hip) -> [start, galibiyet, ilk3, son_sira]
out=io.StringIO(); w=csv.writer(out); w.writerow(['tarih','hip','kosu','kod','at','sicil_start','sicil_galibiyet','sicil_ilk3','sicil_son_sira'])
n=0
for key in sorted(R):
    rs=R[key]
    for r in rs:
        s=st.get((r['kod'],key[1]),[0,0,0,''])
        w.writerow([key[0],key[1],key[2].lstrip('0') or '0',r['kod'],r['at'].strip(),s[0],s[1],s[2],s[3]]); n+=1
    for r in rs:
        x=st.setdefault((r['kod'],key[1]),[0,0,0,'']); sn=r['sonuc'].strip()
        if sn.isdigit(): x[0]+=1; x[1]+=sn=='1'; x[2]+=int(sn)<=3; x[3]=int(sn)
with gzip.open(os.path.join(K,'veri','hipodrom_sicil_gecmis.csv.gz'),'wt',encoding='utf-8',newline='') as f: f.write(out.getvalue())
print('yazıldı veri/hipodrom_sicil_gecmis.csv.gz |',n,'at-koşu')
