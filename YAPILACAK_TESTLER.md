# Yapılacak testler

Son güncelleme: 22.11.2026. Kullanıcı: "Yapılması gereken testleri yap dediğimde hepsini yaparsın." Bu dosya o liste.

## Nasıl çalışılır (sonraki oturum için)

1. Yeni oturum aç, bu dosyayı ve `BILGI.md`'yi oku. Önce hangi maddenin gerçekten yapılmadığını `BILGI.md`'de ara (tekrar test etme).
2. Her madde için: kopyada dene, sonucu **güven aralığı / z / iki yarı** ile ver, `BILGI.md`'ye tarihli kısa bölüm yaz, betiği `scripts/` altına koy, bu dosyada maddeyi `✅` yap ve sonucu bir satırla yaz, commit + push.
3. Ölçüt standardı (tüm maddelerde): beklenen = piyasa; **A/E** (gerçek/beklenen), z, ilk/ikinci yarı tutarlılığı, düz oyun getirisi. Çok segment denenirse **|z|≥3** ve iki yarıda aynı yön olmadan "bulgu" deme. Özellik eklemeyi **mevcut v9'a eklenince katkı** (log kaybı, bootstrap %95 aralık) ile ölç, tek başına değil.
4. Kurallar: dondurulmuş tahminlere (`veri/tahminler/`) dokunma. Actions'ın yazdığı CSV'leri (`para_takip`, `kazanan_profil`, `canli_takip*`, `agf_kayit`) elle yazma, yalnızca oku. Yeni sonuç dosyaları yeni adla. Push çakışırsa `pull --rebase --autostash -X theirs`.
5. Kota: bu işleri yeni, kısa oturumda yap. Uzun sohbet geçmişi taşıma.
6. Başkasının lisanssız kodunu kopyalama (`nino0435/ganyan-model`, `buyhan-lab/kosai-at-yarisi-analiz`): yalnızca yöntem fikri, kod sıfırdan.

---

## A. Veri hazır, hemen yapılabilir

**1. Hata raporu** (`scripts/hata_raporu.py`, yeni)
- Amaç: sürprizlerin neden geldiği, bizim neyi gözden kaçırdığımız; diğer koşularda hata arama.
- Girdi: `veri/kazanan_profil.csv`, `veri/canli_takip.csv`. Sürpriz ayrımı için `scripts/surpriz_ayri.py` hazır (kartlar `veri/agf_kayit/<tarih>/SURPRIZ.md`); hata raporu bunun üstüne kurulabilir.
- Çıktı: `veri/hata_raporu/<tarih>.md`, gün sonu `agf_plan.py` çağırır (`agf_dogruluk.py` gibi).
- İçerik: (a) her sürpriz kazanan için piyasadan ayrıldığı yönler ve bizim modelin ona verdiği sıra, nedenleri "olası neden" diye etiketle; sürprizi kendi **segmentinin beklenen oranıyla** (`surpriz_nerede.py`, at sayısı/hipodrom/tür) kıyasla; (b) büyük hatalar: kazananın model sırası ≥4 ya da ilk seçimimiz ≥5. bitmiş; ortak özellikleri say; (c) üstte günlerin toplam tablosu.
- Not: örnek az (45 kazanan, 7 sürpriz); yorumları "olası" yaz, sağlam sonuç için geçmiş veriyle (`veri/at_gecmisi`) test et.

