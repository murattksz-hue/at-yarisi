# Analiz indeksi (yeni oturum önce bunu oku)

**Her koşu için canlı analiz listesi (hepsi birleştirilmiş): `ANALIZ_LISTESI.md`, çıktı `veri/analiz_listesi/<gün>/`.** `BILGI.md` ayrıntılı günlük (tarihli bölümler, ~1000 satır); bu dosya ne bulduğumuzu **tek bakışta** verir. Durum: ✅ sağlam, ◐ işaret var kanıtlanmadı, ❌ etkisiz/geçersiz, ↩ geri çekildi. Her satırın ayrıntısı için `BILGI.md`'de bölüm başlığını ara.

## 1. Ana sonuç
Piyasa (kapanış ganyan/AGF) iyi kalibre ve güçlü; hiçbir modelimiz piyasayı kanıtlanmış biçimde geçemedi, düz oyun getirisi ~%70–80 (kesinti). Hedef: tahminlerimizi kaydedip hatamızı bulmak, "gözden kaçan kazanan"ın nedenini anlamak. Dış projelerin dürüst sonuçları da aynı (fatihbozdag/Ganyan, pedigreeall-ai: ROI negatif).

## 2. Modeller (`scripts/model*.py`, `analiz3.py`, test: 542 görülmemiş koşu, kronolojik)
| Model | Sonuç |
|---|---|
| v4–v6 (koşullu logit; HP, form, soy, kulvar, jokey, hava) | v5/v6 piyasa (AGF) log-olabilirliğine yakın (v6 −1,855 / AGF −1,868); hava etkisi küçük ◐ |
| v8, v9 (+hız puanı, pist-mesafe galibi, galop, karma koşuda dişi) | **v9 AGF'li** LL −1,846, 1. seçim ~%32,8, ilk 3 ~%66,4; **AGF'siz** LL −1,956, 1. seçim %30,4, ilk 3 %59,6. Piyasa favorisi %34,5–35,5. Değer bahsi getirisi ≤%101 ◐ |
| v9 + uzun geçmiş (2024) | fayda yok (gürültü); AGF'siz basit testte +0,0084, v9'da tekrarlanmadı |
| BİRLEŞİK (piyasa + 0,5×baş-başa; `tahmin_birlesik.py`, `tahmin_10dk.py`) | piyasayla pratikte aynı seçim; 26.11 14 koşu: ilk seçim 5/14 |

## 3. Tek tek etkenler (piyasanın ötesinde bilgi var mı?)
| Etken | Sonuç | Script / bölüm |
|---|---|---|
| Jokey | beceri farkı büyük ama piyasa biliyor (kalıcılık r −0,02) ❌ | `jokey_kalicilik.py` |
| Antrenör, sahip, form, soy (baba kanı), ıslak/kuru zemin | çoğu piyasada fiyatlı ❌/◐ (küçük katkılar) | `ozellik_test*.py`, `soy_*.py` |
| Aygır/baba × mesafe/pist/çeşit | birkaç hücre güçlü (Kayayürekli Handikap 1,57; Good Curry Kum 1,42 …) ama çoklu karşılaştırma, canlı sınav bekliyor ◐ | `soy_tercih.py` → `veri/soy_tercih.md` |
| Atın/babanın mesafe profili (en son test, tam veri) | **piyasanın ötesinde bilgi yok**; uzun atlarda yalnızca kötüleri ayıklıyor (baba bantta kötü A/E 0,87) ❌ | `mesafe_profil_testi.py` |
| Anne babası / anne | ek bilgi yok ❌ | aynı betik |
| Baş başa (h2h) | A/E 1,13 (z +7,3) lider, ama log-kazanç anlamsız ◐ | `bas_basa.py`, `ozellik_ekleme_testi.py` |
| Tabela, aynı jokey, kilo farkı, uzmanlık, orta kilo | anlamsız ❌ | `ozellik_ekleme_testi.py` |
| Sınıf düşüşü, ilk kez hipodrom/mesafe/yüzey, mesafe değişimi, jokey değişimi, takı | zayıf/etkisiz ❌ (yüzeyde ilk kez A/E 1,09 ama kararsız ◐) | `sinif_dusus.py`, `ilk_kez_test.py`, `yuzey_ilk.py` |
| Cinsiyet kodları | e/d = genç, a/k = 4+, g = iğdiş (veriyle doğrulandı) | `cinsiyet_analiz.py` |
| Koşu ikramiyesi | at sayısı/sınıf vekili, ek bilgi yok ❌ | `ikramiye_analiz.py` |
| Altılı ödemesi | ödeme ~ ganyan çarpımı (r 0,93); devir/havuz verisi yok | `altili_ikramiye.py` |
| Hipodrom kalibrasyonu | İzmir (0,74), Antalya (0,73), Adana (0,82): uzun atlar fazla fiyatlı ◐ | `surpriz_nerede.py` |
| Egzotik (ikili/sıralı ikili) | getiri %77–92, değer yok ❌ | `ikili_test.py`, `harville_test.py` |
| Shin yöntemi | ganyanda kötü ❌; basit güç (k=1,05) küçük anlamlı iyileşme | `olasilik_donusumu.py` |

