"""Koşu çeşidi raporu. Kullanım: kosu_tipi_rapor.py   → veri/kosu_tipi_rapor.md (gün sonu agf_plan.py çağırır; önce kosu_tipi_kayit.py)
Her çeşit için (aile ve ayrıntılı tür × ırk): TARİHSEL (veri/kosu_turu_analiz.json: koşu sayısı, ort. at, favori %, ganyan≥10 sürpriz %) ve CANLI kayıt (19.11'den beri, veri/kosu_tipi_kayit.csv: koşu, favori kazandı %, sürpriz %, v9 AGF'li / AGF'siz / BİRLEŞİK_10 ilk seçim tuttu %).
Amaç: aynı çeşitten koşu geldiğinde tahmini tarihsel taban oranlar ve kendi canlı sicilimizle birlikte değerlendirmek. n küçükse (<10) yüzdeler gösterge değildir."""
import os,sys,csv,json,collections
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KA=json.load(open(os.path.join(K,'veri','kosu_turu_analiz.json'),encoding='utf-8')) if os.path.exists(os.path.join(K,'veri','kosu_turu_analiz.json')) else {}
R=list(csv.DictReader(open(os.path.join(K,'veri','kosu_tipi_kayit.csv'),encoding='utf-8'))) if os.path.exists(os.path.join(K,'veri','kosu_tipi_kayit.csv')) else []
def yz(rs,c):
    v=[r[c] for r in rs if r[c]!='']; return ('—',0) if not v else (f'%{100*sum(x=="1" for x in v)/len(v):.0f}',len(v))
def satir(ad,rs,hist):
    h=f"{hist['kosu']} koşu, {hist['alan']:.1f} at, fav %{hist['favori']:.0f}, sür. %{hist['s10']:.0f}" if hist else '—'
    sur=f"%{100*sum(r['surpriz']=='1' for r in rs)/len(rs):.0f}"
    fav,_=yz(rs,'fav_kazandi'); a,na=yz(rs,'v9_agfli_ilk'); s,ns=yz(rs,'v9_agfsiz_ilk'); b,nb=yz(rs,'b10_ilk')
    return f"| {ad} | {h} | {len(rs)} | {fav} | {sur} | {a} | {s} | {b} ({nb}) |"
H='| Çeşit | Tarihsel (2024+) | Canlı n | Favori kazandı | Sürpriz | v9 AGF\'li ilk | v9 AGF\'siz ilk | BİRLEŞİK_10 ilk (n) |\n|---|---|---|---|---|---|---|---|'
L=['# Koşu çeşidi raporu','',f'Canlı kayıt: {len(R)} koşu ({min((r["tarih"] for r in R),default="—")} – {max((r["tarih"] for r in R),default="—")}). n<10 olanlar gösterge değildir.','','## Aile × ırk',H]
G=collections.defaultdict(list)
for r in R: G[(r['irk'],r['aile'])].append(r)
for (irk,a),rs in sorted(G.items(),key=lambda kv:-len(kv[1])): L.append(satir(f'{irk} {a}',rs,KA.get(f'{irk} {a}')))
L+=['','## Ayrıntılı tür × ırk (n≥3)',H]
G2=collections.defaultdict(list)
for r in R: G2[(r['irk'],r['tur'])].append(r)
for (irk,t),rs in sorted(G2.items(),key=lambda kv:-len(kv[1])):
    if len(rs)>=3: L.append(satir(f'{irk} {t}',rs,KA.get(f'{irk} {t}')))
L+=['','## Mesafe bandı',H]
G3=collections.defaultdict(list)
for r in R: G3[r['mesafe_band']].append(r)
for b,rs in sorted(G3.items()): L.append(satir(b,rs,None))
open(os.path.join(K,'veri','kosu_tipi_rapor.md'),'w',encoding='utf-8').write('\n'.join(L)+'\n'); print('yazıldı: veri/kosu_tipi_rapor.md')
