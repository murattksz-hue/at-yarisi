# at-yarisi

Türkiye at yarışları (TJK) için notlar, veri toplama ve analiz araçları. Ayrıntılar ve geri test sonuçları: `BILGI.md`.

| Dosya | Ne yapar |
|---|---|
| `scripts/sonuc_indir.py` | Son N günün TJK sonuç CSV'lerini indirir |
| `scripts/aygir_stat.py` | Sonuçlardan aygır kan istatistiği (ırk/zemin/mesafe A/E) üretir |
| `scripts/idman.py` | Günün programındaki galop (idman) bilgilerini toplar |
| `scripts/gunluk.py` | **Tek komut:** `python3 scripts/gunluk.py GG.AA.YYYY [galop]`, o günün tüm Türkiye hipodromlarını indirip analiz eder (`analizler/`) |
| `scripts/hava.py` | Hava arşivi ve koşu günü tahmini (Open-Meteo, yedek wttr.in) |
| `scripts/hava_analiz.py` | Islaklık/sıcaklık etkisi analizi |
| `scripts/model6.py` | v6 (v5 + hava) eğitimi ve testi |
| `scripts/ozellik_test.py` | Literatür etkenlerini (hız puanı, sınıf, kilo, ekipman, antrenör, jokey) piyasaya göre test eder |
| `scripts/hiz_tablosu.py` | Beyer tipi hız puanı tablosu üretir |
| `scripts/galop_pegadrom.py` | Galopları pegadrom.com’dan toplar |
| `scripts/galop_test.py` | Galop özelliklerini piyasaya göre test eder |
| `scripts/analiz3.py` | **Günlük analiz (v4):** grup özel olasılık, adil oran, değer işareti, galop, profil notu |
| `scripts/model5.py` | v5 modelini (kronolojik, jokey, koşu türü) eğitir ve test eder: `model5.py sonuc program 2026-10-19 cikti.json 1000 tur` |
| `scripts/model.py` | v4 modeli (eski) |
| `scripts/kosu_jokey.py` | Koşu türü, cinsiyet ve jokey analizi |
| `scripts/jokey_kalicilik.py` | Jokey avantajı kalıcı mı testi |
| `scripts/profil.py` | Irk × zemin × mesafe profilleri ve kulvar etkisi |
| `scripts/program_indir.py` | Geçmiş program CSV'lerini indirir |
| `scripts/analiz2.py` | Günün programını puanlar: HP, s20, form, pist uyumu, baba ve kısrak babası kanı, galop |
| `scripts/geritest.py` | Modelleri geçmiş sonuçlarda sızıntısız karşılaştırır |
| `scripts/analiz_v1.py` | İlk basit model |
| `veri/model.json` | v4 ağırlıkları + aygır ve kulvar tabloları |
| `veri/irk_zemin_mesafe_profil.txt` | Grup profilleri tablosu |
| `veri/aygir_istatistik.json` | 180 günlük aygır tablosu (18.11.2026) |

## Kullanım

```bash
python3 scripts/sonuc_indir.py veri/sonuc 180
python3 scripts/aygir_stat.py veri/sonuc veri/aygir_istatistik.json
# günün programı: tjk.org günlük program sayfası (HTML) + CSV
python3 scripts/idman.py program.html idman.json
python3 scripts/analiz3.py program.html program.csv veri/model.json veri/irk_zemin_mesafe_profil.json İstanbul idman.json veri/kosu_turu_jokey.json
```