**2. Sürpriz tanımı: ganyan ≥10 mı AGF mi?** (karar bekliyor, şimdilik DEĞİŞTİRME)
- `kazanan_profil.py` şu an ganyan ≥10. Aday: AGF %10 altı (≈ilk 4 dışı) ve büyük sürpriz AGF %5 altı (`scripts/agf_surpriz.py`, `BILGI.md`'ye bak).
- Test: iki tanımla sürpriz profillerini (jokey değişimi, AGF hareketi vb.) kıyasla, hangisi daha ayırt edici. Kapanış AGF yerine **sabah ve −60 dk AGF** ile sınıflama ne kadar değişiyor.
- Karar kullanıcıdan alınmadan canlı kayıt sistemine dokunma.

**3. SHAP'ı doğru kur** (`scripts/taslak_kalibrasyon_shap.py` taslak, uyarıyı oku)
- Önce yaş sütunundaki ikinci/üçüncü harfin anlamını doğrula (cinsiyet mi renk mi, ırk mı). Sonra özellikleri düzelt, kategorikleri hash yerine doğru kodla.
- Gerçek v9 özellikleriyle (`veri/model.json`: 27 özellik) SHAP: sürpriz kazananlarda hangi özellikler modeli yukarı/aşağı itti. Sürpriz örnek sayısını artır (≥1000 koşu testi).
- Gereksinim: `pip install scikit-learn shap` (Actions'a ekleme, yalnızca elle).

**4. Kalibrasyon betiğini repoya al ve modele uygula**
- Piyasa kalibrasyonu repoda (taslak içinde): ganyan <%2 A/E 0,69, %2–4 0,86, orta 1,0, favori 1,05; izotonik düzeltme fayda sağlamadı (Brier 0,07893→0,07895).
- Yapılacak: v9'un **kendi olasılıklarının** kalibrasyonu (AGF'li ve AGF'siz), tahmin dosyaları/`geritest.py` çıktısıyla, görülmemiş dönemde; scikit-learn `calibration_curve`, Brier, izotonik/Platt.

**5. Baş-başa, tabela ortalaması, aynı jokey, "orta kilo"** (kosai makalesindeki fikirler, `BILGI.md`'de YOK)
- Fikirler (kendi verimizle sıfırdan): (i) son 8 koşunun bitiş ortalaması en düşük at (tabela), (ii) önceki koşuyla aynı jokey, (iii) handikapta yaş grubu içinde kategoriye özel "orta kilo", (iv) atın bu kategori/mesafe/hipodromda geçmiş top-3 oranı ≥%50 (`pist_mesafe_galibi` ile örtüşebilir, katkıyı ölç), (v) baş-başa üstünlük.
- Ölçüt: v9'a eklenince 542+ görülmemiş koşuda log kaybı değişimi + bootstrap aralığı. Makaledeki "havuz-yakalama %75–83" rakamlarını **kullanma** (havuz büyüklüğü olmadan yanıltıcı); ölçüt havuz içi değil, olasılık kalitesi.
- Zaten yapılmış, tekrarlama: antrenör, jokey hipodrom uzmanlığı, ilk kez hipodrom/mesafe/yüzey, mesafe değişimi, sınıf farkı, soy, kulvar.

**6. Altılı ikramiye / devir testi** (`nino0435/ganyan-model` fikri, `BILGI.md`'de YOK)
- Fikir: ikramiye sürprizle büyür (log-ikramiye eğimi negatif, R² 0,90 raporlanmış, doğrulanmadı). Kendi verimizle: sonuç dosyalarındaki altılı ikramiye ve havuz (Tevzi) ile ikramiyeyi modelle; **devreden günlerde** beklenen getiri farklı mı.
- Ölçüt: günlük altılı beklenen getirisi (kesinti dahil) ve devir etkisi, bootstrap aralığı.

**7. Net piyasa testini koşudan ÖNCEKİ oranla yinele** (`scripts/net_piyasa.py` kesin ganyan kullanıyor)
- Karar anındaki oran (−60 dk) ile favori–ikinci farkı ve isabet/getiri. Elimizdeki −60 dk ganyan (`para_takip.csv`) yeterli sayıya ulaşınca yap (≥500 koşu).
- Eski sonuç: net piyasa yalnızca daha yüksek olasılık demek, ek bilgi yok; her aralıkta düz oyun getirisi negatif.

**8. Yüzey testini tam geçmişle yinele**
- `scripts/yuzey_ilk.py`: ilk kez yeni yüzeyde A/E 1,09 (z 2,3) ama ilk yarı 1,14, ikinci 1,03. Geçmiş 2024'ten başlıyor, 2022–2023 eksik; daha uzun geçmiş bulunabilirse "ilk kez" doğruluğu artar, sonra yinele.

## B. Veri birikmesini bekleyenler (önkoşul sağlanınca yap)

**9. TJK önbellek düzeltmesi sonrası TJK ↔ eBayi karşılaştırması** (düzeltme 22.11 öğleden sonra)
- Önkoşul: ≥7 gün düzeltmeli veri. `DOGRULUK.md`'yi yeniden değerlendir; "hangisi doğru/ önde" artık önbellek yüzünden TJK'yı geri göstermiyor mu. Önceki günleri (düzeltme öncesi) ayrı raporla ve karıştırma.

**10. İlk yayınlayan tespiti (08:00 penceresi)**
- Önkoşul: ≥10 gün `ilk_zaman.json`. Hangi kaynak önce yayınlıyor, saat dağılımı, hipodrom bazında. Kontrol aralığı 5 dk; yeterince kısa mı (1–2 dk) karar ver.

**11. Oran hareketi (💰/🤫, sabah→−60→−30→−10)**
- Önkoşul: ≥500 koşu −60/−30/−10 görüntüsü ve ≥50 sürpriz. Hareket (AGF ve ganyan) kesin sonuca ek bilgi taşıyor mu: A/E, bootstrap, iki yarı. Bizim özel verimiz, en umutlu madde.

**12. Model ↔ AGF güven aralığı**
- `veri/agf_kayit/GUVEN_ARALIGI.md` (gün sonu otomatik). Önkoşul ≥300 koşu: AGF'li ve AGF'siz v9 AGF favorisinden anlamlı iyi mi (46 koşuda aralık sıfırı kapsıyor).

**13. Model ayrışma testi: AGF'li ↔ AGF'siz ilk seçim farklı olunca kim haklı**
- Önkoşul ≥100 ayrışan koşu (`veri/tahminler/*` ve `canli_takip*.csv`). 22.11'de ayrışanlar: İzmir 1, 2, 4, 7, 8; Adana 6, 8 (sonuçlar akşam `canli_takip.csv`'de).

**14. Sürpriz segment A/E kalıcılığı** (`scripts/surpriz_nerede.py`)
- İzmir (A/E 0,82; ikinci yarıda 0,75) ve Antalya (0,78) uzun atları abartıyor; 1 ay sonra yeni verilerle yinele, kalıcı mı (z≤−3 iki yarıda).

## C. Altyapı / veri kalitesi

**22. İlk yayın KISMİ geliyor: `ILK` görüntüsü ile "sabah AGF" ayrı tanımlanmalı** (öncelikli, 25.11'de bulundu)
- 08:00 penceresi AGF'nin ilk yayınını yakalıyor (09:01–09:06), ama o an atların çoğunda AGF henüz %0 (23.11 Şanlıurfa: 104 attan 33'ü dolu). `ILK_*.csv` "ilk yayın saati" için doğru, "sabah AGF" değeri olarak yanlış.
- Yapılacak: ilk görüntüyle birlikte **"ILK_TAM"** (≥%90 atın AGF'si dolu ilk görüntü) ya da sabit bir sabah saati (örn. 10:00) kaydet; `kazanan_profil.py`'deki `agf_sabah`, `agf_fark`, `agf_artis_sira`, 💰/🤫 işaretlerini ona bağla. 23.11 ve sonrası kayıtlar bu açıdan güvenilmez (22.11 ve öncesi 09:15'te alındığı için dolu).
- Geçici: `surpriz_ayri.py` doluluk <%80 ise AS10 vermiyor ve uyarı yazıyor.
- Not: bu, `agf_kayit.py` (canlı kayıt sistemi) değişikliği, kullanıcıdan onay al.

**15. Veri sağlık kontrolü** (kosai makalesindeki "veri toplama hatası" dersi)
- TJK CSV'de AGF sütunu 10. indekse bağlı, ganyan/AGF/HP sütunu kayarsa fark edilmiyor. Günlük kontrol: "AGF toplamı ~%100 mü", "ganyan = HP oranı %0'a yakın mı", "at sayısı makul mü"; sapma olursa `GUNLUK.md` başına uyarı.

**16. Ganyan 999.99 yer tutucusu**
- Analiz çıktısında bazı atlar için `ganyan 999.99` görülüyor (22.11 İzmir 1). Erken saatte havuz açılmamış olabilir; olasılık/değer hesabına girmediğini ve `kazanan_profil` kaydına yanlış sızmadığını doğrula.

**17. Dondurma zamanı < koşu saati doğrulaması** (ileri test koruması fikri)
- `canli_takip.py` yalnızca koşudan ÖNCE dondurulmuş tahminleri saysın: dosya zamanı ile koşu saatini karşılaştıran açık bir kontrol ekle ve rapora "geçerli koşu sayısı" yaz.

## D. Düşük öncelik / isteğe bağlı

**18. "Piyasa net/kararsız" etiketini günlük rapora ekle** (bilgi amaçlı; strateji değil, getiri her aralıkta negatif).

**19. scikit-learn / XGBoost sıralama modeli** (`rank:pairwise`, koşullu logit karşılaştırması `statsmodels`): v9'a alternatif. Beklenti düşük (model ≈ piyasa), yalnızca yeni özellikler (madde 5, 11) eklenince anlamlı.

**20. `alibaba/open-code-review`**: gerekirse "delegation" modunda `agf_plan.py` gibi yoğun dosyalara kod incelemesi. Claude kotası yer; şimdilik gerek yok.

**21. Açık repoların fikir taraması (kullanıcı isterse):** `nino0435/ganyan-model` aylık yürüyen backtest yapısı (ay ay A/E tablosu, bootstrap), `shap/shap`, `scikit-learn`, `evidentlyai/evidently` (veri kayması izleme; madde 15 yeterliyse gerekmez).

---

## Tamamlananlar (referans)
- Piyasa kalibrasyonu (170 bin at), net piyasa, sürpriz nerede (segment A/E), AGF'ye göre sürpriz tanımı, yüzeyde ilk kez, mesafe değişimi/uyumu, ilk kez hipodrom/mesafe: sonuçlar `BILGI.md`.
- TJK CSV önbellek düzeltmesi ve güven aralığı betiği eklendi (22.11).