## 4. Uzun atlar / "gözden kaçan kazananlar" (p<%10, ganyan ≥10 ya da AGF <%10)
- Genel A/E 0,93 (piyasada fazla fiyatlı; ganyan 40+ 0,62). Tanımlar: G (ganyan ≥10), A10, A5, AS10 (`surpriz_ayri.py`, kartlar `veri/agf_kayit/<gün>/SURPRIZ.md`).
- Kayıtlı özellikler (tipik uzun ata göre göreli A/E, `gozden_kacan_ozellik.py` → `veri/gozden_kacan_ozellik.md`): HP rakiplere yakın/yüksek 1,10/1,05; HP düşük 0,86; aygır 1,07; genç dişi 0,90; handikap 1,06; mesafesi kısalan 1,06; iç start 1,05; Diyarbakır 1,21; 90+ gün ara 0,82; ilk koşu 0,89; yaş/jokey değişimi ayırt etmez ◐ (etki ±%5–15).
- **Düzeltilmiş artık-modeli** (`gozden_kacan_model.py`; piyasa logit'i sabit, LightGBM): test log-kaybı +0,0013 (anlamlı, küçük); onluk dilimlerde A/E 0,34 → 1,30; **ROI hâlâ negatif** (en iyi %10: −%9, tüm uzun atlar −%40). Tek gizli faktör yok, çok küçük etki. ◐
- **Kilo sırası ve zemin geçişi (27.11 eklendi, `gozden_kacan_ozellik.py`):** uzun atlar içinde en ağır at göreli A/E 1,00 (fark yok), sahanın en hafif 3 atı 0,94; ilk kez çime çıkan 1,14 (z +2,2), ilk kez kuma çıkan 0,83 (z −2,7), ikisi de çoklu karşılaştırmada zayıf ◐ (canlı sınav bekliyor). Handikap tüm atlarda kilo sırası piyasa ötesi bilgi vermedi (A/E 0,98 / 1,03 / 0,99) ❌.
- **Apranti jokey ve kilo (27.11, `apranti_kilo_testi.py` → `veri/apranti_kilo_testi.md`; işaret ebayi `APRANTIKILOINDIRIMI`):** apranti A/E 0,97 (z −2,2), handikapta 0,94 (z −2,4), piyasada hafif fazla fiyatlı; apranti × sahanın en ağır 3 atı (handikap, fark ≥8 kg) A/E 0,84 (z −4,2); kilo indirimi büyüklüğü 4+ kg'da 1,01; kilo farkı ≥8 kg'da en ağırdan 7,5+ kg altı 0,95 (Bursa 0,91, z −1,3). Apranti, gözden kaçan kazananı artırmıyor (at başına %1,73'e karşı %1,51 normal). Piyasanın ötesinde avantaj yok ❌/◐.
- **Koşu riski modeli (27.11, `kosu_riski_modeli.py` → `veri/kosu_riski.md`):** koşunun kazananının ganyan ≥10 olma olasılığı; piyasa riski (p<%10 payı) + at sayısı + favori payı + hipodrom/çeşit/ırk/mesafe/zemin; test (2025-07 sonrası) AUC 0,656 = yalnızca piyasa riski ve at sayısı (0,656): ek katkı yok. İlk sürümde Arap koşuları İngiliz sayıldığı için bozuktu, düzeltildi ✅.
- **Koşu riski v2 (27.11, `kosu_riski_v2.py` → `veri/kosu_riski_v2.md`):** hedef = kazananın piyasa ilk 3 dışından gelmesi (3 atlık liste kaçırır). LightGBM, özellikler: piyasa riski, at sayısı, favori payları, entropi, HP/kilo yayılımı, ırk, mesafe, zemin, hipodrom, çeşit, saat. Test (2025-07 sonrası) AUC 0,648 (yalnız piyasa riski 0,597): gerçek iyileşme. Tersil kaçırma oranı düşük/orta/yüksek %19/%33/%44 (eski %25/%29/%41). Gözden kaçan kazanan (ganyan≥10) hedefinde fark yok (0,655/0,648). Kural: iki ölçü çelişirse riskli olanı al ✅.
- **Hipodromda önceki galibiyet (27.11, `hipodrom_galibi_testi.py` → `veri/hipodrom_galibi_testi.md`):** tüm atlarda bu hipodromda daha önce kazanmış A/E 1,03 (z +3,2), kazanmamış 0,97 (z −3,4), iki yarıda aynı. Orta ve favori gruplarında +%3–4; uzun atlarda hipodromda galibiyeti olmayanlar piyasada fazla fiyatlı (A/E 0,88), galibiyeti olanlar 0,97. Aynı mesafede ±200 m galibiyet daha zayıf (1,02). Küçük ama tutarlı etki, piyasanın ötesinde ROI kanıtı yok ◐.
- **Hipodromda galibiyet oranı ≥%30 (en az 3 start):** tüm atlarda A/E 1,08 (z +5,1, iki yarıda 1,08/1,08), orta 1,07, favori 1,09, uzun atlarda 1,01 (diğer uzun atlar 0,92). Bu hipodromda 2+ galibiyet: 1,02. En güçlü hipodrom etkisi ◐ (ROI kanıtı yok; çoklu karşılaştırma).
- **Mesafe sicili (28.11, `mesafe_sicil_testi.py` → `veri/mesafe_sicil_testi.md`, 290.707 at-koşu):** bugünkü mesafe ±200 m'de >=3 start ve galibiyet oranı >=%30: A/E 1,06 (z +4,4, iki yarıda 1,07/1,06; orta 1,07, favori 1,06); ilk 3 oranı >=%50: 1,04 (z +4,5); kısa mesafe günü kısa sicil iyi 1,05 (z +3,9); uzun mesafe günü uzun sicil iyi 1,05 (z +2,6, yarılar 1,07/1,02 zayıflıyor). Olumsuz: kısa mesafe günü kısa sicil kötü (>=4 start ilk 3 yok) 0,90 (z −2,2), orta grupta 0,80; uzun atlarda (p<%10) bu mesafede hiç koşmamış 0,87 (z −3,6) ve >=3 start hiç galibiyet yok 0,92 (z −3,5). Etkiler küçük (%4–8) ama iki yarıda tutarlı ◐; çarpan henüz uygulanmadı.
- Koşu düzeyi: **açık koşu riski** = piyasada p<%10 atların payı (≤0,198 düşük, ≤0,31 orta, üstü yüksek); liste 3/4/5 at (geçmişte kazananı yakalama %77/%81/%76).
- ↩ **Geri çekilenler:** "HP ilk 3 + AGF≥1,3× + ganyan≥10 → getiri %127" ve ilk SHAP bulguları (hp_fark +0,266 …) **HP sırası eşitlik sızıntısı** yüzündendi; 🎯 işareti (mesafeye uyumlu + baba olumlu) tam veriyle A/E 0,98 çıktı, dayanağı yok.

## 5. Koşu çeşidi ve kaç at
- Çeşitler: Maiden, Şartlı 1–5 (19/27), Handikap 13–24, KV 6–9, Satış, Grup (`kosu_tipi.py`, `kosu_turu_analiz.py`). Favori kazanma: Şartlı İngiliz %40, Handikap %34, Arap Handikap %29 …
- Canlı çeşit tablosu `veri/kosu_tipi_rapor.md` (gün sonu otomatik), kayıt `veri/kosu_tipi_kayit.csv`.

## 6. AGF / veri altyapısı
- TJK CSV AGF'si ile ebayi AGF'si aynı veri (12:15'ten sonra fark 0,02–0,16); ilk yayında senkron değil. İlk yayın kısmi → **TAM** (≥%90 dolu) ~4–22 dk sonra; AGF TAM'dan 15–20 dk sonra yerleşiyor (TAM anında kapanışa göre 1,8–5,5 puan oynak). Dondurma TAM+15 dk, en son dolu görüntü.
- Kapanış AGF geçmişi `at_gecmisi`'nde 2020'den beri (altılıya giren atlarda %63–88). Koşu öncesi hareket (−60/−30/−12/−10/−3 dk) yalnızca 19.11.2026'dan beri.
- Son 5 dk bilgisi taşır (JRA çalışması), ama bizde −3 dk görüntüsü var; −10…−60 dk görüntülerinin kapanışa göre farkı 97 koşuda anlamsız (−0,045 [−0,10, +0,01]).
- 💰 ganyan düşüşü ve 📈/📉 AGF hareketi: **test edilmedi** (≥500 koşu gerek), yanıltıcı olabilir (kullanıcı uyarısı, Lodato/Angel On The Right örnekleri).

## 7. Kaynaklar (durum)
| Kaynak | Durum |
|---|---|
| TJK CSV (`medya-cdn.tjk.org`), ebayi.org JSON | ana kaynak, açık |
| pegadrom.com | galop (kullanılıyor); sonuç sayfalarında AGF yok |
| yenibeygir.com | ToS otomatik çekimi yasaklıyor; yalnızca elle/seyrek; "Blt" = Bülten Ortalama Puanı (AGF'den bağımsız ama ilişkili, 26.11 İzmir) |
| agftablosu.com, agftahmin.com, liderform | Cloudflare 403 (bot korumasını aşma) |
| ganyantime2.com | geçmiş AGF arşivi yok, otomatik toplu erişim sözleşmeye aykırı |
| tjk.org idman, aygır istatistik | otomatik isteğe 403 |
| Tavily | anahtar ortamda (`api.tavily.com`), arama çalışıyor; bot engeli olan sitelerde extract yasak sayıldı |

## 8. Canlı sicil
- 26.11 (14 koşu): kazanan listede 14/14, ilk seçim BİRLEŞİK_10 5, piyasa 5, v9 AGF'li 7, v9 AGF'siz 6; ganyan getirisi tüm liste %100, ilk seçim %80; gözden kaçan kazanan 1 (Çelikgiller 10,80, listede 4.). Küçük örnek; kol üstünlüğü kanıtlanmaz.
- Günlük raporlar: `veri/tahminler_10dk/SONUC.md`, `veri/hata_raporu/<gün>.md`, `veri/son_dakika/<gün>/`.

## 9. Bilinen tuzaklar
Eşitlikte sıra yok (HP sırası sızıntısı); f-string tek tırnak; Actions CSV'lerine elle yazma çakışması (kullanıcı onayı olmadan yazma); sonuç dosyaları bitiş sırasında dizili; `python3 -I` ile sys.path; konteyner yeniden başlayınca arka plan süreçleri ölür.
