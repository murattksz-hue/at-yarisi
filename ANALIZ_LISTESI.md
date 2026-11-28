# Analiz listesi: tüm analizler, tek yerde (birleştirilmiş, 28.11)

Her koşu için `veri/analiz_listesi/<gün>/<hipodrom>_<koşu>.md` dosyası otomatik yazılır (−12 dk, `scripts/son_dakika_ozet.py`): önce mevcut kart (bölüm 0), sonra 15 bölüm. Veri: `veri/hipodrom_sicil/<gün>_analiz.json` (günlük, `hipodrom_sicil.py`), `<gün>_mesafe.json`, `<gün>.json`, program CSV, eBayi görüntüleri. Hiçbir eski analiz silinmedi; aynı olanlar birleştirildi, eksik olanlar eklendi. Testlerin sonuçları ve durumları `ANALIZ_INDEKSI.md`'de.

## Koşu başına dosyadaki bölümler

| Bölüm | Analiz | Eski mi / yeni mi | Not |
|---|---|---|---|
| Üst satır | Koşu çeşidi, mesafe, zemin, at sayısı, 1. ikramiye | YENİ | program CSV |
| 0 | Piyasa %, sabah AGF, ganyan −60 → şimdi, v9 AGF'li / AGF'siz, BİRLEŞİK_10 (sicil çarpanlı), işaretler (💰📈📉⚖🤫🎯), favoriler, açık koşu riski ve liste (3/4/5), mesafe tercihi (kendi + baba bantları), koşu çeşidi tarihsel ve canlı sicil | ESKİ (korundu) | mevcut kart aynen gömülü |
| 1 | Çim / kum / sentetik tablosu (tüm hipodromlar) | YENİ | |
| 2 | Çimden kuma / kumdan çime geçiş, bu zeminde ilk kez | YENİ | gün sonu `gozden_kacan_ozellik` zaten ölçüyor |
| 3 | Kilo avantajı: kilo, sahada sıra, en ağırdan fark, son koşuya göre, apranti | YENİ | |
| 4 | Hipodrom sicili (start/gal/ilk 3) ve liste çarpanı | YENİ | BİRLEŞİK_10'a uygulanıyor |
| 5 | Soyların uzun / orta / kısa mesafe durumu: at, baba, anne babası | YENİ | `mesafe_tipi.py` |
| 6 | Mesafe artmış mı azalmış mı; bu mesafede (±200 m) ve uzun / kısa sicil | YENİ (0'daki mesafe tercihiyle birlikte okunur) | |
| 7 | Çimi seven / kumu seven atlar | YENİ | |
| 8 | Para girişleri / çıkışları (ganyan −60 → −30 → şimdi) | ESKİ 💰'nın genişletilmişi | 0'daki 💰 ile aynı eşik |
| 9 | AGF yükselen / düşen (sabah → şimdi) | ESKİ 📈📉'nin genişletilmişi | |
| 10 | Sabah AGF – öğleden sonra AGF (12:00 TR) – şimdi | YENİ | |
| 11 | Jokey değişimi (önceki, bugünkü) | YENİ (eski işaret yalnızca bayrak) | soyad + ilk harf eşleşmesi |
| 12 | At kalitesi, grupta denge: HP, grup ortalaması / std / aralık, HP sırası, son koşuya göre HP | YENİ | |
| 13 | Yaş / cinsiyet, kulvar, KGS, son 6 yarış, takı, antrenör, ekuri | YENİ (eksik olanlar tamamlandı) | |
| 14 | Form ve sınıf: tabela (son 8 ort. sıra), son koşu, tür değişimi, ilk kez hipodrom / mesafe / zemin | YENİ (eksik olanlar tamamlandı) | |
| 15 | Baş-başa (h2h) skoru ve BİRLEŞİK % | ESKİ (kartta yoktu, eklendi) | |

## Gün sonu ve ayrı raporlar (silinmedi)

| Analiz | Dosya |
|---|---|
| Gözden kaçan kazananların özellikleri (yaş, cinsiyet, kulvar, kilo, kilo sırası, HP, zemin geçişi, hipodrom sicili ...) | `veri/gozden_kacan_ozellik.md` |
| Hata raporu, büyük hatalar, favori yıkılması | `veri/hata_raporu/<gün>.md` |
| Puanlama (BİRLEŞİK_10, piyasa, v9) | `veri/tahminler_10dk/SONUC.md` |
| Koşu çeşidi tablosu | `veri/kosu_tipi_rapor.md` |
| Soy tercihi (aygır × mesafe / pist / çeşit) | `veri/soy_tercih.md` |
| Koşu riski modelleri | `veri/kosu_riski.md`, `veri/kosu_riski_v2.md` |
| Hipodrom ve mesafe sicili testleri, apranti ve kilo testi | `veri/hipodrom_galibi_testi.md`, `veri/mesafe_sicil_testi.md`, `veri/apranti_kilo_testi.md` |
| Atların mesafe tipleri (baba, anne babası) | `veri/mesafe_profil/` |
| yenibeygir Blt – AGF karşılaştırması (elle) | `veri/yenibeygir_el_kayit/` |

## Henüz koşu dosyasında olmayanlar

- Hava / pist durumu (hava etkisi küçük çıkmıştı; koşu dosyasına eklenmedi).
- Mesafe sicili liste çarpanı (test sonucu var, onay bekliyor).
- Hipodrom ve mesafe çarpanının birlikte testi.

**Listeden çıkarılan:** Bursa pist yönü (kullanıcı kararı, yön sabit, etki yok). Çim / kum tablosu artık hipodrom adına bağlı değil.

## Koşu riski (geçmişten öğrenilen, her koşu dosyasının başında)

`veri/analiz_listesi/<gün>/<hip>_<koşu>.md` en üstte "Koşu riski" bölümünü taşır: (1) piyasada %10 altı atların payı (şimdi), (2) v2 modeli (`kosu_riski_v2.py`, geçmiş koşulardan eğitilmiş: kazananın piyasa ilk 3 ve ilk 4 dışından gelme olasılığı), (3) geçmiş segment oranları (`kosu_riski_gecmis.py` → `veri/kosu_riski/gecmis_segment.md`: hipodrom, çeşit + ırk, mesafe, at sayısı, zemin, kombinasyon; favori kazandı, ganyan>=10 kazanan, kazanan ilk 3 dışı). Sınıf iki ölçüden riskli olandır; liste 3/4/5 at; tek at yalnızca düşük risk ve favori >=%50. Günlük adım: `agf_plan.py` 2b (`mesafe_tipi`, `hipodrom_sicil`, `kosu_riski_gecmis`, `kosu_riski_v2`), veri `veri/kosu_riski/<gün>.json`.
