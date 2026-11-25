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
- 25.11: Shin yöntemi denendi (✅, **kötü**, kullanma); basit güç dönüşümü p ∝ (1/g)^k, k=1,05 küçük ama anlamlı iyileşme (+0,0016), `scripts/olasilik_donusumu.py`. Kalan: v9'un kendi olasılıklarının kalibrasyonu ve k'yı canlı oranla (−60 dk) yeniden öğrenme.
- Piyasa kalibrasyonu repoda (taslak içinde): ganyan <%2 A/E 0,69, %2–4 0,86, orta 1,0, favori 1,05; izotonik düzeltme fayda sağlamadı (Brier 0,07893→0,07895).
- Yapılacak: v9'un **kendi olasılıklarının** kalibrasyonu (AGF'li ve AGF'siz), tahmin dosyaları/`geritest.py` çıktısıyla, görülmemiş dönemde; scikit-learn `calibration_curve`, Brier, izotonik/Platt.

**5. Baş-başa, tabela ortalaması, aynı jokey, "orta kilo"** (kosai makalesindeki fikirler, `BILGI.md`'de YOK)
- Fikirler (kendi verimizle sıfırdan): (i) son 8 koşunun bitiş ortalaması en düşük at (tabela), (ii) önceki koşuyla aynı jokey, (iii) handikapta yaş grubu içinde kategoriye özel "orta kilo", (iv) atın bu kategori/mesafe/hipodromda geçmiş top-3 oranı ≥%50 (`pist_mesafe_galibi` ile örtüşebilir, katkıyı ölç), (v) baş-başa üstünlük: **✅ tek başına test edildi (25.11, `scripts/bas_basa.py`): lider A/E 1,13 z +7,3, üç dönemde tutarlı, getiri −%18,9; sıradaki: v9'a ekleyip katkıyı ölç.**
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

**23. yenibeygir AGF'si AKŞAMDAN yayınlanıyor: ayrı takip** (25.11'de başladı, kullanıcı kararı)
- Amaç: (a) akşam AGF'si ne zaman ilk görünüyor, akşamdan sabaha değişiyor mu; (b) 09:00'da TJK/eBayi'nin ilk (kısmi) AGF'sinden ne kadar farklı; (c) **ilk yayımlanan AGF kapanışa göre daha mı doğru** (kullanıcı gözlemi, `BILGI.md` "ilk AGF" notu) ve sürpriz atlarda akşam AGF'sinde ne vardı (akşam→kapanış hareketi); (d) yenibeygir'in kaynağı.
- Ölçüt: kapanış AGF'ye ortalama mutlak fark (TJK/eBayi kesin AGF'ye karşı), favori aynı mı, A/E ve AGF hareketi; iki yarı, bootstrap. Not: yenibeygir tamsayı verir, karşılaştırmayı TJK/eBayi değerini tamsayıya yuvarlayarak yap.
- Kayıt düzeni (elle, düşük hacim): bir hipodrom sayfası = 1 istek (`/<tarih>/<hipodrom>`). Günde 2–3 anlık görüntü (önceki akşam ~21:00, sabah ~08:00, 09:30), satırlar `veri/yenibeygir_el_kayit/<tarih>.csv` dosyasına **eklenir** (`zaman_tr` sütunu ayırır; yalnızca at no, ad ve AGF sayısı). Kullanıcı "yenibeygir kaydı al" deyince yapılır.
- **Otomatik/zamanlı çekim EKLEME:** site kullanım şartları (madde 4) izinsiz otomatik taramayı yasaklıyor. Sürekli takip istenirse önce site sahibinden (İletişim sayfası) izin al. Repo açık olduğundan yalnızca sayılar tutulur, sayfa içeriği kopyalanmaz.
- İlk kayıt: 25.11 08:49 (Elazığ ve İstanbul; Elazığ 08:26 ile aynı, 0/96 değişim). Sıradaki karşılaştırma: bugün 09:05'ten sonra bizim ilk AGF'miz geldiğinde (`ILK_*`) bu değerlerle.

