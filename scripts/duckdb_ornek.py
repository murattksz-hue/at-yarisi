"""DuckDB ile analiz örneği: at sayısına göre sürpriz oranı (gerçek / piyasanın beklediği). Kullanım: duckdb_ornek.py
Kurulum (yalnızca elle analiz için, Actions'a EKLEME): pip install duckdb
at_gecmisi/*.csv.gz dosyalarını SQL ile doğrudan okur (17.884 koşu ~0,7 sn). Yeni analizler için şablon:
  - ganyan virgüllü: TRY_CAST(replace(ganyan,',','.') AS DOUBLE)
  - geçerli koşu: tüm atlarda ganyan>1, >=5 at, tek kazanan
  - piyasa olasılığı: (1/g)/sum(1/g) OVER (PARTITION BY tarih,hip,kosu)
Sonuç Python analizlerimizle birebir tuttu (22.11.2026 testi: 5-8 at %8,8 · 9-11 %15,4 · 12-14 %23,7 · 15+ %30,0)."""
import os,duckdb
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YOL=os.path.join(K,'veri','at_gecmisi','202[4-9]','*.csv.gz')
SQL=f"""
WITH r AS (
  SELECT tarih,hip,kosu, TRY_CAST(replace(ganyan,',','.') AS DOUBLE) AS g, sonuc='1' AS kazandi
  FROM read_csv('{YOL}', all_varchar=true, header=true)
), gecerli AS (
  SELECT tarih,hip,kosu FROM r GROUP BY ALL
  HAVING count(*)>=5 AND min(g)>1 AND count(*) FILTER (WHERE kazandi)=1
), k AS (
  SELECT r.*, (1/g)/sum(1/g) OVER (PARTITION BY r.tarih,r.hip,r.kosu) AS p,
         count(*) OVER (PARTITION BY r.tarih,r.hip,r.kosu) AS n
  FROM r JOIN gecerli USING (tarih,hip,kosu)
), yarislar AS (
  SELECT tarih,hip,kosu, any_value(n) AS n,
         max(CASE WHEN kazandi AND g>=10 THEN 1 ELSE 0 END) AS surpriz,
         sum(CASE WHEN g>=10 THEN p ELSE 0 END) AS beklenen
  FROM k GROUP BY ALL
)
SELECT CASE WHEN n<=8 THEN '5-8' WHEN n<=11 THEN '9-11' WHEN n<=14 THEN '12-14' ELSE '15+' END AS at_sayisi,
       count(*) AS kosu, round(avg(surpriz),3) AS gercek, round(avg(beklenen),3) AS beklenen,
       round(sum(surpriz)/sum(beklenen),2) AS "A/E"
FROM yarislar GROUP BY ALL
UNION ALL SELECT 'HEPSİ', count(*), round(avg(surpriz),3), round(avg(beklenen),3), round(sum(surpriz)/sum(beklenen),2) FROM yarislar
ORDER BY CASE at_sayisi WHEN '5-8' THEN 1 WHEN '9-11' THEN 2 WHEN '12-14' THEN 3 WHEN '15+' THEN 4 ELSE 5 END
"""
if __name__=='__main__': print(duckdb.connect().sql(SQL))
