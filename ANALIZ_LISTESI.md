# Analiz listesi (her koşu için, −12 dk, otomatik)

Kullanıcının 28.11'de verdiği liste. Her koşu için `veri/analiz_listesi/<gün>/<hipodrom>_<koşu>.md` dosyasında atlar piyasa sırasıyla bu 12 bölümle yazılır (`scripts/son_dakika_ozet.py`; veri `scripts/hipodrom_sicil.py` günlük çıktısı `veri/hipodrom_sicil/<gün>_analiz.json` ve program CSV, eBayi görüntüleri).

| # | Analiz | Kaynak |
|---|---|---|
| 1 | Çim / kum / sentetik tablosu (tüm hipodromlar, start/gal/ilk 3), hipodrom adı yok | at_gecmisi |
| 2 | Çimden kuma / kumdan çime geçiş (bu zeminde ilk kez) | at_gecmisi, program |
| 3 | Kilo avantajı: kilo, sahada sıra, en ağırdan fark, son koşuya göre kg, apranti | program, at_gecmisi |
| 4 | Atın hipodrom sicili (start/gal/ilk 3) ve liste çarpanı | hipodrom_sicil.py |
| 5 | Soyların uzun / orta / kısa mesafe durumu (at, baba, anne babası) | mesafe_tipi.py |
| 6 | Mesafe artmış mı azalmış mı; bu mesafede (±200 m) ne kadar koşmuş, uzun / kısa sicil | hipodrom_sicil.py |
| 7 | Çimi seven / kumu seven (zemin tercihi) | at_gecmisi |
| 8 | Para girişleri / çıkışları (ganyan −60 → −30 → şimdi) | eBayi görüntüleri |
| 9 | AGF yükselen / düşen (sabah → şimdi) | eBayi görüntüleri |
| 10 | Sabah AGF – öğleden sonra AGF (12:00 TR) – şimdi | eBayi görüntüleri |
| 11 | Jokey değişimi (önceki, bugünkü, değişti mi) | program, at_gecmisi |
| 12 | At kalitesi, bu grupta denge: HP, grup ortalaması/std/aralık, HP sırası | program |

**Listeden çıkarılanlar:** Bursa pist yönü (28.11, kullanıcı kararı; yön sabit, etki yok). Çim/kum tablosu artık hipodrom adına bağlı değil, her koşuda tüm atlar için.

Bu liste bilgi içindir. Liste çarpanı yalnızca madde 4'te (hipodrom sicili) uygulanır; diğer maddeler çarpana girmez (mesafe çarpanı onay bekliyor).