**22. ✅ YAPILDI 25.11 (TAM AGF, `BILGI.md` "TAM AGF düzeltmesi"); kalan: geçmişi onar. İlk yayın KISMİ geliyor: `ILK` görüntüsü ile "sabah AGF" ayrı tanımlanmalı** (öncelikli, 25.11'de bulundu)
- 08:00 penceresi AGF'nin ilk yayınını yakalıyor (09:01–09:06), ama o an atların çoğunda AGF henüz %0 (23.11 Şanlıurfa: 104 attan 33'ü dolu). `ILK_*.csv` "ilk yayın saati" için doğru, "sabah AGF" değeri olarak yanlış.
- Yapılacak: ilk görüntüyle birlikte **"ILK_TAM"** (≥%90 atın AGF'si dolu ilk görüntü) ya da sabit bir sabah saati (örn. 10:00) kaydet; `kazanan_profil.py`'deki `agf_sabah`, `agf_fark`, `agf_artis_sira`, 💰/🤫 işaretlerini ona bağla. 23.11 ve sonrası kayıtlar bu açıdan güvenilmez (22.11 ve öncesi 09:15'te alındığı için dolu).
- Geçici: `surpriz_ayri.py` doluluk <%80 ise AS10 vermiyor ve uyarı yazıyor.
- Kalan iş (isteğe bağlı): 23–25.11 için eski görüntülerden **TAM'ı geriye dönük türet** (`agf_tam.py` ile) ve `kazanan_profil` sabah AGF/hareket alanlarını yeniden hesapla (ayrı dosya, mevcut CSV'ye elle yazma). 25.11 Elazığ/İstanbul AGF'li tahminleri kısmi AGF'li, `canli_takip` değerlendirmelerinde ayrı etiketle.
- Ölçüm (pandera, `scripts/saglik_ilk_yayin.py`): 22.11 geçti; 23.11 14/17, 24.11 11/16 koşu kısmi. Gün sonu raporuna bu kontrolü eklemek de mümkün.
- Not: bu, `agf_kayit.py` (canlı kayıt sistemi) değişikliği, kullanıcıdan onay al.

**15. Veri sağlık kontrolü** (kosai makalesindeki "veri toplama hatası" dersi)
- TJK CSV'de AGF sütunu 10. indekse bağlı, ganyan/AGF/HP sütunu kayarsa fark edilmiyor. Günlük kontrol: "AGF toplamı ~%100 mü", "ganyan = HP oranı %0'a yakın mı", "at sayısı makul mü"; sapma olursa `GUNLUK.md` başına uyarı.

**16. Ganyan 999.99 yer tutucusu**
- Analiz çıktısında bazı atlar için `ganyan 999.99` görülüyor (22.11 İzmir 1). Erken saatte havuz açılmamış olabilir; olasılık/değer hesabına girmediğini ve `kazanan_profil` kaydına yanlış sızmadığını doğrula.

**17. Dondurma zamanı < koşu saati doğrulaması** (ileri test koruması fikri)
- `canli_takip.py` yalnızca koşudan ÖNCE dondurulmuş tahminleri saysın: dosya zamanı ile koşu saatini karşılaştıran açık bir kontrol ekle ve rapora "geçerli koşu sayısı" yaz.

**24. Kod kalitesi: ruff + pytest** (25.11'de kuruldu, `BILGI.md` "Araçlar")
- **✅ 25.11: 34 çıplak `except:` → `except Exception:`** (E722 0). Kalan: 36 kör `except Exception`, 37 `subprocess.run` `check`siz.
- Önce **çıplak/kör `except` (70 yer) ve `subprocess.run` `check`siz (37)**: hataları sessizce yutuyor olabilirler (kosai makalesindeki "sessiz veri hatası" dersi). Dosyalara dokunmadan önce kullanıcıdan onay al, canlı kayıt betiklerinde (`agf_kayit.py`, `agf_plan.py`) davranış değiştirme.
- pytest: önce TJK CSV ve eBayi JSON **ayrıştırıcıları** için örnek dosyalarla testler (format değişirse hemen fark edilir).

## D. Düşük öncelik / isteğe bağlı

**18. "Piyasa net/kararsız" etiketini günlük rapora ekle** (bilgi amaçlı; strateji değil, getiri her aralıkta negatif).

**19. scikit-learn / XGBoost sıralama modeli** (`rank:pairwise`, koşullu logit karşılaştırması `statsmodels`): v9'a alternatif. Beklenti düşük (model ≈ piyasa), yalnızca yeni özellikler (madde 5, 11) eklenince anlamlı.

**20. `alibaba/open-code-review`**: gerekirse "delegation" modunda `agf_plan.py` gibi yoğun dosyalara kod incelemesi. Claude kotası yer; şimdilik gerek yok.

**21. Açık repoların fikir taraması (kullanıcı isterse):** `nino0435/ganyan-model` aylık yürüyen backtest yapısı (ay ay A/E tablosu, bootstrap), `shap/shap`, `scikit-learn`, `evidentlyai/evidently` (veri kayması izleme; madde 15 yeterliyse gerekmez).

---

## Tamamlananlar (referans)
- Piyasa kalibrasyonu (170 bin at), net piyasa, sürpriz nerede (segment A/E), AGF'ye göre sürpriz tanımı, yüzeyde ilk kez, mesafe değişimi/uyumu, ilk kez hipodrom/mesafe: sonuçlar `BILGI.md`.
- TJK CSV önbellek düzeltmesi ve güven aralığı betiği eklendi (22.11).
