# Türkiye At Yarışı – Çalışma Notları (18.11.2026)

## Veri kaynağı (canlı, erişilebilir)
- Günlük program: https://www.tjk.org/TR/YarisSever/Info/Page/GunlukYarisProgrami
- CSV: https://medya-cdn.tjk.org/raporftp/TJKPDF/YYYY/YYYY-AA-GG/CSV/GunlukYarisProgrami/GG.AA.YYYY-<Şehir>-GunlukYarisProgrami-TR.csv
- Sonuçlar: https://www.tjk.org/TR/YarisSever/Info/Page/GunlukYarisSonuclari
- Analiz: `python3 analiz.py <csv>`

## Program sütunları
- HP: handikap puanı (yüksek = güçlü). Handikap koşularında kilo HP'ye göre verilir.
- Son 6 Y.: pist harfi + derece. K=Kum, Ç=Çim, S=Sentetik; 0 = ilk 9 dışı; "-" = sezon arası.
- KGS: son koşudan beri geçen gün. 7–30 ideal; 60+ ise uzun ara (form sorusu).
- s20: son 20 koşu performans puanı (20 en iyi).
- AGF: altılı ganyan favorisi yüzdesi = halkın tercihi (piyasa).
- St: start kulvarı. AP: apranti jokey (kilo indirimi). "+x Fazla Kilo".
- Ekipman: KG kapalı gözlük, DB dil bağı, K kulaklık, SK/SKG ringden starta.

## Koşu türleri
Maiden (hiç kazanmamış) → Şartlı 1-5 → Handikap (H1/H2, kilo HP'ye göre) → KV (Kısa Vade) → Listed/G3/G2/G1.
Irklar: İngiliz (daha hızlı) ve Arap ayrı koşar. "DHÖW" gibi şart kodlarının anlamı henüz doğrulanmadı.

## Bahis türleri (TJK)
Ganyan (1.), Plase, İkili, Sıralı İkili, Çifte (art arda 2 koşu birincisi), 3'lü/4'lü/5'li/6'lı Ganyan,
Sabit ihtimalli: Sabit Ganyan, Sabit İkili, Sabit İlk 2/3/4, Kim Geçer.

## Analiz çerçevem
1. Pist uyumu (bugünkü zemin = atın başarılı olduğu zemin mi?)
2. Mesafe uyumu (En İyi Derece hangi mesafede / benzer mesafede derece)
3. Sınıf: HP ve koşu türü (sınıf düşen atlar avantajlı)
4. Form: son 3 koşu, KGS
5. Kilo: Handikapta kilo/HP dengesi, apranti indirimi
6. Jokey/antrenör formu
7. Start (kısa mesafede iç kulvar avantajı)
8. Değer: tahminim AGF'den belirgin farklıysa değer var.

## Takvim notları (2026)
- 100. Gazi Koşusu (28.06.2026, Veliefendi): BAY NALÇAKAN – Halis Karataş (7. Gazi zaferi).
- Kasım 2026 aktif: İstanbul (kış sezonu 1. Y.G. 18.11), Elazığ, Adana (Yeşiloba), İzmir (Şirinyer).

## Kan (pedigri) analizi – eklendi 18.11.2026
- Kaynak: 180 günlük TJK sonuç CSV'leri (3.233 koşu, 559 aygır). TJK'nın aygır istatistik sorgu sayfası otomatik isteklere 403 veriyor; o yüzden istatistik kendi hesabımız.
- A/E = yavruların gerçek birinciliği / alan büyüklüğüne göre beklenen birincilik. 1,00 ortalama; 1,30+ çok iyi.
- Kırılımlar: ırk (Arap/İngiliz ayrı), zemin (Kum/Çim/Sentetik), mesafe bandı (≤1400 kısa, 1500–1900 orta, ≥2000 uzun).
- Az örnekli aygırlar ortalamaya çekilir (+4 sanal beklenen koşu).
- Not: A ≥1,30, B ≥1,05, C ≥0,85, D altı. Kısrak babası da aynı tablodan (kendi yavrularının başarısı) notlanır.

## Galop (idman) analizi
- Kaynak: programdaki "İdman Bilgileri" sekmesi (son idman: tarih, zemin, tür, 200–2200 m süreleri, idman jokeyi).
- Galop puanı = %60 hız (400 m süresi, koşudaki en hızlıya göre; 4 sn geride = 0) + %40 tazelik (≤7 gün tam, ≤14 gün %60, ≤30 gün %30).
- Kenter (süresiz) idman hız puanında düşük sayılır. Zeminler arası (kum/sentetik) süre farkı henüz düzeltilmiyor.
- Geçmiş idman verisi indirilmediği için galop bileşeni henüz geri teste girmedi.

## Model ve geri test (son 30 gün, 544 koşu, sızıntısız)
| Model | 1. seçim kazandı | Kazanan ilk 3'te | Ganyan getirisi |
|---|---|---|---|
| v1 (HP/s20/form) | %22,4 | %50,6 | %67 |
| v2 (+pist uyumu +baba kanı) | %22,8 | %54,6 | %65 |
| AGF favorisi (halk) | %30,5 | %64,0 | %66 |
| v3 (v2 + AGF yarı yarıya) | %31,2 | %64,3 | %68 |
- Ders: halkın tercihi (AGF) güçlü bir bilgi; model tek başına onu yenemiyor. Birlikte kullanılınca az farkla geçiyor.
- Ganyan getirisi her modelde ~%65–68: TJK kesintisi yüzünden sadece en iyi atı oynamak uzun vadede zarar. Kârlılık için model olasılığı ile oran arasında belirgin fark (değer) aranmalı.
- 18.11.2026 İstanbul (galoplu tam model v2+galop): 9 koşuda 4 kez ilk seçim kazandı, 5 koşuda kazanan ilk 3'te. Örnek çok küçük.

## Irk × zemin × mesafe profilleri (180 gün, 3.233 koşu) – eklendi 18.11.2026
Tam tablo: `veri/irk_zemin_mesafe_profil.txt`. "Piyasa A/E": ganyan oranının beklediğine göre; 1,00'den büyükse halk bu etkiyi hafife alıyor.

| Bulgu | Ayrıntı |
|---|---|
| İngilizler daha öngörülebilir | Favori İngilizlerde %31–44, Araplarda %27–36 kazanıyor. Arap alanları daha kalabalık (ort. 11–12 at; İngilizlerde 9–10). |
| Kısa mesafede iç kulvar | Arap kum kısa: 1–3 start piyasaya göre 1,14; Arap çim orta 1,21; Arap çim uzun 1,28; İngiliz kum kısa 1,09. Halk iç kulvarı biraz hafife alıyor. |
| Dış kulvar | İngiliz sentetik uzun ve Arap çim uzun gruplarında 10+ start çok zayıf (≈0,5). İngiliz çim uzun ve sentetik kısa gruplarında ise 10+ start iyi (1,2). Örnekler küçük. |
| HP lideri | Kısa mesafede HP en yüksek at %26–33, orta/uzun çimde sadece %16–17 kazanıyor: mesafe uzadıkça HP daha az belirleyici. |
| Apranti / en ağır kilo | Ham etki güçlü görünüyor (apranti 0,3–0,8; en ağır kilo 1,1–1,6), ama piyasaya göre ~1,0: büyük kısmı atın kalitesinden. Halk bunu zaten fiyatlıyor. |
| Yaş | İngiliz kum kısada 7+ yaş piyasaya göre 0,58: yaşlı sprinterler fazla oynanıyor. |

## v4 modeli: koşullu logit (koşu içi softmax)
- Özellikler: HP, s20, form, pist formu, baba kanı (zemin+mesafe A/E), kulvar etkisi (hipodrom+zemin+mesafe), AGF, uzun ara (>60 gün), apranti, yaş, kilo. Koşu içinde standartlaştırılır.
- Eğitim: 2.140 koşu (19.10.2026 öncesi), test: 542 görülmemiş koşu (son 30 gün). Aygır ve kulvar istatistiği eğitimde at kendi koşusunu dışarıda bırakarak hesaplanır.
- Gruba özel ağırlık, genel ağırlığa çekilerek (L2) öğrenilir.

| Test (542 koşu) | log-olabilirlik | 1. seçim | ilk 3 | 1. seçim getirisi |
|---|---|---|---|---|
| Sadece AGF | -1,868 | %30,6 | %64,4 | %66 |
| Genel model | -1,867 | %31,2 | %65,5 | %73 |
| Grup özel, zayıf çekim (λ=30) | -1,897 | %31,5 | %64,8 | %78 |
| Grup özel, güçlü çekim (λ=1000, kullanılan) | -1,870 | %31,2 | %66,8 | %73 |

- Dürüst sonuç: Gruplar arası farklar gerçek, ama büyük kısmını halk (AGF) zaten fiyatlıyor. Gruba özel serbest ağırlıklar ezber yapıyor (λ=30 testte daha kötü). Model AGF'yi ancak hafifçe geçiyor.
- 1. seçimi oynamanın getirisi %66'dan %73'e çıkıyor ama hâlâ başabaşın (%100) altında.
- Güvenilir kalan küçük avantaj: kısa mesafede iç kulvar.
- Galop, modelde küçük bir ek düzeltme olarak var (geri test edilmedi).
- Günlük kullanım: `scripts/analiz3.py` her ata olasılık, adil oran ve AGF karşılaştırması verir; olasılık AGF'nin 1,3 katı ve %8'den büyükse "★DEĞER" işaretler.

## Koşu kuralları (kaynak: TJK 2026 At Yarışları Genel Hükümleri)
- **Maiden:** hiç birincilik kazanmamış atlar. **Şartlı 19:** koşu kazanmamışlar (maiden gibi, bölünmez). **Şartlı 27:** hiç start almamışlar.
- **Şartlı 1–5:** kazanç tavanına göre artan sınıflar (a: 2 yaşlı İngiliz / 3 yaşlı Arap; b: büyükler).
- **KV-6…KV-9:** kısa vadeli, daha üst sınıf (KV-6-b2 ≥51 puan, KV-7-b2 ≥56 puan).
- **Handikap 13…24:** puanlı; her puan ½ kg; en yüksek puanlı at azami sıkleti taşır, diğerleri puan başına ½ kg az. Handikap 22/24 ve G3-Handikap'ta azami sıklet 61 kg.
- **G1/G2/G3:** grup (açık) koşular; kazananlar alt sınıflara belirli süre giremez.
- **DHÖW:** Devlet Harası veya Özel yetiştirme veya WAHO'ya kayıtlı Arap atlarına açık koşu. **ULS-W:** uluslararası WAHO. **TR:** Türkiye doğumlu. **E/D:** sadece erkek/dişi. **Y0–Y3:** apranti koşuları.
- **Apranti (jokey yamağı) indirimi:** Maiden, Şartlı 19/2/3/4/5 ve Handikap 13/14/15/16/17/21'de geçerli; açık, KV ve satışta yok. Y-koşularında sınıfa göre 1–4 kg.

## Koşu türü analizi (180 gün; tam tablo `veri/kosu_turu_jokey.txt`)
Not: eşit kilo/HP'li atlar eşit sıra alır (önceki sürümde sonuç dosyasındaki bitiş sırası eşitlikleri bozuyordu; düzeltildi).

| Bulgu | Ayrıntı |
|---|---|
| En öngörülebilir | İngiliz KV-8 (favori %51), KV-9 %48, Handikap 24 %47, G1 %50, Şartlı 5 %42 |
| En sürprizli | İngiliz Handikap 15 (favori %22), Arap Handikap 17 %16, Arap Handikap 21 %6, Arap G3 %12,5 |
| Handikapta HP lideri zayıf | Handikap 14–17'de HP en yüksek at sadece %8–13 kazanıyor (kilo dengeliyor). Şartlı/KV'de %18–36. |
| Tipik HP aralıkları | Maiden 10–34, Handikap 14: 29–47, H15: 32–56, H16: 38–69, H17: 55–82, KV-6: 41–95, G3: 54–106 |
| Karma koşuda dişiler | Çoğu türde piyasaya göre 0,6–0,9 (Arap Handikap 14–15'te 0,6); İngiliz KV-6/7'de 1,2 |
| En ağır kilo | Eşitlik düzeltmesinden sonra piyasaya göre ~1,0: halk doğru fiyatlıyor |

## Jokey analizi
- 150+ binişli jokeyler `veri/kosu_turu_jokey.txt`. Beceri farkı büyük: N.AVCİ, G.KOCAKAYA, V.ABİŞ, M.M.BİLGİN alan büyüklüğüne göre ~2 kat kazanıyor.
- Ama piyasa bunu biliyor: ilk 90 günde piyasaya göre iyi olan 16 jokey sonraki 90 günde 1,04, kötü olan 14 jokey 0,96. Korelasyon -0,02 (`veri/jokey_kalicilik.txt`). Jokeyde kalıcı "halkın kaçırdığı" avantaj çok küçük.

## v5 modeli
- Eklenenler: jokey özelliği; koşu türü ailesine göre grup (Maiden/Şartlı/Handikap/KV/Grup/Satış × ırk).
- Önemli düzeltme: aygır/kulvar/jokey tabloları artık **kronolojik** (her gün yalnızca önceki günlerden). Önceki "kendi koşusunu dışarıda bırakma" yöntemi küçük bir negatif kayma yaratıyordu.

| Test (542 görülmemiş koşu) | log-olabilirlik | 1. seçim | ilk 3 | 1. seçim getirisi | değer bahsi getirisi |
|---|---|---|---|---|---|
| Sadece AGF | -1,868 | %30,6 | %64,4 | %66 | %92 |
| v5 genel | -1,859 | %31,5 | %65,5 | %74 | %98 |
| v5 ırk×zemin×mesafe grubu | -1,896 | %31,5 | %66,2 | %76 | %95 |
| **v5 ırk×koşu türü grubu (kullanılan)** | **-1,856** | %31,4 | %66,2 | %74 | **%100** |

- Ağırlıklar (genel): AGF 0,99; yaş -0,15 (yaşlı atlar fazla oynanıyor); form -0,08 (halk son forma fazla güveniyor); kilo -0,08; uzun ara -0,07; kulvar +0,06; jokey ≈0 (piyasa fiyatlıyor).
- Değer bahsi (olasılık > piyasa×1,3, oran ≤30) başabaşa geldi: 830 bahiste %100. Örnek hâlâ küçük; ±%15 belirsizlik var.

## AGF'siz model (bahis açılmadan önce) – eklendi 18.11.2026
- Yarının programında AGF boş olur. AGF'ye dayanan v5 o zaman anlamsızlaşır; `analiz3.py` AGF yoksa otomatik olarak `veri/model_agfsiz.json` kullanır ve değer işareti koymaz.
- Test (542 görülmemiş koşu): 1. seçim %27,5, ilk 3 %59,8 (AGF favorisi %30,6 / %64,4). Değer bahsi getirisi %81: sadece sıralama için, değer için değil.
- Ağırlıklar (AGF yokken): HP 0,32, pist formu 0,31, jokey 0,18, s20 0,14, form 0,12; uzun ara -0,23, yaş -0,19, apranti -0,18.
- Standartlaştırılmış özellikler ±2,5 ile sınırlandı (test sonucunu değiştirmedi). Uyarı: 5–6 atlık küçük alanlarda olasılıklar fazla iddialı çıkabiliyor.
- Antalya sezonu yeni başladığı için Antalya kulvar istatistiği henüz yok (nötr kabul ediliyor).

## Hava durumu – eklendi 18.11.2026
- Geçmiş hava: Open-Meteo arşivi, 10 hipodrom × 202 gün (`veri/hava_gecmis.json`). Islaklık = günün yağışı + önceki günün yarısı. Kuru <1 mm, hafif 1–5, ıslak ≥5.
- Koşu günü tahmini: Open-Meteo, günlük sınır dolarsa wttr.in (`scripts/hava.py tahmin`). Koşu günü TJK'nın pist durumu (ör. "Kum: Normal") ve hava satırı okunur; TJK pisti ağır/ıslak/yumuşak/sulu/çamurlu derse ıslak sayılır.
- Tam tablo: `veri/hava_etkisi.txt`.

| Bulgu | Ayrıntı |
|---|---|
| Islak kumda favori daha güvenilir | Favori kazanma: ıslak %40, kuru %32 (tüm ırklar). İngiliz ıslak kum %43, Arap %36. HP lideri ıslakta %26, kuruda %20. |
| Çim ve sentetikte de | Islak çimde favori %42 (kuru %36), ıslak sentetikte %39 (kuru %34). |
| Kulvar | Islak sentetikte iç kulvar avantajı kayboluyor (Arap 0,88). Islak çimde dış kulvar iyi görünüyor (İngiliz 2,09) ama sadece 21 koşu. |
| Sıcaklık | Belirgin etki yok (favori %33–35). |
| Aygırın ıslak pist farkı | Tabloda büyük farklar var (EPAULETTE, LION HEART ıslakta iyi; SEMEND, KARAÜZÜM, AUTHORIZED kötü) ama modelde yeni günlerde işe yaramadı (ağırlık -0,03): büyük kısmı şans. |

## v6 modeli (v5 + hava)
- Yeni özellikler: ıslak günde HP ve AGF etkileşimi, babanın ıslak/kuru farkı (kronolojik).
- Test (542 koşu, 20'si ıslak gün): log-olabilirlik -1,855 (v5 -1,856, AGF -1,868); değer bahsi 826 bahiste %101.
- Ağırlıklar: ıslak günde AGF +0,08 (yağışta favoriye daha çok güven), ıslak HP -0,04, baba ıslak -0,03.
- AGF'siz v6: 1. seçim %27,5, ilk 3 %60,0.
- Sonuç: Hava, favorinin ne kadar güvenilir olduğunu değiştiriyor; ama bunu modele katınca kazanç küçük. Asıl kullanımı: ıslak günde favoriye/HP liderine daha çok güven, sürpriz arayışını azalt.

## Galop: pegadrom.com – eklendi 18.11.2026
- TJK'nın idman sayfası otomatik isteklere 403 verdiği için galop artık pegadrom.com'dan alınıyor (kaynak TJK idman kayıtları; robots.txt izin veriyor; istekler arası 2 sn). `scripts/galop_pegadrom.py`.
- Her at için geçmiş idmanlar: tarih, pist, zemin, tür, **efor** (Rahat / Hafif Çalışarak / Çalışarak), süre, ara dereceler, idman jokeyi, site puanı.
- İlk geri test (10 gün, 146 koşu, `scripts/galop_test.py`), piyasaya göre A/E:

| Özellik | A/E |
|---|---|
| Son 30 günde 3+ idman | 1,46 (42 kazanma / 28,8 beklenen) |
| 400 m'de koşunun en hızlısı | 1,19 |
| Son idman 4–7 gün önce | 1,27; 8–14 gün önce 0,62 |
| Son efor "Çalışarak" (zorlanarak) | 0,29 (2 / 6,9) |

- Ama günü dışarıda bırakan testte piyasa + galop, sadece piyasadan iyi değil (-1,8690 / -1,8681). 146 koşu az: sinyaller umut verici, kanıtlanmadı. 46 yarış günü daha indiriliyor.
- `analiz3.py`: galop satırında 30 gündeki idman sayısı, en iyi 400 m, son efor; "↑çok idman" ve "⚠zorlanarak" işaretleri. Olasılığa etkisi küçük tutuldu.

### Galop: büyük örnekle sonuç (67 yarış günü indirildi; 30 gün / 420 koşu testte)
| Özellik | Piyasa A/E |
|---|---|
| Son 30 günde hiç idman yok | 0,72 |
| Son 30 günde 3+ idman | 1,15 |
| Son idman 4–7 gün önce | 1,12 (8–14 gün 0,79; 15+ gün 0,79) |
| Son efor "Çalışarak" | 0,66 |
| 400 m'de en hızlı | 1,10 |

- Günü dışarıda bırakan test: sadece piyasa -1,9260 → piyasa + galop **-1,9183** (koşu başına +0,0077; v5'in AGF'ye katkısından bile büyük).
- Öğrenilen ağırlıklar (`veri/galop_agirlik.json`): son 7 günde idman +0,34, 30 gündeki idman sayısı +0,23, zorlanarak -0,33, galop yok -0,14, 400 m hızı ~0.
- Yorum: Galop süresi değil, **düzenli ve yakın zamanda rahat çalışmış olmak** önemli. Halk bunu tam fiyatlamıyor. Zorlanarak çalışan at genelde hazır değil.
- `analiz3.py` bu ağırlıkları kullanıyor (önceki el yapımı galop puanının yerine).

## Literatür etkenlerinin testi – eklendi 18.11.2026
Kaynaklar: Benter'in iki aşamalı modeli (temel model + halk oranları, koşullu logit; Bolton & Chapman 1986), Beyer tipi hız puanları (par süre + günlük pist değişkeni), handikap yazılarındaki "sınıf düşüşü, ilk kez kapalı gözlük, antrenör formu, kilo değişimi" iddiaları.
Yöntem (`scripts/ozellik_test.py`): her atın geçmişi yalnızca önceki koşulardan; ganyan oranı sabit (ağırlık 1), özellik ağırlığı gün bazlı 10 katlı çapraz doğrulamayla öğrenildi; 1.837 görülmemiş koşu. Katkı = koşu başına log-olabilirlik farkı × 1000.

| Etken | Katkı (binde) | Karar |
|---|---|---|
| **Hız puanı: son 3 koşunun en iyisi** | **+4,87** | Eklendi (ağırlık 0,125) |
| Hız puanı: son koşu | +1,98 | En iyi-3 ile örtüşüyor |
| Son koşuda birinciye saniye farkı | +0,89 | Çok küçük |
| Hız puanı hiç yok | +0,34 | Çok küçük |
| Antrenör formu (60 gün) | +0,21 | Etkisiz |
| İlk kez kapalı gözlük | +0,01 | Etkisiz |
| Kilo değişimi | -0,13 | Etkisiz |
| Son koşu derecesi | -0,17 | Etkisiz |
| Mesafe değişimi | -0,25 | Etkisiz |
| Sınıf değişimi (ödüle göre) | -0,30 | Etkisiz |
| Jokey yükselmesi | -0,33 | Etkisiz |

- Halk sınıf, kilo, jokey ve ekipman değişikliğini zaten fiyatlıyor; bizim verimizde bunların ek bilgisi yok. Hız puanı ise halkın tam kullanmadığı bilgi.
- Hız puanı: `-1000 × ((süre - par)/par - günlük değişken)`. Par = aynı hipodrom+pist+mesafe+ırkta önceki günlerin kazanan süre medyanı (≥4 örnek). Değişken = o gün o pistte kazananların par'dan sapma medyanı. 0 = ortalama kazanan; +10 ≈ %1 daha hızlı.
- Kalıcılık: 180 günlük sonuç CSV'leri `veri/sonuc/` içinde. `gunluk.py` her çalıştığında son 10 günün eksik sonuçlarını indirip `veri/hiz_puani.json`'ı yeniden üretir.

## Eküri – eklendi 19.11.2026
- Aynı sahip/antrenörün atları tek bahis birimidir: ganyan oranları aynıdır, biri kazanırsa ganyan kazanır (sonuç dosyasında örnek: ALPLİ ve YAZ MELTEMİ ikisi de 3,15).
- Eküri bilgisi program HTML'indeki `tablo-ekuri` satırından ve CSV'deki "[(..)AD,(..)AD,] eküridir" satırından okunur.
- **Düzeltilen hata:** önceki testlerde ganyandan piyasa olasılığı hesaplanırken eküri iki kez sayılıyordu. Düzeltmeyle sadece-piyasa log-olabilirliği -1,8806'dan -1,8762'ye iyileşti (piyasa olasılıkları daha doğru).
- `analiz3.py` eküri atlarını [EKÜRİ] diye işaretler ve birlikte olasılığını/adil oranını yazar.

## Sürpriz analizi (2.464 koşu, eküri tek birim; `veri/surpriz.txt`)
| Durum | Favori kazanır | Ganyan ≥10 kazanır |
|---|---|---|
| Tümü | %34,1 | %17,8 |
| ≤7 bahis birimi | %44,9 | %8,8 |
| 14+ bahis birimi | %27,9 | %29,1 |
| Arap Handikap | %25,9 | %27,2 |
| İngiliz KV | %43,0 | %8,1 |
| İngiliz Şartlı | %42,1 | %11,4 |

Favori–sürpriz yanlılığı (oran kovasına göre piyasa A/E ve 1 TL getirisi): ganyan 1–5 ≈1,00 (%68–70); **5–20: 1,05–1,06 (%75)**; 20–50: 0,83 (%57); 50+: 0,42 (%26). Çok uç oranlı atlar sistematik olarak fazla oynanıyor. Hiçbir kova tek başına ~%30 kesintiyi aşmıyor.
`analiz3.py` her koşuya geçmişe dayalı sürpriz riskini yazar (bahis birimi sayısı ve ırk × koşu türüne göre).

## Jokey tablosu (`veri/jokey_tablo.json`, `scripts/jokey_tablo.py`)
- Her jokey için gerçek sayılar: 180 gün biniş/galibiyet/yüzde, son 30 gün, hipodrom bazında, favoriyle kazanma, piyasa A/E (eküri düzeltmeli).
- Örnek: N.AVCİ %20,8 (600 biniş), İzmir 49/182, favoride 33/89, piyasa A/E 1,14. A.SÖZEN %8,0, piyasa A/E 0,66.
- Not: önceki tabloda piyasa A/E'de pay/payda uyumsuzluğu vardı (oranı eksik koşulardaki galibiyetler paya giriyordu); düzeltildi.

## Kupon ve ikili olasılıkları (`scripts/kupon.py`)
- Çoklu ganyan (5'li/6'lı/7'li): her adımda (isabet olasılığı artışı / maliyet artışı) en iyi olan at eklenir; bütçe sınırı. Çıktı: her ayak, ayak kapsaması, kombinasyon sayısı, maliyet, modele göre isabet olasılığı.
- İkili / sıralı ikili: Harville formülü P(i 1., j 2.) = p_i·p_j/(1−p_i). Literatürde Harville'in sürpriz atların 2.liğini biraz abarttığı bilinir.
- `gunluk.py` her analiz dosyasının sonuna kuponu ekler (varsayılan 1 TL birim, 300 TL bütçe).

## AGF hareketi
- Geç gelen para (1. ve 2. AGF arası değişim) için geçmiş veri yok. `gunluk.py` her çalıştığında program CSV'sinin saat damgalı kopyasını `veri/agf_kayit/` altına saklar; birkaç gün biriktikten sonra test edilecek.

## 2. tur etken testi (1.850 görülmemiş koşu, eküri düzeltmeli; `scripts/ozellik_test2.py`, `veri/ozellik_test2.json`)
| Etken | Katkı (binde) | Karar |
|---|---|---|
| Hız puanı, son 3'ün en iyisi | +4,54 | ✅ (ağırlık 0,10) |
| Bu pistte daha önce kazanmış | +2,16 | ✅ (0,062) |
| Hız puanı, son koşu | +1,74 | ✅ (0,04) |
| Deneyim (koşu sayısı, log) | +1,64 | ✅ (0,053) |
| Aynı hipodrom+pist+mesafede (±100 m) kazanmış | +1,48 | ✅ (0,13) |
| At sahibi (A/E) | +0,81 | ✅ (0,034) |
| Son koşuda saniye farkı | +0,57 | ❌ birlikte ters işaret aldı (hız puanıyla aynı bilgi) |
| Uzun dinlenme (>60 gün) | +0,34 | çok küçük |
| Jokey hipodrom uzmanlığı | +0,04 | ❌ |
| Jokey son 30 gün formu | -0,74 | ❌ |
| Antrenör + jokey ikilisi | -1,07 | ❌ |
| HP değişimi | -0,58 | ❌ |
| Sınıf / kilo / mesafe değişimi, ilk kez KG, son derece | -0,35…+0,13 | ❌ |

- Seçilenler birlikte: **+5,80 binde** (tek başına hız puanı +4,54).
- Jokey: beceri gerçek ama halk tam fiyatlıyor; son form ve hipodrom uzmanlığı ek bilgi taşımıyor. Analizde gerçek sayılarla gösteriliyor, olasılığa ek etkisi yok.
- `veri/hiz_puani.json` artık her at için koşu sayısı, galibiyetleri (hipodrom/pist/mesafe) ve son 3 hız puanını; her sahip için A/E'yi tutar.

## Koşu türüne göre etken ağırlıkları farklı mı? (`scripts/kosu_turu_etkilesim.py`, `veri/kosu_turu_etkilesim.txt`)
- 1.850 görülmemiş koşu, 10 katlı gün bazlı çapraz doğrulama.
- Tek ağırlık: +5,97 binde; ırk × koşu türü ailesine göre ayrı ağırlık (genele çekilerek): +5,61 binde → **ayrı ağırlık daha iyi değil**.
- Tabloda görülen farklar (ör. Arap Maiden'da deneyim 0,27, Handikapta pist-mesafe galibi 0,16–0,20, İngiliz Şartlı'da hız puanı 0,24) yeni günlerde tutmadı; grup başına 40–300 koşu yetersiz. Veri biriktikçe tekrar test edilecek.
- Koşu farklılığı analizde profil olarak gösterilir (favori/HP lideri oranı, sürpriz riski, kulvar, hava); etken ağırlıkları tek tutulur.

## Eksik denetimi ve kapsamlı test – 19.11.2026
**Web:** Türkiye için açık ara derece (tempo/son 800) kaynağı bulunamadı. Literatür: kazançta strateji model kadar önemli; tahmin hatası nedeniyle kesirli (1/4) Kelly önerilir (Metel 2017; Hubáček vd. 2021); kalibrasyon ayrıca test edilmeli.

**Kapsamlı test** (`scripts/tam_test.py`, `veri/tam_test.txt`; galoplu 420 koşu, 10 katlı gün CV, eküri tek birim):
| Model | log-olabilirlik | piyasaya katkı |
|---|---|---|
| Piyasa (ganyan) | -1,9089 | – |
| + geçmiş etkenleri | -1,8977 | +11,2 binde |
| + galop | -1,8957 | +13,2 binde |

Kalibrasyon: %0–20 tahminlerde iyi (gerçek biraz yüksek); **%20–30 ve %35–40 aralığında model fazla iyimser** (22–27 tahmin → 18–22 gerçek).

Değer bahsi (koşu sonrası kesin ganyanla; gerçekte bahis anında bilinmez):
| Eşik | Bahis | Sabit 1 TL | 1/4 Kelly |
|---|---|---|---|
| 1,1× piyasa | 850 | %90,7 | %129,0 |
| 1,2× | 529 | %90,5 | %130,7 |
| 1,3× | 294 | %95,6 | %133,2 |
| 1,5× | 70 | %174,9 | %138,2 |
- Sabit bahis 1,3× eşikte bile zarar. 1,5× eşik umut verici ama 70 bahis / 18 kazanan: rastlantı olabilir. Kârlılık iddia edilmez; canlı takip gerekir.
- Değişiklik: ★DEĞER eşiği 1,3×'ten **1,5×**'e (p ≥ %5). Her ata "değer için ganyan ≥ 1,5/p" eşiği yazılır; bahis anındaki gerçek ganyanla karşılaştırılmalı.

**Harville testi** (`scripts/harville_test.py`, `veri/harville_test.txt`; 2.446 koşu): ilk ikiye girme tahmini %0–70'te gerçekle 1–3 puan içinde; çok güçlü favorilerde abartılı (%84 tahmin → %76 gerçek). Sıralı ikilide en olası kombinasyonlar biraz hafife alınıyor (%17–32 tahmin → %20–36 gerçek).

**Veri genişletme:** sonuçlar ~560 güne genişletiliyor (Antalya kış sezonu ve atların daha uzun geçmişi için). Bittiğinde hız tablosu, aygır/kulvar/jokey tabloları ve testler yeniden üretilecek.

### Veri genişletme tamamlandı (19.11.2026)
- Sonuçlar 2025-05-07 → 2026-11-18: 1.184 yarış günü, 7.921 koşu (önce 391 gün). Antalya 57 gün (geçen kış dahil).
- Yeniden üretildi: hız puanı (9.593 at), jokey tablosu (238), koşu türleri (31 tür, 17 kod), sürpriz, koşu türü/jokey, ırk×zemin×mesafe profilleri, model aygır/kulvar/jokey tabloları.
- AGF'li model testte değişmedi (-1,855); AGF'siz model iyileşti (-2,011 → -2,006; ilk 3 %60,0 → %60,9).
- Uzun veriyle sürpriz: favori %35,3, ganyan ≥10 kazanan %15,8 (7.921 koşu).

## v8: bütün etkenler AGF ile birlikte eğitildi – 19.11.2026
- `scripts/gecmis_ozellik.py`: her at-koşu için yalnızca önceki günlerden hız puanı (en iyi-3, son), pist-mesafe galibi, pist galibi, deneyim, sahip, galop (100.521 kayıt).
- `scripts/model8.py` = v6 + bu özellikler (aynı kronolojik eğitim; test 19.10–18.11, 542 koşu).

| Test | log-olabilirlik | 1. seçim | ilk 3 |
|---|---|---|---|
| Sadece AGF | -1,868 | %30,6 | %64,4 |
| v6 | -1,855 | %31,5 | %65,5 |
| **v8** | **-1,849** | **%32,1** | **%67,0** |
| AGF'siz v6 | -2,006 | %27,3 | %60,9 |
| **AGF'siz v8** | **-1,963** | **%29,3** | %60,3 |

- v8 ağırlıkları (genel): AGF 0,92; hız en iyi-3 0,12; pist-mesafe galibi 0,12; kulvar 0,06; ıslak×AGF 0,08; yaş -0,15; form -0,10; uzun ara -0,09; kilo -0,08; deneyim -0,06 (AGF ile birlikte işaret değişti).
- Galop eğitim döneminde yok (galop verisi yalnızca son 30 gün) → v8'de galop ağırlığı 0; galop ayrı doğrulanmış ağırlıklarla (`veri/galop_agirlik.json`) eklenmeye devam ediyor. Galop geçmişi biriktikçe v8'e katılacak.
- v8 olasılıkları daha temkinli (ör. BEAUTY ALYA %43 → %33): kalibrasyon testindeki aşırı iyimserliği azaltıyor.
- Canlı test: 19.11 için hem sabahki v6 hem v8 tahminleri koşudan önce donduruldu (`veri/tahminler/*_v8.json`); `canli_takip.py` ikisini ayrı kaydeder (`veri/canli_takip.csv`, `veri/canli_takip_v8.csv`).
- 19.11 canlı teste üçüncü model eklendi: **AGF'siz** (sadece bizim verimiz, halkın tercihi yok). `AGFSIZ_ZORLA=1` ile üretildi, koşudan önce donduruldu (`veri/tahminler/*_agfsiz.json`), sonuçları `veri/canli_takip_agfsiz.csv`. Karşılaştırma: v6 (sabah), v8 (AGF'li), AGF'siz ve AGF favorisi.

## Galop kaynakları karşılaştırması – 19.11.2026
| Site | Durum | Karar |
|---|---|---|
| pegadrom.com | Sunucuda hazır HTML, robots.txt izin veriyor; geçmiş idmanlar, efor, ara dereceler, jokey | **Kullanılıyor** |
| TJK idman bilgileri / İdman İstatistikleri | Otomatik isteklere 403 / zaman aşımı | Engel aşılmadı |
| puanlibulten.com/galoplar | Tablo JavaScript ile robots.txt'nin yasakladığı /api/'den yükleniyor | Kurala uyuldu, kullanılmadı |
| sonduzluk.com | Galop sayfası 403 | Engel aşılmadı |
| hipodrom.com | JavaScript uygulaması, HTML'de veri yok | Kullanılamıyor |
| sihirlikantarma.org | Eski blog yazıları (2022–2025), güncel tablo yok | İşe yaramaz |
| horseturk.com | Tahmin sitesi, galop listesi yok | İşe yaramaz |
- pegadrom erişilemezse `gunluk.py` galopsuz çalışır, analizde "idman yok" yazar.

## Ganyan (muhtemel) – 19.11.2026
- TJK program HTML'inde her atın güncel muhtemel ganyanı var (`Gny` sütunu; CSV'de yok). `analiz3.py` her atın yanına yazar; ganyan ≥ 1,5/olasılık ise ★GANYAN (eküri birim olasılığıyla).
- **Piyasa oturma kontrolü:** eküri tek birim sayılarak Σ(1/ganyan) normalde ~1,25–1,45 (TJK kesintisi). 1,15–1,60 dışındaysa "piyasa oturmamış" yazılır ve işaret konmaz (sabah erken saatte 546, 999 gibi anlamsız oranlar görülüyor).
- `scripts/ganyan_kontrol.py GG.AA.YYYY Hipodrom [v8|agfsiz]`: koşudan hemen önce güncel ganyanı çekip dondurulmuş tahminlerle karşılaştırır. En anlamlı kullanım: koşuya ~5–10 dakika kala.

## Sürpriz atlarda değer var mı? (`scripts/surpriz_deger_test.py`, `veri/surpriz_deger_test.txt`)
7.228 koşu, 69.367 bahis birimi; piyasa (kesin ganyan, eküri tek birim) + geçmiş etkenleri, 10 katlı gün CV.
| Ganyan | Hepsi: 1 TL getirisi | Model > 1,2× piyasa |
|---|---|---|
| 1–5 | %72,1 | %83,7 (1.042 bahis) |
| 5–10 | %72,5 | %85,0 (757) |
| 10–20 | %68,5 | %65,2 (420) – seçim daha kötü |
| 20–50 | %53,8 | %143,0 (159 bahis, 9 kazanan; model 5,6 bekliyordu → büyük ölçüde şans) |
| 50+ | %38,9 | yetersiz örnek |
- Sonuç: model sürprizleri kârlı biçimde seçemiyor; ★SÜRPRİZ ADAYI işareti eklenmedi (veri desteklemiyor). Model kısa oranlarda (1–10) seçimi iyileştiriyor ama %100'ün altında.
- Galop ve AGF dahil test için galoplu veri biriktikçe tekrarlanacak.

## Irk karakteristiği (`scripts/irk_karakter.py`, `veri/irk_karakter.txt`; 9.946 koşu)
| | Arap | İngiliz |
|---|---|---|
| Kazanan hızı (m/sn) | 13,8–15,1 | 15,1–16,7 (**her zemin/mesafede %10–11 daha hızlı**) |
| Koşu başına at | 10,8 | 9,5 |
| 1. ile 2. arası (medyan) | 0,28 sn | 0,29 sn |
| İstikrar (ardışık koşu derece korelasyonu) | 0,27 | 0,26 |
| ≤1400 m payı | %55 | %51 |
| Karma koşuda erkek / dişi (alan A/E) | 1,12 / 0,58 | 1,11 / 0,66 |
- İstikrar ve kazanma farkı iki ırkta neredeyse aynı: Araplardaki fazla sürpriz kalabalık alanlardan.
- Yaş (karma yaşlı koşularda): Arap 4 ve 6 yaş biraz iyi, İngiliz 3 yaş biraz iyi; çoğu koşu tek yaşa açık olduğundan zayıf bulgu.

### Dişi atlar karma koşularda fazla oynanıyor (kalıcı piyasa yanılgısı)
| | 1. dönem (<11.02.2026) | 2. dönem |
|---|---|---|
| Arap dişi, piyasa A/E | 0,84 (206 / 245,9) | 0,78 (146 / 188,3) |
| İngiliz dişi, piyasa A/E | 0,84 (277 / 328,5) | 0,81 (243 / 300,6) |
| Erkek | 1,04–1,06 | 1,04–1,06 |

## v9 = v8 + "karma koşuda dişi" (`scripts/model9.py`)
| Test (542 koşu) | log-olabilirlik | 1. seçim | ilk 3 |
|---|---|---|---|
| AGF favorisi | -1,868 | %30,6 | %64,4 |
| v8 | -1,849 | %32,1 | %67,0 |
| **v9** | **-1,845** | **%33,0** | **%67,3** |
| AGF'siz v8 | -1,963 | %29,3 | %60,3 |
| **AGF'siz v9** | **-1,947** | **%31,2** | %61,1 |
- Ağırlık: AGF'li -0,15, AGF'siz -0,37. AGF'siz model (yalnızca bizim verimiz) artık AGF favorisinden sık kazananı buluyor.
- 19.11 canlı testi sabah dondurulan v6/v8/AGF'siz(v8) tahminleriyle devam ediyor; v9 bir sonraki yarış gününden itibaren kullanılacak.

## Cinsiyet kodları ayrı ayrı (`scripts/cinsiyet_analiz.py`, `veri/cinsiyet_analiz.txt`)
Kodların anlamı veriyle doğrulandı: **erkek/dişi** = genç (Arap 3 yaş, İngiliz 2–3 yaş); **aygır/kısrak** = 4 yaş ve üstü; **iğdiş** = kısırlaştırılmış erkek (her yaş).
Piyasa A/E (iki dönem; eküri tek birim):
| Cinsiyet | Arap | İngiliz | Yorum |
|---|---|---|---|
| Erkek (genç) | 1,05–1,08 | 1,06–1,09 | halk hafife alıyor (tutarlı) |
| Dişi (genç), karma koşu | 0,76–0,83 | 0,81–0,86 | halk fazla oynuyor (tutarlı) |
| Kısrak, karma koşu | 0,79–0,84 | 0,97 / 0,59 | Arapta tutarlı, İngilizde çelişkili |
| Aygır | 1,03–1,04 | 0,97–1,07 | doğru fiyatlanıyor |
| İğdiş | 0,75–0,98 | 0,78–0,91 | az örnek (8–38 kazanan/dönem) |
- Not: ilk çalıştırmada piyasa A/E'de pay/payda hatası vardı (oranı eksik koşulardaki galibiyetler paya giriyordu); düzeltildi.
- v10 (v9 + genç erkek + iğdiş): AGF'li -1,844 (v9 -1,845), AGF'siz -1,947 (aynı) → fark gürültü düzeyinde; genç erkek ile dişi karma koşuda aynı bilginin iki yüzü. **v9 kullanılmaya devam ediyor.**

## Soy, antrenör, sahip ve form ayrıntıları – 19.11.2026 (7.228 koşu, piyasa = ganyan, kronolojik, 10 katlı gün CV)
Raporlar: `veri/soy_rapor.txt`, `veri/antrenor_rapor_test.txt`, `veri/sahip_rapor_test.txt`; testler: `veri/soy_test.txt`, `veri/form_test.txt`.
| Etken | Katkı (binde) |
|---|---|
| Aygırın piyasa A/E'si ("X yavrusu" etkisi) | -0,09 |
| Kardeş başarısı (aynı anne) | +0,26 |
| Aygırın bu yaş grubundaki yavruları (erken/geç olgunlaşma) | +0,71 |
| Antrenör: piyasa A/E / ilk koşu / uzun ara / hipodrom | +0,22 / +0,05 / 0,00 / -0,06 |
| Sahip: alan A/E / piyasa A/E / hepsi birlikte | +0,83 / -0,03 / +2,11 |
| Form: son koşu / son 3 / son 6 / galibiyet sayısı / pist son 6 / gidişat | -0,12 / +0,71 / +1,09 / +1,16 / +1,16 / -0,05 |
- Kalıcılık: aygır piyasa A/E dönemler arası korelasyonu Arap 0,22, İngiliz 0,05; antrenör -0,02; sahip -0,23 → halk bunları fiyatlıyor.
- Tutarlı yanılgı görülen birkaç aygır: FATİH AĞA ve AYABAKAN hafife alınıyor (iki dönemde 1,12–1,23), TAMERİNOĞLU fazla oynanıyor (0,79/0,69).
- **v11** (v9 + baba_yas, anne_kardes, sahip_piyasa, galibiyet6): AGF'li -1,844 (v9 -1,845), AGF'siz -1,947 (aynı) → gürültü düzeyi; galibiyet6 ağırlığı eksi (form/hız ile örtüşme). **v9 kullanılmaya devam ediyor.**
- Anne babası: sonuç dosyalarında yok; `scripts/soy_kayit.py` her gün programdan baba/anne/anne babası biriktiriyor (`veri/soy_kayit.json`); yeterli veri olunca test edilecek.

## SİAYSD 2026 aygır kataloğu (`scripts/aygir_katalog.py`, `veri/aygir_katalog_2026.json`)
- Kaynak: https://www.siaysd.org.tr/2026-aygir-katalogu-sayfalari/ (robots.txt izin veriyor). 124 İngiliz aygırının PDF sayfası (adresler: `veri/aygir_katalog_2026_pdf_adresleri.txt`; PDF'ler 213 MB, repoya konmadı).
- Her aygır: don, doğum yılı, haraya giriş, kendi yarış kariyeri, babası, **yıllara göre tay sonuçları (koşan, kazanan, koşu, galibiyet; 12.12.2025'e kadar)**, anne hattı, en iyi tayları.
- Okunan: 113 aygırın babası, 80 aygırın yıllık tay verisi. 13 aygırda katalog toplamı yıllık satırlarla uyuşmuyor (ör. FALCO: 485 koşu / 542 galibiyet; kaynaktaki hata) → `uyusmazlik` işaretli; tabloda yıllık satırların toplamı ayrıca tutuluyor.
- Yalnızca İngiliz aygırları (Arap aygırları bu katalogda yok).
- Kullanım planı: katalog verisi 12.12.2025'te kesildiği için 2026 koşularında sızıntısız test edilebilir (uzun dönem aygır başarısı, bizim 560 günlük istatistiğe ek bilgi katıyor mu?).

## ganyancanavari.com.tr (robots.txt izin veriyor) – 19.11.2026
- Açık: takı değişiklikleri (bugünkü takıyla daha önce kazandıysa *), şehir değişiklikleri (bu şehirde daha önce kazandıysa *), koşmayan atlar, jokey değişiklikleri, pist durumu, yazılan atlar/bankolar, kullanıcı yorumları.
- Giriş gerektiren: galop incelemesi (kullanılmadı, engel aşılmadı).
- Kullanıcı yorumları/tahminleri veri değil kişisel görüş (ör. gayrı resmi "yarıştan çıkabilir" söylentisi) → modelde kullanılmaz.
- Takı ve şehir değişikliği TJK sonuçlarından da hesaplanabildiği için kendi verimizde test edildi (`scripts/sehir_taki_test.py`).
- Sonuç (7.228 koşu, binde): şehir değişti -0,22; şehir değişti + burada kazanmış +0,28; takı değişti -0,11; takı eklendi -0,05; takı çıkarıldı -0,14; bugünkü takıyla daha önce kazanmış +0,48 → hepsi önemsiz (hız puanı +4,5). Eklenmedi.

## Kullanıcı gözlemi (test edilecek): "Sabah ilk yayımlanan AGF'lerin doğruluk oranı yüksek; koşuya doğru AGF yüzdeleri değişiyor."
- TJK'daki "1./2. AGF Tablosu" günün 1. ve 2. altılısıdır (sabah/öğle değil) ve her zaman güncel değeri gösterir → ilk AGF geçmişi TJK'da saklanmıyor.
- `scripts/agf_kayit.py`: AGF değiştikçe saat damgalı görüntü (`veri/agf_kayit/<tarih>/<hipodrom>_<SSDD>UTC.csv`), ilk dolu AGF ayrıca `ILK_<hipodrom>.csv`.
- Her gün 08:00'den koşulara kadar saatte bir otomatik çalıştırılıyor. Yeterli gün birikince test: ilk AGF, son AGF ve kesin ganyanın kazananı tahmin isabeti (log-olabilirlik, favori kazanma oranı) karşılaştırılacak.
- 19.11 İzmir 1. koşu gözlemi: erken ganyanda LADY ECRİN 1,45 (favori), kesin ganyanda 2,30; kazandı. (Tek gözlem, kanıt değil.)

## Para girişi takibi (kullanıcı uyarısı: "yoğun para girişi olan atlara dikkat et") – 19.11.2026
- 19.11 İzmir 1. koşu: LADY ECRİN'e erken yoğun para (ganyan 1,45) fark edildi ama kullanılmadı (erken oranlar "oturmamış" sayıldı; koşu altılı dışında, model AGF'siz). Kazandı.
- `agf_kayit.py` artık her saat ganyanları da saklıyor (`<hipodrom>_<SSDD>UTC_ganyan.json`).
- `scripts/para_girisi.py`: ilk ve son kayıt arasında ganyandan türeyen olasılık ≥1,5× arttıysa (ganyan ≤20) ya da AGF payı ≥1,5× arttıysa (AGF ≥%5) 💰 işareti. `ganyan_kontrol.py` çıktısında gösterilir.
- 19.11 Antalya örnekleri (AGF 10:12 → 15:59): YOU ARE BIG %23→%70, SWORD MASTER %20→%51, CANSEFİRE %10→%27, DEĞERHAN %5→%13, BAŞKUT ANA %5→%14.
- Uyarı: AGF'nin bir kısmı mekanik değişir (sabah az kupon → dağınık yüzdeler). 1,5× eşiği 69 attan 14'ünü işaretledi; eşik veriyle ayarlanacak.
- **Henüz test edilmedi; olasılığa katılmıyor.** Test: işaretli atlar piyasaya (kesin ganyan) göre fazla mı kazanıyor? Kayıtlar biriktikçe.
- Yakın takip (kullanıcı isteği): koşu günü AGF + ganyan **10 dakikada bir** (`scripts/agf_dongu.sh`, 22:15'e kadar; kilitle tek kopya; saatlik görev durmuşsa yeniden başlatır).
- `scripts/takip_rapor.py GG.AA.YYYY Hipodrom [koşu]`: her koşunun en çok oynanan 5 atı için AGF ve ganyanın sabahtan koşuya seyri, bitiş ve kesin ganyan.
- 19.11 Antalya 6. koşu örneği: YOU ARE BIG AGF %23 (10:12) → %36 (11:31) → %70 (15:54); aynı anda ganyan 4,95 (havuz yeni). Altılı oynayanlar toplanmış, ganyan henüz değil.
- Kota: 10 dakikalık döngü bağımsız süreç olarak çalışır (model turu harcamaz); her kayıttan sonra kendisi GitHub’a kaydeder. Model turu gerektiren kontrol görevi günde 2 kez (07:03, 13:03): döngü durmuşsa başlatır.
- **4 nokta** (kullanıcı isteği): `takip_rapor.py` her koşu için AGF ve ganyanı 4 noktada gösterir: sabah ilk, öğle (12:30'a en yakın), koşudan 30 dk önce, 5 dk önce; yanında kesin ganyan ve sonuç. Döngü 5 dakikada bire indirildi (yalnızca değişince kaydeder).
- **Çekilen (koşmaz) atlar:** canlı takipte çıkarılır, olasılıklar koşanlar arasında yeniden dağıtılır (TJK çekilen atın bahsini iade eder). 19.11: İzmir 1. koşu WIN RIVER SOSAN, 4. koşu DRAGON RUNNER (v8/v6'nın 1. adayıydı; AGF %27–29 → %7) çekildi.

## Düzeltme: koşmayan atlar sonuç dosyalarında (19.11.2026)
- TJK sonuç CSV'lerinde koşmayan atlar sıra numarasıyla listelenir (derece = "Koşmaz"). 161.404 satırın 2.811'i (%2,8). Betikler bunları (a) kaybeden at sayıyor (alan büyüklüğü şişiyor, jokey/aygır/antrenör A/E hafif düşüyor), (b) koşu sayısına katıyor (deneyim/form), (c) ganyanı boş olduğu için bazı testlerde o koşuyu tümden dışlıyordu.
- `scripts/sonuc_temizle.py`: ham veri korunur, koşmayanlar çıkarılmış kopya `veri/sonuc_temiz/`. Günlük tablolar (hız puanı, jokey) ve model artık temiz kopyadan.
- Etki küçük: v9 AGF'li -1,845 → -1,844 (1. seçim %33,0 → %33,2); AGF'siz -1,947 → -1,945 (%31,2 → %31,5). Önceki bulguların hiçbiri değişmedi.

## Güven düzeyine göre isabet (v9, temiz veri, 542 görülmemiş koşu) – kullanıcı hedefi: %50 üstü
| Model 1. adaya | Koşuların % | 1. aday kazandı | İlk 2'de | 1. aday ganyan getirisi |
|---|---|---|---|---|
| hepsi | %100 | %33,2 | %53,5 | %79 |
| ≥%40 | %29 | %44,9 | %65,4 | %71 |
| **≥%45** | %20 | **%54,2** | %72,0 | %81 |
| **≥%50** | %13 | **%69,0** | %83,1 | %97 |
| **≥%60** | %6 | **%77,1** | %88,6 | %99 |
- %50 üstü isabet yalnızca seçici oynayarak mümkün (günde ~2 koşu). Ganyanlar düşük olduğu için getiri hâlâ ~başabaş.
- Her koşuda kazanan ilk 2 adayda %53,5 (ikili/çifte için).
- `analiz3.py` her koşuya güven düzeyini ve tarihsel isabetini yazar (★ ≥%45, ★★ ≥%50, ★★★ ≥%60). Yalnızca AGF'li model için geçerli; canlı testle doğrulanacak.

## beygir.com (robots.txt izin veriyor, /api/ hariç) – 19.11.2026
- **Muhtemeller:** her koşu için güncel ganyan, ikili, sıralı ikili, çifte muhtemel ödemeleri (TJK programında yalnızca ganyan var). `scripts/muhtemel_kayit.py` koşu günü 15 dakikada bir sayfa metnini sıkıştırarak saklar (`veri/muhtemel_kayit/`).
- Galoplar (son 10 idman, TJK kaynaklı): pegadrom'a yedek kaynak olabilir. AGF, sonuçlar: TJK'da da var.

## İkili / sıralı ikili değer testi (Benter yönü; `scripts/ikili_test.py`, `veri/ikili_test.txt`)
9.068 koşu (temiz veri), gerçek TJK ödemeleri; kazanma olasılığı: piyasa + geçmiş etkenleri (10 katlı gün CV); kombinasyon: Harville.
| Bahis | Kural | Bahis | İsabet | 1 TL getirisi |
|---|---|---|---|---|
| İkili | her koşu en olası kombinasyon | 6.092 | %17,0 | %77,1 |
| İkili | model > 1,3× piyasa (≥%3) | 2.846 | %7,4 | %91,6 |
| İkili | model > 1,6× piyasa | 81 | 4 | %134,3 (model 5,0 isabet bekliyordu → şans) |
| Sıralı ikili | her koşu en olası kombinasyon | 7.082 | %11,3 | %78,1 |
| Sıralı ikili | model > 1,3× piyasa | 4.082 | %6,1 | %89,4 |
| Sıralı ikili | model > 1,6× piyasa | 101 | 6 | %92,3 |
- Değer kuralı getiriyi %77 → %89–92'ye çıkarıyor ama başabaşın altında. Kanıtlanmış kâr yok.
- Sınır: piyasa çift olasılığı ganyandan (Harville) türetildi, gerçek ikili havuz fiyatı değil. beygir.com'dan kaydedilen gerçek ikili muhtemelleri biriktikçe tam test yapılacak.

## uatracing.com (19.11.2026)
- robots.txt üye sayfalarını yasaklıyor (canlı bülten, galoplar, tahminciler…) → girilmedi. İçerik çoğunlukla JavaScript/API ile yükleniyor.
- Açık bilgiler: 46.000+ anaçlık pedigri, 5 kuşak soy ağacı, **dozaj indeksi** (Chef-de-Race; soydan mesafe yatkınlığı), akrabalık katsayısı; AGF birincileri; sabit ihtimalli bahis açıklamaları. "Kim geçer %88,2 isabet" gibi iddialar doğrulanmamış reklam; kullanılmadı.
- Asıl faydalı ipucu: verilerinin TJK kaynaklı ve 1970'e uzandığı. Kontrol edildi: **TJK'nın kendi sunucusunda CSV sonuç dosyaları 2021 sonbaharından beri var** (Kasım 2021 var, Haziran 2021 yok). Kullanıcı isteğiyle çok eskiye gidilmedi: **Ocak 2024 – Mayıs 2025** arası indiriliyor (`.gunluk/eski_sonuc_indir.log`) → veri ~1,5 yıldan ~3 yıla çıkacak (2024 başından bugüne). Bittiğinde tablolar ve testler yeniden üretilecek.
- **Düzeltme (19.11):** erken saatlerde ganyan havuzu küçük ve oynak. VİÇE HANIM (Antalya 2): 15:59 6,20 → 16:28 2,20 → 18:10 1,75 → 18:31 7,55 → 18:42 7,15. "Son dakika para girişi" diye yanlış yorumlandı. 💰 artık yalnızca son 30 dakikadaki ganyan değişimine (≥1,4×) ya da AGF artışına dayanıyor.

## Maiden ve Şartlı 19: koşu kazanmamış atlar (test 19.11.2026, `scripts/maiden_analiz.py`, gerçek sonuçlar 2025-05-07 → 2026-11-18)
- **Tanım:** Maiden, hiç koşu kazanmamış atlara açık koşu (TJK programı: "koşu kazanmamış 2 yaşlı safkan İngiliz taylarına mahsustur" gibi). Kazanan at sonraki koşularında Şartlı 1'e geçer. Şartlı 19 da koşu kazanmamışlara açık. Numaranın şartnamedeki tam tanımı doğrulanmadı.
- 9915 koşu (kesin ganyanı tam olanlar), eküri tek bahis birimi:

| grup | koşu | favori kazandı | ganyan ≥10 kazanan | ganyan ≥20 kazanan | medyan kazanan ganyan |
|---|---|---|---|---|---|
| Tümü | 9915 | %35,5 | %15,4 | %4,6 | 3,80 |
| Kazanmış atların koşuları | 7669 | %35,6 | %15,1 | %4,0 | 3,75 |
| Maiden + Şartlı 19/27 | 2246 | %35,2 | %16,5 | **%6,3** | 3,85 |
| Maiden Arap 3 yaş | 846 | %33,1 | **%18,4** | **%7,9** | 4,20 |
| Maiden İngiliz 2 yaş | 590 | %38,5 | %15,1 | %5,6 | 3,42 |
| Şartlı 19/27 | 219 | %35,6 | %20,1 | %6,4 | 4,40 |
| Handikap (karşılaştırma) | 2891 | %31,5 | %18,5 | %5,1 | 4,35 |

- **Sonuç:** Maidende favori yine aynı oranda kazanıyor. Ganyan ≥20 kazanan %6,3, kazanmış atların koşularında %4,0. En sürprizli grup **3 yaşlı Arap maideni**. Örnek: 19.11 Antalya 2, CİHANDERE.
- **DÜZELTME (aynı gün, tüm koşu türleri testi):** bu fark alan büyüklüğünden geliyor. Maiden alanları kalabalık (ort. 10,6 birim, KV'de 7,6) ve piyasa bunu zaten fiyatlıyor. Maidende ganyan ≥10 kazanan %16,6, piyasanın beklentisi %19,3 (z −3,2). Yani **piyasanın beklediğinden FAZLA sürpriz yok, tersine az**. "Maiden sürprizli" ancak "oranlar dağınık" anlamında doğru.
- **Ama sürpriz atı oynamak yine kâr getirmiyor:** maidende ganyan 20–50 A/E 0,84, 50+ A/E 0,64 (piyasa beklentisinden az kazanıyorlar). Sürpriz daha sık geliyor ama hangi uzak ihtimalin geleceği önceden belli değil. Bu, analizde tek ata değil, kupon genişliğine işaret eder.
- **İlk kez koşan atlar piyasada fazla oynanıyor:** A/E 0,82 (90 galibiyet, 110 beklenen; 2025-09 sonrası). En belirgin olan İngiliz 3 yaşta ilk koşu: A/E 0,41 (7'ye 17). Örneklem küçük, izlenecek. Bu atlar analizde "İLK KOŞU" diye işaretleniyor.
- Son koşuda 2. ya da 3. olan maiden atları piyasa doğru fiyatlıyor (A/E 0,98–1,00). "Hep yaklaştı, bu sefer kazanır" diye bir avantaj yok.
- Günlük analiz: maiden koşularında bu uyarı satırı çıkar. Tablo her gün `gunluk.py` ile yenilenir (veri/maiden_analiz.json).

## Her koşu türünde ne geliyor? (test 19.11.2026, `scripts/kosu_turu_analiz.py`, 9915 koşu, veri/kosu_turu_analiz.json)
Favori = en düşük kesin ganyan; "beklenen" = piyasanın (ganyandan) verdiği olasılık. Eküri tek birim.

| aile | koşu | alan | favori kazandı | piyasa beklentisi | AGF favorisi | HP lideri | ganyan≥10 kazanan | piyasa beklentisi | medyan ganyan |
|---|---|---|---|---|---|---|---|---|---|
| Tümü | 9915 | 9,5 | %35,5 | %34,5 | %34,5 | %24,4 | %15,4 | %17,5 | 3,80 |
| KV | 1073 | 7,6 | %39,9 | %38,4 | %38,4 | %30,6 | %10,3 | %13,3 | 3,10 |
| Grup | 262 | 9,9 | %40,8 | %39,3 | %42,7 | %34,4 | %18,7 | %19,8 | 3,38 |
| Şartlı (1–5) | 3156 | 8,7 | %37,5 | %37,0 | %36,6 | %30,1 | %13,4 | %15,4 | 3,45 |
| Satış | 307 | 9,7 | %35,2 | %34,3 | %35,3 | %27,7 | %13,7 | %16,8 | 3,60 |
| Maiden + Şartlı 19/27 | 2220 | 10,6 | %35,3 | %34,0 | %33,9 | %24,0 | %16,6 | %19,3 | 3,85 |
| Handikap | 2891 | 10,3 | %31,5 | %30,1 | %30,6 | **%15,3** | %18,5 | %19,9 | 4,35 |
| Arap Handikap | 1327 | 11,1 | **%29,2** | %27,7 | %28,9 | %14,2 | **%21,4** | %22,1 | **4,80** |
| İngiliz KV | 651 | 7,3 | %40,7 | %39,5 | %39,5 | %31,2 | **%8,8** | %12,1 | **2,90** |

Bulgular:
- **En sürprizli tür Arap Handikap**: favori %29, ganyan≥10 kazanan %21, medyan kazanan 4,80. **En öngörülebilir tür İngiliz KV ve İngiliz Şartlı 4–5**: favori %41–42, sürpriz %9–12.
- **Hiçbir koşu türünde piyasanın beklediğinden fazla sürpriz yok.** Her ailede ganyan≥10 kazanan, beklenenin altında (toplam z −5,5; KV, Maiden, Şartlı ayrı ayrı anlamlı). Favori-uzak ihtimal yanlılığı her türde geçerli: favoriler beklenenden biraz çok, uzak ihtimaller az kazanıyor. Yine de favoriye düz oynamak 1 TL'ye 0,71–0,78 TL geri veriyor, yani zararda.
- **Handikapta HP lideri yalnızca %15 kazanıyor** (Şartlı'da %30, KV'de %31). Handikapta kilo puanı eşitliyor, HP'ye bakmak işe yaramaz.
- **AGF favorisi ile ganyan favorisi hemen hemen aynı.** Grup koşularında AGF favorisi biraz önde (%42,7, ganyanda %40,8; az örnek).
- Tek tek türlerde (ör. İngiliz Handikap 17, KV-7, Şartlı 3) |z|≈2–3 sapmalar var. Ama yaklaşık 140 karşılaştırmada birkaç tanesi şansla da çıkar; doğrulanmış sayılmaz.
- **Modelimiz (v9) türlere göre (görülmemiş 542 koşu, az örnek):** en iyi Handikapta, özellikle Arap Handikapta. 1. seçim %27 kazandı, favori %21; log-olabilirlik +140‰. Bu, piyasanın en zorlandığı yerde. İngiliz KV'de modelin üstünlüğü yok (1. seçim %35, favori %42,5; −3‰). Arap Şartlı'da ise fark yok (+2‰).
- Günlük analizde her koşunun başında bu türün geçmiş istatistiği yazılır (KOŞU TÜRÜ satırı). Tablo `gunluk.py` ile her gün yenilenir.

## Kaç at önermeli? Koşu türüne göre aday sayısı (test 19.11.2026, `kosu_turu_analiz.py` → `ilk_k`, `oneri_at`)
Kullanıcı önerisi: "sürprizli koşuda 3 değil 5 at öner". Gerçek veriyle ölçüldü: kazanan, piyasa sıralamasında ilk K at içinden ne sıklıkla çıkıyor (9915 koşu)?

| tür | koşu | ilk 3 | ilk 4 | ilk 5 | ilk 6 | önerilen (kazananın ≥%80'i) |
|---|---|---|---|---|---|---|
| Tümü | 9915 | %69,7 | %79,5 | %86,1 | %91,0 | 5 |
| Arap Handikap | 1327 | **%60,4** | %71,2 | %77,5 | %83,9 | **6** |
| Arap Maiden | 990 | %67,5 | %77,7 | %83,5 | %89,8 | 5 |
| İngiliz Handikap | 1564 | %68,0 | %78,0 | %84,8 | %90,0 | 5 |
| İngiliz Şartlı | 1715 | %75,9 | %84,3 | %90,2 | %95,0 | 4 |
| İngiliz KV | 651 | **%77,4** | %88,2 | %93,2 | %96,6 | 4 |

- Modelin (v9) sıralaması da aynı tabloyu verdi (görülmemiş 542 koşu): ilk 3 %67, ilk 5 %82. Arap Handikapta ilk 3 %53, ilk 5 %70.
- %80 eşiğini ben seçtim, keyfî bir eşik. Daha fazla at kapsamak kazanma ihtimalini artırır ama bilet maliyetini de artırır. Ganyanda kâra çevirmez (1 TL getirisi oran ne olursa olsun ~0,7). Asıl kullanım alanı altılı ve kupon ayak genişliği.
- **Gerçek örnek, 19.11 Antalya 2 (Arap Maiden):** sabah 11:44'te dondurulan tahminde CİHANDERE modelin 5. sırasındaydı (v9 ve v8). 3 at önerisinde dışarıda kaldı, 5 at önerisinde içeride olurdu. AGF'siz modelde 7. sıradaydı, orada da dışarıda kalırdı.
- Günlük analizde artık her koşuda "► ÖNERİLEN ADAY SAYISI" satırı var. Tahmin JSON'unda `oneri_at` alanı bulunur. Canlı testte "kazanan ilk K içinde mi" ayrıca izlenecek.

### Güncelleme: aday sayısı koşu türüne göre değil, KOŞUNUN KENDİ belirsizliğine göre (kullanıcı: "her koşuya 5 yazma, sadece içinden çıkılamayan koşulara çok at yaz")
- Kural: model olasılıkları büyükten küçüğe toplanır, toplam %75'e ulaşana kadar at eklenir (en az 1, en çok 6).
- v9 testi (535 görülmemiş koşu): ortalama 4,24 at, kazanan listede %78,5. Sabit 4 at %74,4, sabit 5 at %82,2. Aynı at sayısında sabit kurala göre ~+1,7 puan kazanç var. Piyasa olasılığıyla yapılan aynı test (9915 koşu) kazanç göstermedi: toplam ≥%75 kuralı 4,31 atta %81,5 verdi, sabit kuralla aynı. Yani fayda küçük. Asıl katkısı atları doğru yere koymak: net koşuya az, belirsiz koşuya çok.

| koşu sınıfı (aday sayısı) | koşu | liste tuttu | 1. aday kazandı |
|---|---|---|---|
| NET (1–2 at) | 49 | %85,7 | %67,3 |
| ORTA (3–4 at) | 256 | %77,0 | %34,0 |
| BELİRSİZ, SÜRPRİZE AÇIK (5–6 at) | 230 | %77,8 | %24,8 |

- Piyasada da aynı ilişki var: favori olasılığı <%25 olan 2114 koşuda favori %22,8 kazandı, ilk 5 %76,1. Favori ≥%50 olan 935 koşuda favori %60,7, ilk 3 %85,9.
- Altılı kuponu (`kupon.py`) zaten bu mantıkla çalışıyor: her adımda isabet artışı / maliyet artışı en iyi olan at eklenir. Belirsiz ayak genişler, net ayak tek kalır.
- **19.11 sabah verisiyle (11:31, koşulardan önce) geriye dönük kontrol, kural bugünkü koşulara göre ayarlanmadı:** İzmir 1 LADY ECRİN (ORTA 4, listede ✅), İzmir 2 ÖZASYALI (BELİRSİZ 6 ✅), İzmir 3 MADEİRA (BELİRSİZ 6 ✅), İzmir 4 ZENITH SKY (ORTA 4 ✅), İzmir 5 WOLF DED (ORTA 3 ✅), **İzmir 6 ÇORLİ (NET 1, QUEEN OF MUĞLA ❌; büyük sürpriz)**, İzmir 7 APOLLO MAXIMUS (BELİRSİZ 5 ✅), Antalya 1 SPIDER (NET 2 ✅), Antalya 2 CİHANDERE (BELİRSİZ 5 ✅). Sonuç 8/9. Tek gün, şans payı büyük; canlı testte izlenecek.

## Veri kaynağı: ebayi.org (TJK'nın resmî internet bayisi; robots.txt "Allow: /") — 19.11.2026
- Statik JSON: `https://ebayi.org/s/d/{program|sonuclar}/{YYYYMMDD}/yarislar.json` ve `.../full/{HIPODROM}.json` (ayrıca agf/, hava/, kosular/). 2024 günleri mevcut. 2022-10-10 için 404 döndü; o gün Antalya'da yarış olmayabilir, kesin alt sınır doğrulanmadı.
- At başına alanlar: KOD (benzersiz at kodu), BABA/ANNE/ANNEBABA ve kodları, JOKEY/SAHİP/ANTRENÖR kodları, KILO, HANDIKAP, AGF1/AGF2 (1. ve 2. altılı), GANYAN, SON6 (pist harfiyle, ör. K3C7 = kumda 3., çimde 7.), SON20, **KGS (son koşudan beri gün)**, TAKI, **SATISBEDELI (atın satış fiyatı)**, YETİŞTİRİCİ, KOSMAZ, EKURI; sonuçta SONUC, DERECE, FARK.
- Doğrulama: 18.11 İstanbul 1. koşu TJK CSV'siyle birebir aynı (DİLBERAN 1., ganyan 13,30, AGF %4,15).
- İndirme: `scripts/ebayi_indir.py .gunluk/ebayi 2024-01-01` (1 sn aralık, Türkiye hipodromları). Sonra satış bedeli, KGS ve anne babası özellikleri gerçek veriyle test edilecek.
- Sitede "sabit ihtimalli bahis" de var. TJK koşuları için sabit oran verip vermediği henüz incelenmedi.
- **Canlı takipte ebayi (19.11):** `canli_takip.py` sonuçları önce ebayi sonuç JSON'undan alıyor (KOSMAZ olan at çıkarılır). Koşu ebayi'de yoksa TJK program sayfasına düşüyor. İzmir'in 7 koşusu iki kaynakta birebir aynı çıktı. Antalya 3'ün sonucu (DEĞERHAN) ebayi'de TJK sayfasından önce yayınlandı.
- `agf_kayit.py` her turda ebayi program görüntüsünü de saklıyor: `veri/agf_kayit/<tarih>/<hip>_<SSDD>UTC_ebayi.json` → {koşu: {at: [AGF1, AGF2, canlı ganyan, koşmaz]}}.
- **ebayi muhtemeller (19.11):** sayfa `vhs.ebayi.org/muhtemeller/` herkese açık CDN dosyalarını okuyor: `vhs-medya.ebayi.org/muhtemeller/s/YYYY/AA/GG/checksum.json` (runs: HIP-NO → [kısa, tam]) ve `vhs-medya-cdn.ebayi.org/muhtemeller/s/YYYY/AA/GG/HIP-NO-full-<run>.json` (ganyan, ikili, sıralı ikili, çifte muhtemelleri, eküri işareti E, favori A, koşu DURUM). `agf_kayit.py` her turda ganyanı `<hip>_<SSDD>UTC_muhtemel.json` olarak saklıyor.
- Gün içi oran geçmişi (`s/h/...-GANYAN-0.json`) CDN'de yalnızca birinin daha önce açtığı koşular için duruyor (18.11 İstanbul: 9 koşudan 2'si). Sistematik geçmiş için kullanılamaz. Canlı geçmiş servisi (`data/history`, POST) herkese açık bir dosya değil, kullanılmadı.
- Örnek, Antalya 8 son dakika: ASİ GÖNÜL ganyanı 21:13'te 4,85 iken 21:31'de 1,65 (yoğun geç para girişi).
- **Düzeltme (19.11, kullanıcı uyarısı "kurgu yasak"):** sohbette "💰 işaretli 5 atın 3'ü kazandı" dedim. Bu sayıyı `para_girisi.py` çıktısından değil, aklımda kalan birkaç attan seçerek uydurdum. Gerçek çıktı, Antalya 19.11: **8 koşuda 72 at koştu, 22 at 💰 işareti aldı, 4'ü kazandı** (SPIDER, DEĞERHAN, CANSEFİRE, YOU ARE BIG; %18). İşaretin çoğu AGF ≥1,5× kuralından geliyor, sabah AGF'si az olan atlarda mekanik olarak tetikleniyor. Kural çok gevşek, veri biriktikçe test edilip daraltılacak. Ayrıca "KANDIRALI 4 atlık aday listesindeydi" dedim, yanlış: liste KAYANİLİM, ASİ GÖNÜL, BAŞKUT ANA, YIRTIL REHA idi.
- Kural: sohbette her sayı bir komut çıktısından gelecek. Komut çalıştırılmadıysa "kontrol etmedim" denecek.
- **İlk 2 isabeti (`scripts/ikili_takip.py`, 19.11, 15 koşu, program çıktısı):** v6 ve v8 ikili 5/15 (%33), sıralı ikili 3/15 (%20). AGF'siz ikili 6/15 (%40), sıralı ikili 5/15 (%33). AGF sırası ikili 3/14 (%21), sıralı 0/14. Antalya 8'de v6 ve v8 KAYANİLİM/ASİ GÖNÜL sıralı ikiliyi bildi. Tek gün; birikecek.
- **Kural (kullanıcı, 19.11): "AGF'ler yayınlanmadan başlama."** Analiz ve tahmin dondurma artık AGF yayınlanınca otomatik başlıyor. `agf_dongu.sh` her turda `agf_sonrasi_analiz.py`'yi çağırır. Bir hipodromun ilk AGF'si (ILK_<hip>.csv) kaydedilince `gunluk.py` analizi çalışır, AGF'li tahmin `veri/tahminler/<tarih>_<hip>.json` olarak, AGF'siz model aynı girdilerle `_agfsiz.json` olarak dondurulur. 20.11 için AGF'den önce yapılan ön analiz ve dondurulmuş AGF'siz tahmin geri alındı.
- **İlk AGF saati (19.11 gerçek kayıt):** 07:48'de (04:48 UTC) AGF yoktu, 10:12'de (07:12 UTC) 72 atın hepsi doluydu. Arada kayıt olmadığından yayın saati yalnızca "07:48–10:12 arası" diye biliniyor. Sabah ilk AGF'yi kaçırmamak için döngü artık **06:03**'te başlıyor (görev: 06:03, 08:03, 13:03, 17:03; sonraki ikisi sunucu yeniden başlarsa diye). Sabah ilk AGF ile koşuya doğru AGF ve ganyanın karşılaştırması `takip_rapor.py` ile yapılıyor: sabah ilk, öğle, −30 dk, −5 dk.
- **Koşu günü kayıt planı (kullanıcı, 19.11; `scripts/agf_plan.py`, `agf_dongu.sh` her dakika çağırır):** (1) 09:15–10:30 arası ilk AGF bütün hipodromlar için kaydedilene kadar 10 dakikada bir (kullanıcı, 20.11). 20.11'de AGF 09:26'dan önce yayınlanmıştı (dün 22:00'de yoktu); gerçek yayın saati bilinmiyor. İlk dolu AGF `ILK_<hip>.csv` olarak ham hâliyle saklanır ve hiç değiştirilmez, AGF gelince analiz yapılır ve tahmin dondurulur. (2) 12:00'de bir kontrol kaydı. (3) Her koşudan 1 saat önce bir kayıt. (4) Her koşudan sonra (başlangıç +15 dk) sonuç kontrolü: `canli_takip.py` → `veri/canli_takip*.csv`. Gün boyu sürekli kayıt yok. Görev 09:25'te döngüyü başlatır, 13:25 ve 17:25'te kapanmışsa yeniden başlatır. Durum: `.gunluk/<tarih>/plan.json`. Deneme: `PLAN_DENEME=1 PLAN_SIMDI=2026-11-20T14:00 python3 scripts/agf_plan.py`.
- **Beraber koşular (kafa kafaya) testi, 19.11 — YARIM KALDI (kullanıcı uzun sürdüğü için iptal etti):** 9168 test koşusu, piyasa −1,8249. `h2h_net`, yani bugünkü rakiplerle önceki karşılaşmalarda önde − arkada bitirme farkı, sonucu −1,8235, binde +1,42. Diğer 3 çeşit (oran, karşılaşma var mı, son karşılaşma) test edilmedi. Karar verilmedi, modele eklenmedi. `scripts/beraber_test.py` ile tekrar çalıştırılabilir, bir çeşit ~10 dk sürüyor.

## github.com/fatihbozdag/Ganyan (incelendi 19.11.2026) — benzer bir TJK tahmin projesi
- Python, ~29 bin satır, son güncelleme 2026-10. LightGBM LambdaRank + hiyerarşik Bayes Plackett-Luce + Harville (egzotik). Veri: tjk.org sayfaları + yarisrehberi.com.
- **Kendi dürüst sonuçları bizimkiyle aynı yönde:** gerçek para ROI'si negatif (ganyan top1 ≈ −%20, sıralı ikili ≈ −%13, üçlü ≈ −%32). "Ganyan havuzu etkin, AGF'yi yenemezsiniz; AGF-kör değer modeli takeout tabanını aşamıyor (test edildi)." Tarihsel top-1 %37,6 diyorlar, ama kendi notlarına göre yeni kodla doğrulanmamış; bizim v9 testinde %33,2. Ayrıca bir "+%583 ROI" iddiasını birim hatası (bilet 2 TL) yüzünden geri çekmişler. Birim hatasına dikkat: ödeme birimini her zaman gerçek biletle doğrula.
- Güven filtresi ("Bayes geçit": 1. aday ≥%35 olan yarışlar) bizim güven kademelerine (★/★★/★★★) benziyor; onlar da yararlı buluyor.
- **Bizde henüz test edilmemiş özellikleri** (ebayi verisi bitince gerçek veriyle test edilecek, eklemeden önce ölçülecek): SON20 skoru alana göre (s20_edge), son koşudan beri gün (KGS, rest fitness), kilo değişimi, mesafe değişimi, pist değişimi, alan tempo yoğunluğu, geç program değişiklikleri, komiser raporu ve jokey cezası.
- Kurulmadı ve kodu çalıştırılmadı. Yalnızca okundu.
- **Ganyan projesinin özellik fikirleri test edildi (19.11, `scripts/ganyan_ozellik_test.py`, `veri/ganyan_ozellik_test.json`):** ebayi sonuç JSON'ları, 16.189 test koşusu (2024-03 → 2026-09), piyasa (kesin ganyan, eküri tek birim) −1,7816, 10 katlı gün çapraz doğrulama, sızıntısız. Piyasaya katkı (binde): SON20 alana göre +0,04; dinlenme günü (KGS kovaları) +0,05; kilo farkı (önceki koşuya göre) +0,11; mesafe farkı +0,07; pist değişti −0,07. **Hepsi anlamsız derecede küçük** (karşılaştırma: hız puanı +4,5, galop +7,7). Piyasa bunları zaten fiyatlıyor. **Hiçbiri eklenmedi.** Ganyan projesinin kendi bulgusuyla aynı: halka açık sinyaller piyasada.
- Henüz test edilemeyenler: geç AGF kayması (para girişi; kendi kayıtlarımız birikince), güven izleme (trip-wire; sabahki ortalama 1. aday güveni ile 90 günlük ortalamanın karşılaştırılması, canlı veri birikince), jokey cezası ve komiser raporu (ayrı veri gerekir).
- **Plan (kullanıcı onayı, 19.11):** 2024 verisi tamamlanınca, eklenen verinin modeli görülmemiş koşularda iyileştirip iyileştirmediği test edilecek (aynı test koşularında eski/yeni eğitim karşılaştırması). **Fayda çıkarsa** ebayi'den daha eskisi çekilecek: sonuçlar 2020'ye, AGF Haziran 2022'ye kadar var. Fayda çıkmazsa çekilmeyecek.

## open-horse-data incelemesi (20.11.2026)
- Sheep-Meadow-Road-Games/open-horse-data: oyun (Horse Racing Manager) için 12 kaynaktan at + pedigri CSV'si üretir; veri repoda yok, betiklerle indirilir. Lisans MIT + atıf zorunlu (kullanılırsa Sheep Meadow Road Games / Horse Racing Manager adı ve linki).
- Türkiye kısmı: `fetch_tjk.py` TJK "Orijin" sorgu tablosunu (tjk.org/EN/YarisSever/Query/DataRows/Orijin, form POST, 50'şer satır, ~2.266 istek) indirir: ~113 bin at için baba, anne, anne babası, don, ülke. Yarış sonucu, derece, AGF, ganyan yok.
- Bizde zaten var: ebayi programında BABA/ANNE/ANNEBABA ve kodları; baba kanı modelde (v2'den beri), anne babası ve anne kardeş v11'de test edildi → gürültü düzeyi.
- Karar: kullanılmadı. Yeni bilgi yalnızca don ve ülke; tahmine katkısı test edilmedi, beklenen kazanç düşük. Repo klonlanıp okundu, betikler çalıştırılmadı.

## soyline.com (20.11.2026)
- Site şu an kapalı: soyline.com, www, .com.tr hepsi HTTP 402 "DEPLOYMENT_DISABLED" (Vercel) döndü.
- Arama sonuçlarına göre (doğrulanamadı, site açık değil): İstanbul merkezli pedigri platformu; soy ağacı sorgusu, akrabalık (inbreeding) renk kodlaması, aygır+kısrak sanal tay eşleştirmesi. Yarış sonucu/AGF/ganyan verisi görünmüyor.
- Karar: kullanılmadı. Soy bilgisi (baba/anne/anne babası) zaten ebayi'de var; anne babası/anne kardeş testi gürültü düzeyi çıktı.

## KynTr4/pedigreeall-ai (20.11.2026)
- Python ML hattı (logistic/CatBoost/XGBoost ensemble), SQLite ambarı, FastAPI pano. Repo klonlanıp okundu, çalıştırılmadı.
- Kendi raporu (reports/backtest_report_v2.md, 30.06.2026): 2026 holdout 1.642 koşu, kazananı bilme **%27,59**, top-1 ROI **−%28,94**; "Production ready: No". AGF karşılaştırması yok ("AGF value-bet test unavailable"). Karşılaştırma için bizde piyasa favorisi 9.915 koşuda %35,5 kazanıyor → bu model AGF/ganyan favorisinden zayıf.
- Komiser raporları: 356 PDF'ten 2.348 olay (661 jokey değişikliği, 664 koşmaz, 127 kurul olayı) çıkarılmış ama yarış verisiyle eşleşme **%0,04** (1 olay) → kullanılamaz durumda.
- Yeni olabilecek kaynaklar (TJK açık sorgu sayfaları): `tjk.org/TR/YarisSever/Query/DataRows/KomiserRaporlari` (komiser raporları) ve `tjk.org/AGFv2/{sehir}/{ggaayyyy}/TR/{tablo}/{sayfa}` (AGF sayfası). AGF ebayi'de zaten var. Komiser raporlarındaki "sıkıştı/engellendi" gibi olaylar ileride "sorunlu koşu" özelliği olarak test edilebilir; test edilmedi.
- Karar: model/kod alınmadı.

## 2024 verisi fayda testi (20.11.2026, `scripts/eski_veri_test.py`, ebayi verisi)
- Geçmiş özellikleri (jokey, antrenör, baba, atın kendi A/E'si) KISA (2025-05'ten) vs UZUN (2024-01'den) geçmişle. Eğitim 5.676 koşu (2025-07..2026-05), test 2.919 görülmemiş koşu (2026-06..2026-11-18).
- Sadece piyasa: LL −1,8439, favori %34,5.
- AGF'li (piyasa+geçmiş): KISA −1,8405 / UZUN −1,8397 → binde +0,76, z +0,99 → **anlamlı değil**.
- AGF'siz (HP+geçmiş): KISA −2,0710 (1. seçim %23,7) / UZUN −2,0626 (%23,8) → binde **+8,39, z +2,85 → anlamlı fayda**.
- Karar (kullanıcının kuralı: fayda varsa daha eskisi çekilir): ebayi 2020-01-01..2023-12-31 indirmesi başlatıldı (`.gunluk/ebayi_indir_eski.log`). Sonra AGF'siz modelin geçmiş tabloları uzun veriyle yeniden kurulup aynı testle ölçülecek.

## Hipotez (kullanıcı, 20.11.2026): sabah ham AGF → koşu öncesi AGF değişimi "gerçek" AGF'yi "sahte"den ayırır
- Durum: TEST EDİLMEDİ. Veri: sabah ilk AGF kaydı yalnızca 19.11 ve 20.11 (2 gün, ~30 altılı koşusu) → yetersiz.
- Test planı (yeterli veri birikince, hedef ≥ ~600 koşu ≈ 6-8 hafta): her at için sabah AGF, 12:00, −1 saat, son AGF ve kesin ganyan.
  1) AGF'si sabahtan sona artan / düşen / sabit atların kazanma A/E'si (beklenen = son AGF ve ayrıca kesin ganyan).
  2) Koşullu logit: piyasa (kesin ganyan) + log(son AGF / sabah AGF) → binde kazanç, iki yarıda da artı mı.
  3) Model 1. seçim isabeti: sabah AGF ile mi, son AGF ile mi, ikisi birlikte mi daha yüksek.
- Sonuç ne çıkarsa çıksın yazılacak; tahmin/kurgu yok.

## Kayıt planı GitHub Actions'ta (20.11.2026)
- Sebep: Claude konteyneri boşta kalınca kapanıyor, arka plan döngüsü ölüyor (20.11'de 4 kez).
- `.github/workflows/kayit.yml`: 09:10–10:40 her 10 dk, 11:00–23:45 her 15 dk `scripts/agf_plan.py` çalışır, kayıtları repoya yazar. Plan durumu `veri/plan/<tarih>.json` (git'te).
- Test (20.11 13:47 ve 13:50): TJK + ebayi erişimi çalıştı (Antalya 63/70, İzmir 49/54 at AGF), kayıt commit'lendi. Sabah analiz+dondurma (gunluk.py) Actions'ta henüz denenmedi → 21.11 sabahı ilk gerçek deneme.
- Konteyner döngüsü (agf_dongu.sh) ve 09:10/13:10/17:10 zamanlanmış görev kapatıldı (çift kayıt ve kota). Repo gizli; ücretsiz paket 2.000 dk/ay, plan ~50 çalıştırma/gün.

## Bahis birim fiyatları (kullanıcı, 20.11.2026)
- 3'lü ganyan: kombinasyon başı **2 TL** (42 kombinasyon = 84 TL, kullanıcının kupon ekranı). Altılı: **2 TL** (kullanıcı düzeltti; önce 1,25 demişti). En az oynama: **20 TL**.
- Kupon kayıtları: veri/kuponlar.csv.

## At geçmişi veritabanı (20.11.2026, kullanıcı isteği: "atları koştukça tanı, kim nerede nasıl geldi unutma")
- `veri/at_gecmisi/<yıl>/<gün>.csv.gz`: her at, her koşu (ebayi resmî sonuçları): hipodrom, koşu no/saat/tür/grup/mesafe/pist, koşan sayısı, at kodu/adı/yaş, baba/anne/anne babası, jokey/antrenör/sahip, kilo, HP, start, takı, AGF, kesin ganyan, sıra, derece, fark.
- İlk kurulum: 246.919 + 137 satır, 20.321 at, 25.640 koşu; 2020-01 → 2020-11 ve 2024-01 → 2026-11-19 (2020-12..2023 indirmesi sürüyor; bitince `at_gecmisi.py kur .gunluk/ebayi` yeniden).
- Günlük ekleme: GitHub Actions 23:00–23:45 çalıştırmalarında `at_gecmisi.py ekle <bugün> <dün>` (tekrar yazmaz). Sorgu: `scripts/at_bilgi.py "AT ADI"`.

## Asıl model (v9) uzun geçmişle (20.11.2026) – KABUL EDİLMEDİ
- Aygır/kulvar/jokey istatistikleri ve at geçmişi (gecmis_ozellik) KISA (veri/sonuc_temiz, 2025-05→) vs UZUN (+ .gunluk/sonuc_eski 2024-01→2025-05). Program verisi aynı (.gunluk/program, 2026-06-21→), eğitim 2.140, test 542 görülmemiş koşu (2026-10-19→).
- AGF'siz genel model: LL −1,956 → −1,953 (binde +3); 1. seçim %30,4 → %29,0; ilk 3 %59,6 → %61,8.
- AGF'li genel model: LL −1,846 → −1,847; 1. seçim %32,8 → %32,3; ilk 3 %66,4 → %66,6.
- 542 koşuda 1,4 puan ≈ 8 koşu → gürültü. Basit testteki (eski_veri_test, binde +8,4) fayda asıl modelde tekrarlanmadı; v9 zaten jokey/baba/form bilgisini başka özelliklerle taşıyor. Mevcut model değişmedi.
- Not: eğitim program arşivi scratchpad'den .gunluk/program'a kopyalandı (325 gün).

## Veri kaybı önlemi (20.11.2026)
- Git dışındaki arşivler repoya alındı: `veri/arsiv/ebayi` (ebayi sonuç JSON.gz, 76 MB), `veri/arsiv/sonuc_eski` (TJK sonuç CSV 2024-01→2025-05), `veri/arsiv/program` (eğitim programları 2026-06-21→11-17, scratchpad'deydi!). `.gunluk/{ebayi,sonuc_eski,program}` bu klasörlere sembolik bağ.
- Günlük programlar zaten `veri/agf_kayit/<gün>/` altında (AGF'li program CSV görüntüleri) git'te. 2020–2023 indirmesi bittikçe yeni dosyalar commit'lenecek.

## Belirsiz koşuda daha çok at (20.11.2026, kullanıcı: "belirsiz koşularda çok at yazılmalı")
- Test (v9, 542 görülmemiş koşu; belirsiz = %75 kapsama için ≥5 at gereken 233 koşu): eski kural (%75, en çok 6) belirsizde 5,47 at, isabet %78,1. %80/8: 6,23 at %86,3. **%85/8: 6,91 at %89,3** (seçilen). %85 sınırsız: 7,03 at %89,7.
- İsabet hedef kapsamayı izliyor (kalibrasyon iyi): daha çok at = daha çok isabet ama kupon pahalanır.
- Örnek 20.11 Antalya 3: kazanan SPEEDTAIL modelde 8. (toplam %89'a 8. atta ulaşılıyor) → yeni kuralla listede olurdu, eskisiyle (6 at) değildi.
- Uygulandı: scripts/analiz3.py (aday sayısı). Dondurulmuş tahminler değiştirilmedi.

## Kazananın AGF hareketi – ilk gözlem (20.11.2026, `scripts/agf_hareket.py`, 16 koşu: 19.11 + 20.11 Antalya 2-3)
- Kazanan, sabahtan koşuya AGF'si EN ÇOK artan at: 6/16; ilk 2'de: 8/16. AGF'si düşen ya da yerinde sayan (sessiz) kazanan: 7/16 (ör. 20.11 Antalya 3 SPEEDTAIL %6,9→%6,0, gny 16,75).
- Not: 19.11 ILK kaydının gerçek sabah ilk AGF olup olmadığı kesin değil (ILK zamanlaması 20.11'de düzeltildi). Örnek çok küçük, piyasa favorisi etkisinden ayrılmadı → TEST DEĞİL, gözlem. Test planı yukarıda (~600 koşu).
- Takip eklendi (kullanıcı): belirsiz koşularda (≥5 aday) AGF'si sessiz kalan atlar (sabah→son ≤1 puan, AGF ≥%2) `para_takip.py` ile 🤫 işaretlenir; `veri/para_takip.csv` sütunları belirsiz/sessiz. Test edilmedi; veri birikince kazanma A/E'si ölçülecek.

## Hipodrom sürpriz analizi (20.11.2026, `scripts/hipodrom_surpriz.py`, 18.027 koşu 2024+)
- Ganyan≥10 kazanan: Şanlıurfa %20,2 (ort. 11,5 at), Elazığ %18,4, Bursa %15,9, Kocaeli %15,3, İstanbul %14,9, Adana %14,3, Ankara %14,1, İzmir %13,1, Antalya %11,2.
- Piyasa beklentisine göre: hiçbir hipodromda beklenenden FAZLA sürpriz yok (Elazığ +0,3 puan ≈ 0; diğerleri eksi; İzmir z −4,2, Antalya −3,3). İki dönemde (2024-01..2025-06 / 2025-07..) yön aynı. Favori her yerde beklentiden biraz fazla kazanıyor (ör. Antalya %41,5 vs %34,7).
- Sonuç: "sürprizli hipodrom" = büyük alan (Şanlıurfa, Elazığ, Bursa). Bu, modelin olasılıklarında ve aday sayısı kuralında zaten var (düz dağılım → daha çok aday). Ek ağırlık eklenmedi; analiz raporuna hipodrom satırı eklendi (analiz3).

## Sürpriz kazanan takibi (20.11.2026, kullanıcı: "sürpriz gelenleri her noktadan analiz et, hepsini kıyasla")
- `scripts/kazanan_profil.py`: her koşunun kazananı → `veri/kazanan_profil.csv` (Actions'ta koşudan 20 ve 45 dk sonra otomatik). Sürpriz = kesin ganyan ≥10.
- Alanlar: model sırası (AGF'li/AGF'siz), aday sayısı, AGF sabah/son ve sırası, AGF farkı ve artış sırası, ganyan −60/−30/son/kesin, 💰/🤫, HP sırası, KGS, start, jokey, kilo, yaş, son 6; önceki koşusu (tarih, sıra, ganyan, jokey/pist/hipodrom/mesafe değişimi, tür).
- Karşılaştırma: `kazanan_profil.py ozet` (sürpriz vs diğer kazananlar). 20.11 itibarıyla 18 koşu, 2 sürpriz → yorum için çok az.
- Not: "sabah AGF" iki kaynakta farklı olabiliyor (TJK ILK CSV ör. LADY SOVEREIGN %9,27; ebayi ilk görüntüsü %15,41). Kazanan profili TJK ILK'i kullanır.

## TJK CSV AGF vs ebayi AGF (20.11.2026, aynı dakikadaki görüntüler, tam isim eşleşmesi)
- 09:26 (ilk yayın): Antalya 63 at ort. fark 3,2 puan (HASTA FINAL TJK %53,2 / ebayi %36,4); İzmir 49 at ort. fark 5,0 (O BİR ÇELİK TJK %72,1 / ebayi %36,1).
- 12:15 ve 14:51: ort. fark 0,02–0,16 puan → aynı veri (küçük fark çekim saniyesi).
- Yorum: ilk yayında iki kaynak senkron değil; en uç değerler TJK CSV'de (çok az kuponla ilk hesap olabilir – doğrulanmadı). "Sabah ilk AGF" çok oynak → AGF değişimi testinde ikinci bir sabah noktası (~10:00) ve 12:00 da baz alınacak. Kazanan profilinde TJK ILK; para_takip'te ebayi ilk görüntü.
- Kullanıcı (20.11): "İlk hangisinde çıkıyorsa doğru olan odur; sabah ikisinden de AGF çek." → Sabah kontrolü 5 dk'da bir, TJK ILK (ILK_<hip>.csv) VE ebayi ILK (ILK_<hip>_ebayi.json) alınana kadar sürer; ilk görülme saatleri `veri/agf_kayit/<gün>/ilk_zaman.json`. 20.11'de ikisi de 09:26 kontrolünde doluydu (hangisinin önce yayınladığı bilinmiyor).
- 20.11 17:15–19:45 Actions döngüsü push edemedi (Claude oturumu aynı CSV'leri – para_takip/kazanan_profil – elle yazınca rebase çakışması). Düzeltme: döngüde `pull --rebase -X theirs`, hata olursa rebase iptal. Kural: Claude oturumu bu CSV'leri elle yazmaz (yalnızca okur/ekrana basar). Kayıp: İzmir koşularının −60/−30/−10 görüntüleri (17:15–19:45).

## Sürprizlerin ortak noktaları (20.11.2026, `scripts/surpriz_ortak.py`, 2024+ gerçek sonuçlar, ganyanı ≥10 olan 88.216 at)
- Genel: ganyanı ≥10 atlar piyasanın beklediğinden AZ kazanıyor (A/E 0,90; 40+ ganyan 0,62).
- **Piyasanın küçümsediği sürprizler (iki dönemde de aynı yön):** HP sırası ilk 3 (A/E 1,30, z 7,1; 13.036 at); AGF payı ganyan olasılığının 1,3–2 katı (A/E 1,26, z 4,7; AGF'li koşular). AGF payı ganyanın ≤0,7 katı → A/E 0,47.
- İkisi birlikte (gny≥10 + AGF≥1,3× + HP ilk 3): 2.047 bahis, %8,0 kazandı, **1 TL ganyan getirisi %127** (2024 %126, 2025 %133, 2026 %121).
- UYARI: Bu testte KESİN ganyan ve kapanış AGF'si kullanıldı (koşudan önce kesin ganyan bilinmez) → canlıda koşu öncesi son görüntüyle ⭐ olarak ölçülüyor (`para_takip.py`, sütun sinyal). Canlı sonuç gelmeden bahis önerisi değil.
- İlk denemede AGF'siz koşular "AGF geride" sayılıp sahte sonuç verdi (A/E 1,94) → düzeltildi, yalnızca AGF'li koşular.
- Etkisiz/zayıf: jokey değişimi, pist/hipodrom değişimi, takı, ara süresi (>60 gün A/E 0,75), tür değişimi.
- Irk ve soy (kullanıcı fikri, aynı analiz): Arap sürprizler A/E 0,95, İngiliz 0,85 (z −5,7; iki dönemde aynı) → İngiliz uzak ihtimaller piyasanın beklediğinden de az kazanıyor; Arap sürprizler beklentiye yakın. Babanın o güne kadarki A/E'si ≥1,3 olan sürprizler A/E 1,11 (z 1,4, 5.098 at) → yön mantıklı ama anlamlı değil; 0,7–1,0 babalar 0,82. Soy etkisi piyasada büyük ölçüde fiyatlanmış.

## Sınıf düşüşü / yükselişi (20.11.2026, kullanıcı fikri, `scripts/sinif_dusus.py`, 2024+)
- Ölçü: son 3 koşudaki rakiplerin ortalama HP'si − bugünkü koşunun ortalama HP'si.
- Kötü formlu sürpriz adaylarında (gny≥10, son 3 ort. sıra ≥6) sınıf düşüşü piyasanın beklediğinden FAZLA kazandırmıyor: düşüş ≥10 A/E 0,95, 5-10 0,97 (anlamsız).
- Asıl etki ters yönde: daha güçlü rakiplere çıkan atlar (yükseliş ≥5) beklenenden az kazanıyor: tüm atlar A/E 0,92 (z −5,0), gny≥10 0,80 (z −5,9), kötü form+yükseliş 0,70; iki dönemde aynı.
- Tüm atlarda büyük düşüş (≥10) A/E 1,07 (z 2,9; 1,06/1,08) → küçük artı, getirisi %71 (kârlı değil).
- Modelde açık bir "sınıf farkı" özelliği yok → ileride özellik testi adayı (sinif_fark).
- **Modele ekleme testi (sinif_fark, v9 + 1 özellik, 542 görülmemiş koşu, `SINIF` ortam değişkeniyle):** AGF'li LL −1,846 → −1,846, 1. seçim %32,8 → %33,6 (≈4 koşu), ilk 3 %66,4 → %66,1. AGF'siz LL −1,956 → −1,951 (binde +5), 1. seçim %30,4 → %30,3; ağırlık +0,12 (sınıf düşüşü artı yönde). Fark gürültü sınırında → üretime alınmadı; veri birikince (daha çok program günü) tekrar test edilecek. Kapsama: program atlarının %77'si.

## "İlk kez" etkileri (20.11.2026, kullanıcı: DEDEMHAMZAREİS İzmir'de ilk kez koşup kazandı; `scripts/ilk_kez_test.py`, 2024+, en az 2 önceki koşusu olan atlar)
- İlk kez bu hipodromda (17.128 at): A/E 1,00 (z 0,0) → piyasa doğru fiyatlıyor; formu iyi olanlarda 1,03 (anlamsız); sürpriz adaylarında 1,00 (diğerleri 0,91).
- İlk kez bu kadar uzun mesafe (+100 m üstü, 12.094 at): A/E 1,04 (z 1,4); formu iyi + en uzun mesafe 1,08 (z 2,0; 1,10/1,06), getiri %74 → küçük artı, kârlı değil. Sürpriz adayı + en uzun mesafe 0,82 (zayıf).
- Sonuç: modele eklenmedi; tek örnekten (DEDEMHAMZAREİS) genel kural çıkmıyor.

## Atın kendi mesafe uyumu (20.11.2026, kullanıcı: "hangi at kısada, hangisi uzunda iyi"; `scripts/mesafe_uyum_test.py`)
- Bant: kısa ≤1400 / orta 1401–1900 / uzun ≥2000. Atın bugünkü banttaki sıra yüzdeliği − diğer bantlardaki (≥2+2 koşu, kronolojik).
- Sonuç: tüm gruplarda A/E ≈1 (belirgin iyi 1,00; belirgin kötü 1,03; z <1,5) → piyasa atın mesafe uyumunu tam fiyatlıyor. Modelde zaten pist_mesafe_galibi ve baba kanı (mesafe bandı) var; ek özellik eklenmedi.
- Bilgi olarak: `at_bilgi.py` artık her atın kısa/orta/uzun ve pist bazında koşu/birincilik/ilk 3 sayısını gösteriyor.

## Günlük rapora eklenenler (20.11.2026, kullanıcı: "yorum yapma, analizlere ekle")
- `scripts/at_notlari.py` + analiz3: her koşuda adayların altında **AT GEÇMİŞİ** satırı: koşu/birincilik, kısa/orta/uzun ilk 3 kaydı, İLK KEZ <hipodrom>, İLK KEZ bu uzunluk (formu iyiyse testli not), sınıf farkı (rakipler son 3 koşuya göre daha zayıf/güçlü, ±HP), son koşusu. Yalnızca analiz gününden önceki veriler.
- **⭐ SÜRPRİZ ADAYI** işareti (gny 10–500 ve piyasa oturmuş, AGF ≥1,3× ganyan olasılığı, HP ilk 3).
- Raporun başında HİPODROM sürpriz satırı (önceden eklendi).
- Mesafe değişimi testi (`veri/mesafe_degisim_test.json`, 2024+): bu tam mesafede ilk kez A/E 1,03 (z 2,1; 41.876 at), formu iyiyse 1,06 (z 2,6; 1,08/1,03); en kısa mesafe formu iyi 1,17 (359 at, az); son koşuya göre ±200–400 m değişim 0,99–1,05 (anlamsız). Getiriler %61–86 (kârlı değil). Rapora etiket olarak eklendi: İLK KEZ <m>, EN KISA, son koşuya göre ±m.
- Kullanıcı (20.11): "at seçerken bunlara da bak" → analiz3: listenin hemen dışındaki 3 attan olumlu geçmiş etiketi (formu iyi + ilk kez mesafe/en uzun/en kısa, ya da rakipler DAHA ZAYIF) olanlar **EK ADAY**; listedeki atlarda rakipler DAHA GÜÇLÜ ise **UYARI**. Olasılıklar değişmez; JSON'da `ek_aday`. TEST EDİLMEDİ → canlı takip. 20.11 İzmir üzerinde deneme: 4. koşuda UYARI alan DEDEMHAMZAREİS kazandı (uyarı tek başına güçlü değil).

## Soy x ırk x mesafe (20.11.2026, kullanıcı; `scripts/soy_mesafe.py`, at_gecmisi tüm yıllar, ≥40 koşu)
- Her ırk+bant için babaların kazanma %, ilk 3 %, A/E (alan büyüklüğüne göre) ve piyasa A/E'si: `veri/soy_mesafe.json`.
- Öne çıkanlar (A/E alan): Arap kısa AFRİKAANDER (300 koşu %19,3), Arap orta ŞİMŞEĞİNOĞLU (361, %13,9) / ALTAHA (465, %14,2), Arap uzun GÜRSU (95, %20) / YILMABAŞAR (167, %18); İngiliz kısa+orta TOUGH GUY (%31,6 / %30,5), İngiliz uzun MY DEAR SON (41, %31,7), KING DAVID (74, %20,3).
- Not: çok baba arasından en iyiler seçildiği için küçük örneklerde (40–60 koşu) değerler abartılı olabilir. Raporda AT GEÇMİŞİ satırına "soy … bant: kazanma/ilk3/A/E" eklendi (bilgi; modelde baba kanı zaten var).

## Kullanıcı analizleri modelin içinde (20.11.2026, `scripts/ek_ozellik.py`, model9 + 8 özellik, 542 görülmemiş koşu)
- Özellikler: sınıf farkı, ilk kez hipodrom, ilk kez mesafe, en uzun, en kısa, mesafe değişimi, soy-bant A/E (kronolojik), formu iyi × yeni mesafe.
- AGF'li: LL −1,846 → −1,845; 1. seçim %32,8 → %33,9 (≈6 koşu); ilk 3 %66,4 → %64,9; 1. seçim getirisi %80 → %87.
- AGF'siz: LL −1,956 → −1,950 (binde +6); 1. seçim %30,4 → %30,4; ilk 3 %59,6 → %60,1.
- Ağırlıklar küçük (en büyük: sınıf farkı +0,12 AGF'siz, en uzun mesafe −0,08/−0,09). Fark gürültü sınırında → üretim modeli değişmedi; özellikler `EKOZ` ile hazır, veri birikince yeniden test. Rapor etiketleri ve takip sürüyor.
- **ÜRETİME ALINDI (kullanıcı talimatı, 20.11.2026 ~21:30):** `veri/ek_agirlik.json` (AGF'li ve AGF'siz için 8 ağırlık, test modelinden), analiz3 bu 8 özelliği her at için hesaplayıp skora ekler (`at_notlari.ek_vektor`). 21.11'den itibaren dondurulan tahminler bu modelle. 20.11 koşularında yeniden hesap (sabah verisiyle): kazananların sırası 12 koşunun 10'unda aynı; İzmir 2 BOLD VOFİ 5. → 4. (listeye girdi), Antalya 2 SABIRLI RIBELLA 3. → 4.; sürprizler (SPEEDTAIL 8., WINGS OF FREEDOM 10., ERBAALI SADİ 7.) değişmedi. Canlı takiple izlenecek.
- Kazanan profiline (20.11 gece) tüm kullanıcı analizleri eklendi: ırk, sınıf farkı, ilk kez hipodrom/mesafe, en uzun/kısa, mesafe değişimi, soy-bant, formu iyi×yeni mesafe, ⭐ sinyal. Gün sonunda Actions `kazanan_profil.py guncelle <bugün> <dün>` ile eksik alanları (ör. İzmir 3 ganyan/para) tamamlar. `goster` modu dosyaya yazmadan gösterir.
- 20.11 sürprizleri (4): SPEEDTAIL 16,75, WINGS OF FREEDOM 26,60, ERBAALI SADİ 18,45, TUNCER 10,65. Model sırası 8/10/7/8. HP sırası 2/9/6/2. Sınıf farkı +5,2/+5,6/−6,9/−0,8. Mesafe son koşuya göre −100/+200/−100/−100. Hiçbiri ⭐ almadı. 3'ü İngiliz.

## Kan analizi: baba hattı ve anne babası (21.11.2026, kullanıcı; `scripts/kan_hatti.py`, at_gecmisi tüm yıllar, ≥60 koşu)
- Baba hattı = babanın babası (at_gecmisi'nde babanın kendi kaydı ya da aygır kataloğu). Anne babası = kısrak babası. Irk x bant (kısa/orta/uzun) için kazanma %, ilk 3 %, A/E (alan) ve piyasa A/E: `veri/kan_hatti.json` (ayrıca `baba_babasi` eşlemesi).
- Öne çıkanlar (A/E alan): Baba hattı – Arap kısa CAŞ (162 koşu, %15,4), PERFECTO (420); Arap uzun WIN RIVER WIN (102, %14,7), BOSPORUS (169); İngiliz kısa KINGMAN (111, %21,6), KURTINIADIS (505, %17,2), SHARP HUMOR (428); İngiliz orta PIVOTAL (1.506, %13,6); İngiliz uzun WAR FRONT (79, %19), PIVOTAL (946, %15), SEA THE STAR (231). Anne babası – Arap kısa SULTAN DE FAUST, DAYIBEY (246); Arap uzun SEZGİNBEY (204), YALAZ (237); İngiliz kısa DISTORTED HUMOR (187, %25,7); İngiliz orta PRESSING (175); İngiliz uzun NAYEF, SHAMARDAL.
- Not: piyasa A/E çoğunlukla 1'in üstünde ama küçük örneklerde abartılı olabilir. Raporda AT GEÇMİŞİ satırına "baba hattı … / anne babası …" eklendi. Modelde baba kanı ve kısrak babası notu (KB) zaten var.

## Grup (koşu türü) düşüşü (21.11.2026, kullanıcı: "6-7-5 bitirmiş olabilir, güçlü gruptan zayıf gruba geçer, birinci olur")
- Tür seviyesi = o koşu türünün ortalama HP'si (`scripts/tur_seviye.py` → `veri/tur_seviye.json`, 32 tür; ör. KV-8 78,4, Handikap 21 76,4). Grup düşüşü = son 3 koşunun tür seviyesi − bugünkü (ek_ozellik'te kronolojik).
- Test (2024+, gerçek sonuçlar, piyasa beklentisine göre): grup düşüşü ≥8 → A/E 1,06 (z 3,4; 24.519 at; 1,06/1,07); **≥8 düşüş + son 3 ort. sıra ≥5 (kötü görünen form) → A/E 1,06 (z 2,1; 15.302 at; 1,02/1,09)**; 3–8 düşüş 0,98; grup yükselişi ≥3 → 0,96 (z −2,6). Getiriler %61–70.
- Rapora eklendi: AT GEÇMİŞİ'nde "GRUP DÜŞÜŞÜ (+x HP; son 3: tür sıra/koşan …)" ya da "GRUP YÜKSELİŞİ". Model özelliği olarak da (e_grup_dusus, e_kotu_form_x_dusus) + anne babası ve baba hattı mesafe bandı (e_annebaba_bant, e_baba_hatti_bant) test ediliyor.
- **12 özellik testi (8 + anne babası bandı, baba hattı bandı, grup düşüşü, kötü form×grup düşüşü; 542 görülmemiş koşu):** AGF'li LL −1,853 (8 özellikte −1,845, önce −1,846), 1. seçim %32,8; AGF'siz LL −1,956 (8'de −1,950), 1. seçim %29,5. Grup düşüşü ağırlığı artı (+0,06/+0,08) ama sınıf farkıyla örtüşüyor (sınıf ağırlığı −0,02'ye düştü) ve toplamda tahmin KÖTÜLEŞTİ → üretimde 8 özellikli model kalıyor (ek_agirlik.json 8 ağırlık; ek_vektor ilk 8'i aynı). Grup düşüşü ve kan bantları raporda not olarak, kazanan profilinde takipte.
- AGF'siz ayrıştırma (542 koşu): 8 özellik LL −1,950 / 1. %30,4 / ilk3 %60,1; +grup düşüşü −1,955 / %29,5 / %60,1; +kan bantları −1,951 / %29,9 / **%60,9**; 12'si −1,956 / %29,5 / %60,5. Hiçbiri 8 özellikli modeli LL'de geçmedi; kan bantları ilk 3'ü +0,8 puan (≈4 koşu) artırdı ama 1. seçimi düşürdü → değişiklik yok, 8 özellik kalıyor.
- **21.11 Actions arızası (kendi hatam):** (1) numpy kullanıcı dizinine kuruluyordu, betikler `python3 -I` ile çalıştığı için göremedi → analiz çalışmadı; (2) gunluk.py başka izlenen dosyaları da değiştirdiği için `git pull --rebase` reddetti → hiçbir kayıt gönderilemedi. Ayrıca zamanlanmış ilk çalıştırma 09:05 yerine 10:02'de başladı (GitHub gecikmesi). Düzeltme: numpy sistem geneline, pull `--autostash`. 21.11 AGF ilk kaydı 12:12'de konteynerden alındı (sabah ilk AGF DEĞİL), tahminler 12:15'te donduruldu.
- Sabah başlangıcı: kullanıcı kararı 22.11'de 08:00 İstanbul'a çekildi (cron 05:00 UTC; önce 09:15'ti, ama 09:15'te AGF zaten yayınlanmış olabildiği için ilk yayınlayan bilinemiyordu); 08:00–10:30 her 5 dk sabah AGF kontrolü (agf_plan.py).

## TJK CSV önbelleği ve güven aralığı (22.11.2026)
- **Bulgu:** TJK program CSV'si `medya-cdn.tjk.org` üzerinden `cache-control: max-age=600` ile geliyor. Düz adres 10 dakikaya kadar eski olabiliyor (22.11 12:45'te İzmir: `age: 560`, `last-modified` 09:30; `?t=<unix>` ile alınan güncel dosya 09:42). Adana'da aynı anda fark yoktu (önbellek o an yeniydi).
- **Düzeltme:** `agf_kayit.py` artık CSV adresine `?t=<unix>` ekliyor (önbellek atlanır). Bu değişiklikten önceki TJK görüntüleri 10 dakikaya kadar geç olabilir.
- **Yorum uyarısı:** 20.11'deki "TJK ile ebayi sabah ilk yayında farklı" ve `DOGRULUK.md`'deki TJK'nın hafif geride çıkması kısmen bu önbellekten olabilir. Yeni veriyle (22.11 öğleden sonra ve sonrası) tekrar bakılmalı. "İlk yayınlayan" tespitinde TJK'nın ilk görülme saati önceki günlerde gecikmeli olabilirdi.
- **Güven aralığı:** `scripts/guven_araligi.py` model - AGF farkını koşu-eşli bootstrap ile %95 aralıkla verir (`veri/agf_kayit/GUVEN_ARALIGI.md`, günün sonunda otomatik). 46 koşuda her iki model için de aralık sıfırı içeriyor: fark kanıtlanmış değil.
- Not: bu iki fikir `nino0435/ganyan-model` raporlarındaki yöntem açıklamalarından alındı (kodu açılmadı, lisansı yok); uygulama sıfırdan yazıldı.


## Sürprizler nerede çıkıyor? (22.11.2026, `scripts/surpriz_nerede.py`, 17.806 koşu 2024+)
- Sürpriz = kazananın kesin ganyanı ≥10. Gerçek oran **%15,1**, piyasanın beklediği %16,8 (A/E 0,90). Uzun atlar her yerde fazla oynanıyor.
- **Ham oran at sayısına bağlı:** 5–8 at %8,8 · 9–11 %15,3 · 12–14 %23,8 · 15+ %29,8. Sürprizleri karşılaştırırken sayıdan çok **A/E** (gerçek/beklenen) bakılmalı.
- Ham orana göre yüksek: Şanlıurfa %20,2, Elazığ %18,6, handikap %18,7, çim %16,6, haziran–ekim ~%16–17. Düşük: Antalya %11,4, KV %10,4, şubat %11,9, aralık %11,7.
- **Piyasadan fazla sürpriz çıkan (A/E>1) anlamlı hiçbir segment yok.** En yakınlar: <1200 m (1,09, n=477, z=+0,9), Elazığ 1,02 — ikisi de gürültü.
- Uzun atların en çok abartıldığı (A/E düşük, z≤−3): Antalya 0,78 · İzmir 0,82 (ikinci yarıda 0,75, z=−4,4) · KV 0,80 · sentetik pist 0,82 · şartlı 0,86 · 9–11 at 0,86 · şubat 0,76. İzmir ve Antalya iki yarıda da aynı yönde.
- ~50 segment denendi; z≥3 olanlarda bile bir kısmı tesadüf olabilir. Sürpriz avlamak için bir "av sahası" bulunamadı.

## Yüzeyde "ilk kez" (22.11.2026, `scripts/yuzey_ilk.py`, 126.912 at-koşu, 2024-07+, en az 2 önceki koşusu olan atlar)
- Hipodromda ilk kez zaten ölçülmüştü (A/E 1,00). Burada **pist yüzeyi** (kum/çim/sentetik): bu yüzeyde ilk kez koşan atlar 7.196, kazanma %8,77 / piyasa beklentisi %8,07 → A/E **1,09 (z +2,3)**, getiri **−%36**. Daha önce koşanlar A/E 1,01.
- **Kalıcı değil:** ilk yarıda 1,14 (z +2,7), ikinci yarıda 1,03 (z +0,6). Yüzeye göre: kum 1,03 · çim 1,12 (z 1,6) · sentetik 1,12 (z 1,9).
- Önceki koşuya göre yüzey değişimi: farklı yüzey A/E 1,01, aynı yüzey 1,01 → fark yok. Geçiş çiftlerinin hepsi 0,99–1,05. O yüzeydeki koşu sayısına göre örüntü yok (0: 1,09 · 1–2: 1,02 · 3–9: 1,02 · 10+: 0,97).
- Sonuç: küçük ve kalıcı olmayan bir fark, kâr getirmiyor. Modele eklenmedi. Uyarı: geçmiş 2024'ten başladığı için "ilk kez" bazı atlarda yanlış olabilir.

## AGF'ye göre sürpriz tanımı (22.11.2026, `scripts/agf_surpriz.py`, 11.949 koşu 2024+, kapanış AGF; yalnızca altılıya giren koşular)
- **Ortalama AGF %, sıraya göre:** 1. 34,8 · 2. 19,9 · 3. 14,1 · **4. 10,2** · 5. 7,3 · 6. 5,3 · 7. 3,9 · 8. 2,9. İlk 3 toplam %68,7, ilk 4 %79,0, ilk 5 %86,2. 4. atın AGF'si at sayısından bağımsız ≈%10 (5–8 at 9,8 · 9–11 10,7 · 12–14 10,3 · 15+ 9,8). **%10 eşiği ≈ "ilk 4 dışı".**
- **Sürpriz sıklığı (kazanan şu tanımın içinde):** AGF sırası >3 %30,9 · >4 %20,6 · >5 %13,7 · >6 %8,8. AGF % <15 %38,8 · <12,5 %30,5 · <10 %22,7 · <7,5 %15,5 · <5 %8,8. Kıyas: kesin ganyan ≥10 %14,8 ≈ AGF <7,5 ≈ sıra >5.
- **Kapanış AGF iyi kalibre:** her eşikte gerçek/beklenen 0,96–1,01 (ganyan ≥10 için 0,90'dı). İlk/ikinci yarıda biraz ters yönde (0,87–0,97 → 1,01–1,08), ortalama 1,0.
- **At sayısına göre değişiyor:** 9–11 atta sürpriz AGF'nin beklediğinden az (sıra >4: A/E 0,91, z −3,3), 12–14 ve 15+ atta biraz fazla (sıra >5: 1,09 z +2,3 / 1,12 z +1,7). Ham sürpriz oranı da ciddi değişiyor (sıra >4: 5–8 at %12,4 · 9–11 %21,9 · 12–14 %32,4 · 15+ %37,8).
- **Getiri:** eşik altındaki atların hepsine düz oyun getirisi %42–62 (yani zarar).
- Öneri: "sürpriz" = AGF %10 altı (≈ilk 4 dışı), "büyük sürpriz" = AGF %5 altı. Karşılaştırmada ham oran değil A/E kullan. Not: canlı takipte sabah/−60 dk AGF kullanılırsa kapanış AGF'den 1–3 puan oynayabilir.

## Yapılacak testler (22.11.2026)
- Bekleyen test ve fikirler `YAPILACAK_TESTLER.md` dosyasında (önkoşul, ölçüt, kurallarla). Yeni testleri oraya ekle, yapılanları ✅ işaretle ve sonucu burada ayrıca yaz.

## Sürprizler ayrı kayıt (22.11.2026, `scripts/surpriz_ayri.py`)
- `kazanan_profil.csv`'yi okuyup sürpriz kazananları **ayrı** dosyaya çıkarır (gün sonu otomatik): `veri/agf_kayit/surpriz_ayri.csv` (tüm günler) ve `veri/agf_kayit/<tarih>/SURPRIZ.md` (o günün kartları + toplam karşılaştırma). `kazanan_profil.py`'ye dokunulmadı.
- Tanımlar (etiketli): **G** ganyan ≥10 · **A10** kapanış AGF <%10 · **AS10** sabah AGF <%10 · **A5** kapanış AGF <%5. Notlar kural tabanlı ("olası"), neden değil.
- 22.11 sürprizleri: İzmir 4 Supertramp (kesin 10,2; AGF 6,6→5,1; start 1, jokey değişti, mesafe −400 m, model 3.), İzmir 5 Chumlee (10,7; AGF 7,3→6,0; start 1, jokey değişti, mesafe +500 m, önceki koşuda favori 6. bitmişti), Adana 2 Selim Usta (12,75; AGF %4,7 hareketsiz 🤫, ganyan son 30 dk'da 26,9→12,1 💰; maiden, pist yüzeyi değişti). Sınır vaka: İzmir 8 Başar Soylu (sabah AGF %7,1 → %11,8, 💰; AGF'siz model 1. sıraya koymuştu).
- Toplam (22.11 itibarıyla, G: 10 sürpriz): jokey değişti %80 (diğer kazananlar %58) · 🤫 %56 (%20) · 💰 %11 (%43) · AGF'li model ilk 3'te %10 (%82) · iç kulvar %50 (%33). Örnek çok az, yorum değil gözlem.

## 22–24 Kasım kontrolü (25.11.2026)
- **Sistem çalıştı:** cron-job.org tetiği 07:55'te GitHub'ı başlattı (23, 24 ve 25.11 ilk Actions commit'i 07:55). 22.11: 94, 23.11: 117, 24.11: 114 Actions commit'i.
- **İlk yayın (08:00 penceresi, TJK önbelleksiz):** 23.11 eBayi **09:01**, TJK **09:06** (eBayi 5 dk önce). 24.11 ikisi de **09:05**. AGF yaklaşık 09:00–09:05'te yayınlanıyor. 5 dk çözünürlük.
- **Doğruluk (`DOGRULUK.md`, 5 gün):** eBayi kapanış AGF'ye daha yakın (0,699 puan; TJK 0,743). Önbellek düzeltmesinden sonra (23: 0,748 / 0,837; 24: 0,935 / 0,977) fark küçüldü ama sürüyor. TJK CSV'sinin kaynak dosyası da birkaç dakikada bir yenileniyor olabilir (doğrulanmadı).
- **Tahmin sonuçları (22–24, 48 koşu, ilk seçim 1. bitti):** AGF'li model 11 (%23), AGF'siz 13 (%27), AGF favorisi 13 (%27). Günlük: 22.11 5/5/6 (16 koşu), 23.11 4/5/5 (17), 24.11 2/3/2 (15). Güven aralığı (94 koşu): iki model için de aralık sıfırı kapsıyor.
- **Sürpriz oranı:** ganyan ≥10: 22.11 %25 (4/16), 23.11 %29 (5/17), 24.11 %25 (4/16), genel beklenti ~%15; AGF %5 altı büyük sürpriz 1, 4 ve 2 tane. Bu 3 gün sürprizli geçti.
- **Veri sorunu (düzeltildi/raporlandı):** 08:00 penceresi AGF'nin ilk yayınını yakalıyor ama o an **kısmi** (23.11 Şanlıurfa ilk görüntüde 104 attan 33'ünün AGF'si dolu, kalanı %0). `kazanan_profil.csv`'deki `agf_sabah`, `agf_fark`, `agf_artis_sira` ve 💰/🤫 işaretleri bu yüzden 23.11'den itibaren bozuk (sahte "AGF 0→17 para girişi"). `surpriz_ayri.py` artık ilk görüntüde doluluk <%80 ise AS10 vermiyor ve "sabah AGF kısmi" uyarısı yazıyor. Kalıcı çözüm: `YAPILACAK_TESTLER.md` madde 22.

## yenibeygir.com incelemesi (25.11.2026)
- **Ne:** TJK bülteninin yeniden düzenlenmiş hâli, tarih/hipodrom/koşu adresiyle (`/25-11-2026/elazig`, `/<tarih>/<hip>/<koşu>/sonuclar|derece|galoplar|jokeyperformans|karsilastirma|pistmesafe|stiller`), geçmiş günler dahil. At, jokey ve antrenör sayfaları var.
- **AGF:** tamsayı olarak (virgülden sonrası yok). Geçmiş testte 24.11 Adana 4. koşuda yenibeygir AGF'si eBayi'nin **AGF2** (2. altılı) değerinin yuvarlanmışı (toplam mutlak fark 2,5; AGF1'e 10,9). Yani kapanış AGF'nin kaba kopyası, bizim TJK/eBayi kaydımız (2 ondalık) daha ince.
- **Yeni bilgi:** koşu **stilleri** (`/stiller`, lider/takip vb. + veri sayısı; v9'da ve `BILGI.md`'de YOK), hazır baş-başa matrisi (`/karsilastirma`), pist-mesafe analizi (`/pistmesafe`, `pist_mesafe_galibi` ile örtüşür), derece ve galop sayfaları. Hepsi kendi geçmiş verimizden de türetilebilir (stil hariç).
- **Dikkat 1, kullanım şartları (madde 4):** "İzinsiz veri kazıma (scraping), otomatik tarama veya ticari yeniden yayınlama amacıyla sistem kaynaklarının aşırı tüketilmesi yasaktır." **Otomatik çekim eklenmedi ve önerilmez**; incelemede elle birkaç sayfa okundu. İzin gerekirse site sahibine (İletişim) sorulmalı. robots.txt yalnızca bazı site kopyalama araçlarını engelliyor, genel tarayıcıya kural yok, ama şartlar ayrıca geçerli.
- **Dikkat 2, ERKEN YAYIN SORUSU (açık):** 25.11 08:26'da yenibeygir Elazığ için tam AGF gösteriyordu (1. koşu toplam %95) iken TJK AGF sayfası boştu ve bizim TJK CSV/eBayi kayıtlarında AGF yoktu (ilk yayın bizde ~09:00–09:05). Bu ya yenibeygir'in daha erken kaynağı, ya da eski/başka veri. Karar: bugün bizim ilk AGF'miz gelince karşılaştır (`YAPILACAK_TESTLER.md` madde 23).

## yenibeygir akşamdan AGF yayınlıyor (kullanıcı bilgisi, 25.11.2026) — ayrı takip
- Kullanıcı: yenibeygir AGF'yi **akşamdan** yayınlıyor. Gözlemimizle uyumlu: 25.11 08:26–08:49'da hem Elazığ hem İstanbul için dolu AGF (koşu toplamları %92–98, tamsayı), TJK'nın üç yerinde boş: AGF tablosu (`AGFv2`, 08:26), günlük program sayfası (AGFORAN hücreleri `-`, 08:48), program CSV'si; eBayi'de de boş. Yani akşamki AGF **TJK/eBayi kaynaklarımızda görünmüyor**, yenibeygir başka kaynaktan alıyor (bilinmiyor).
- **Sabah 08:26 ↔ 08:49 Elazığ: 96 attan 0'ında değişim** (değerler sabit, akşam AGF'si dondurulmuş gibi). 09:00'dan sonra TJK/eBayi'nin ilk AGF'si (kısmi, 09:01–09:06) ile farkı bekleniyor.
- Takip düzeni ve amaç: `YAPILACAK_TESTLER.md` madde 23. Anlık görüntüler `veri/yenibeygir_el_kayit/<tarih>.csv` (yalnızca sayılar). **Otomatik/zamanlı çekim YOK** (kullanım şartı madde 4).

## Baş-başa karşılaştırma testi (25.11.2026, `scripts/bas_basa.py`, 14.847 koşu 2024-07+)
- Skor: atın bugünkü rakiplerini daha önce yenip yenmediği ((galibiyet−yenilgi)/(karşılaşma+1), yalnızca daha önce karşılaşılan rakipler, sızıntısız). Ortalama at başına 2,56 karşılaşmalı rakip. Fikir yenibeygir `/karsilastirma` sayfasından; **veri kullanılmadı**, kendi geçmişimizden hesaplandı.
- **Baş-başa lideri** (≥2 karşılaşmalı rakibi olan en yüksek skorlu at; 11.564 koşu) kazandı **%21,6**, piyasanın beklediği %19,1 → **A/E 1,13 (z +7,3)**. Üç dönemde de aynı: 1,12 · 1,12 · 1,15. Favori olmayan liderlerde de 1,14 (8.206 koşu). Piyasa favorisiyle aynı at olma oranı %29.
- **Ama kâr yok:** düz oyun getirisi −%18,9 (favoriye düz oyun −%27'ye göre daha iyi, yine negatif). Koşullu logit (piyasa + b·skor, b=0,5): test koşusu başına log-olabilirlik kazancı **+0,0017** (%95 [+0,0004, +0,0031]); karşılaşması çok olan koşularda +0,0042. Yani piyasanın tam fiyatlamadığı küçük ama gerçek bir sinyal.
- Sonraki adım: v9'a özellik olarak ekle (`YAPILACAK_TESTLER.md` madde 5) ve **eklenince katkıyı** 542+ koşuda ölç (v9 form/sınıf bilgisiyle örtüşebilir). Günlük rapora "baş-başa" etiketi (bilgi) eklenebilir.

## DuckDB kuruldu (25.11.2026)
- `pip install duckdb` (sürüm 2.0.1; yalnızca elle analiz için, Actions'a eklenmedi). `scripts/duckdb_ornek.py`: `at_gecmisi/*.csv.gz` üzerinde SQL ile "at sayısına göre sürpriz oranı", 17.884 koşuda **0,7 sn**; Python analizimizle birebir aynı sonuç (genel gerçek %15,2, beklenen %16,8, A/E 0,90). Yeni analizlerde (baş-başa, segment, kalibrasyon) şablon olarak kullan.

## Araçlar kuruldu ve denendi (25.11.2026)
- Kurulum (yalnızca elle analiz için, **Actions'a eklenmedi**): `pip install duckdb pandera ruff pytest shin flumine` (duckdb 2.0.1, pandera 0.36.0, ruff, pytest 9.1.1, shin 0.2.2, flumine 3.4.1). Yeni oturumda tekrar kurulması gerekir.
- **pandera** (`scripts/saglik_ilk_yayin.py`): ilk yayın AGF doluluğu kontrolü. 22.11 geçti; **23.11'de 17 koşunun 14'ü, 24.11'de 16'nın 11'i kaldı**: kısmi ilk yayın sorunu sandığımızdan yaygın (`YAPILACAK_TESTLER.md` madde 22).
- **ruff** (yalnızca sayım, dosyalara dokunulmadı; 89 betik): en sık 235 `SIM115` (dosya `with`'siz açılmış), 170 `C408`, 115 sırasız import, **70 çıplak/kör `except` (E722+BLE001)**, 37 `subprocess.run` `check`siz. Çıplak `except` hataları sessizce yutabilir (ör. kosai'deki "sessiz veri hatası" dersi); önce bunlar.
- **Shin (`mberk/shin`) kötü:** ganyandan olasılıkta kazananın log-olasılığı −1,8122; basit normalizasyon −1,7993 (fark −0,0129, güven aralığı anlamlı). En küçük olasılıklarda A/E 1,68 (aşırı düzeltiyor): Shin sabit oranlı bahis bürosu modeli, ganyan toplu havuz. **Kullanma.**
- **Güç dönüşümü** p ∝ (1/g)^k: k=1,05 (ilk %60'ta öğrenildi), son %40'ta koşu başına log-olabilirlik kazancı **+0,0016** (%95 [+0,0007, +0,0025]); %2–4 aralığında A/E 0,84→0,96, %2 altı hâlâ 0,75. Küçük ama anlamlı. Betik: `scripts/olasilik_donusumu.py`.
- **flumine** yalnızca mimari okumak için (modüller: `markets`, `streams`, `simulation`, `strategy`, `execution`...), kullanılmadı.

## TAM AGF düzeltmesi ve çıplak except temizliği (25.11.2026, kullanıcı onaylı)
- **Sorun:** `ILK_*` kısmi ilk yayını yakalıyor ve tahmin dondurma ona bağlıydı. Dondurulan AGF'li tahminlerde AGF'si %0 olan at oranı: 25.11 Elazığ ortalama %12 (bazı koşularda %30), İstanbul %1 (maks %10), 23.11 Şanlıurfa %2 (maks %17).
- **Çözüm:** `scripts/agf_tam.py` (saf fonksiyonlar). `agf_kayit.py` artık **TAM** dosyaları yazar: `TAM_<hip>.csv` ve `TAM_<hip>_ebayi.json` = altılıya giren **her** koşuda atların ≥%90'ının AGF'si dolu ilk görüntü. Altılı koşular programdaki "N. 6'LI GANYAN Bu koşudan başlar" işaretinden bulunur (2 altılı birleşir; Antalya 24.11 → 2–7). `ilk_zaman.json`'a `tjk_tam`, `ebayi_tam` anahtarları eklendi. ILK (ilk görünme saati) aynen duruyor.
- **Dondurma:** `agf_plan.py` ve `agf_sonrasi_analiz.py` tahmini TAM görüntüyle dondurur; TAM 10:15'e kadar oluşmazsa ILK ile (yedek). `gunluk.py` dondurmada TAM CSV'sini kullanır (`AGF_TAM_KULLAN=1`, yeniden indirme boş/kısmi gelebiliyor), diğer indirmelerde `?t=` ekler. Sabah kontrolü TAM iki kaynakta da alınana kadar sürer.
- **Diğer tüketiciler:** `kazanan_profil.py` `agf_sabah` için TAM'ı (yoksa ILK'i) kullanır; `surpriz_ayri.py` ve `agf_karsilastir.py` TAM'ı tercih eder.
- **Gözlem:** AGF ilk yayından ~20–25 dk sonra tamamlanıyor: TAM 23.11 Bursa 09:23, Şanlıurfa 09:28; 24.11 Adana 09:09, Antalya 09:17; 25.11 İstanbul 09:12, Elazığ 09:27. Kapanışta bütün koşular %100 dolu. TJK CSV'si bazen kısa süre boş/eski dönüyor (25.11 İstanbul 09:13 ve 09:19), tam doluluk koşulu bundan korur.
- **Etkilenen geçmiş:** 23–25.11 kayıtlarında ILK'ten türeyen `agf_sabah`, `agf_fark`, `agf_artis_sira` ve 💰/🤫 güvenilmez (TAM yok). 25.11 Elazığ/İstanbul AGF'li tahminleri kısmi AGF'yle dondurulmuş (dondurulan değiştirilmez; değerlendirmede ayrı tut). 22.11 ve öncesi etkilenmedi (ILK 09:15'te).
- **Test:** `tests/test_agf_tam.py` (9 test, `pytest`), 22–25.11 kayıtlarıyla geriye dönük doğrulama, gerçek veriyle kopyada çalıştırma, plan için 4 senaryo (ILK yalnızca → dondurma yok, TAM → var, 10:15 sonrası ILK → yedek, 10:10 → yok).
- **Çıplak except:** 34 yer `except Exception:` yapıldı (ruff E722: 0; hiçbirinde `sys.exit`/sinyal yoktu, canlı kayıt betiklerinde değildi). Dokunulmayan: 36 `BLE001` (kör except), 37 `subprocess.run` `check`siz, 235 `SIM115` (`with`'siz dosya).

## BİRLEŞİK günlük tahmin testi (25.11.2026, `scripts/tahmin_birlesik.py`)
- Kullanıcı isteği: bugünün koşularına bütün analizlerle tahmin, hem test hem takip için. Dosya: `veri/tahminler_birlesik/<tarih>.json` ve `.md`, **koşulardan önce** kaydedilir ve gönderilir (25.11: 13:18, ilk koşu 14:00).
- **Kollar** (hepsi kaydedilir, hepsi puanlanır): v9 AGF'li, v9 AGF'siz (dondurulmuş, değişmedi), piyasa (son eBayi AGF; yoksa ganyan^1,05), **BİRLEŞİK** = softmax(log piyasa + 0,5·baş-başa skoru). BİRLEŞİK yalnızca **test edilmiş bileşenleri** kullanır (AGF kapanışta kalibre, A/E ~1,0; baş-başa lideri A/E 1,13 z +7,3, logit kazancı +0,0017). Ağırlıklar bugün ayarlanmadı, tek ayarlanan b=0,5 (daha önce öğrenildi).
- Ek alanlar: dört kolun mutabakatı (kaç kol BİRLEŞİK'le aynı atı seçti), güven (net ≥%40, orta %28–40, düşük), sürpriz olasılığı (piyasaya göre kazananın AGF %10 altı attan çıkma olasılığı), sürpriz adayları. Elazığ v9 AGF'li kolunda kısmi AGF uyarısı (atların %12'sinde AGF 0).
- **Beklenti (dürüst):** BİRLEŞİK ile piyasa farkı küçük (baş-başa kazancı koşu başına +0,0017 log). Tek günde bir şey kanıtlanamaz; ≥300 koşu birikince güven aralığıyla kıyaslanacak (`YAPILACAK_TESTLER.md` madde 12 ile birlikte).

## Sürprizlerin ortak noktası, canlı kayıtlar (25.11.2026, 19–25 Kasım, 22 ganyan≥10 sürprizi)
- **Statik profilde belirgin ortak nokta YOK.** Sürprizler genel uzun at popülasyonuna (ganyan≥10, 80.827 at, 2024+) benziyor: HP sırası ≥4 %91 (popülasyon %82), jokey değişti %86 (%78), önceki koşuda 4. ve sonrası %86 (%85), iç kulvar %41 (%28), handikap %45 (%33), ortalama 11,3 at (diğer kazananlar 9,7). Hepsi n=22 ile anlamsız. Geçmişte de bu özelliklerin A/E'si 0,89–0,98 (uzun atlar genel A/E 0,90): "sürprizlere özgü" statik işaret bulunmadı.
- **Modeller göremiyor:** AGF'li model sürprizlerin %9'unu (2/22), AGF'siz %5'ini (1/22) ilk 3'e koymuş.
- **"Diğer kazananlarla" kıyas yanıltıcı:** sürprizleri favorilerden oluşan kazananlarla kıyaslamak (örn. 💰 %10'a %41) yanlış sonuç verir; doğru karşılaştırma uzun at popülasyonuyla.
- **Canlı işaretler (`para_takip.csv`, 85 koşu, 867 at, piyasa beklentisine karşı):** **🤫 sessiz AGF + ganyan≥10: 71 at, 8 kazandı, beklenen 3,1 → A/E 2,62 (z +2,9), getiri +%63**; sessiz olmayan uzun atlar 11/13,3 (A/E 0,83, −%47). 💰 para girişi: ganyan≥10'da A/E 1,21 (z +0,3), anlamsız. ⭐ sinyal: 14 at, 0 kazanan (beklenen 1,0).
- **🤫 için uyarılar:** (1) 3 kazanan 24.11'de (6 attan 3), kümelenme; (2) 23–25.11'de sabah AGF kısmi ilk yayındı (TAM yok), o günlerin 🤫'sı güvenilmez; (3) birden çok işaret ve alt küme denendi (çoklu test); (4) 8 kazanan çok az. **İlk umut verici işaret, kanıt değil.** `YAPILACAK_TESTLER.md` madde 11'de TAM'lı temiz AGF ve ≥150 uzun atla yeniden test.


## YAPILACAK_TESTLER çalıştırıldı (25.11.2026 akşam)
Kısa sonuçlar; örnek küçük olanlar "olası" diye okunmalı.
- **#1 hata raporu (✅ kuruldu):** `scripts/hata_raporu.py`, çıktı `veri/hata_raporu/<tarih>.md`; gün sonu `agf_plan.py` `surpriz_ayri.py`'den sonra çağırır. İçerik: günlük özet tablosu, günün sürprizleri (segment beklentisiyle kıyas, kural tabanlı "olası" notlar), büyük hatalar. 25.11: 13 koşuda sürpriz 2 (beklenen 1,9); kazananın model sırası ≥4: 7/12 (Elazığ 1–4, İstanbul 2/4/8). 19–25.11 toplam: ilk seçim doğru AGF'li 27/106 (%25), AGF'siz 33/106 (%31), AGF favorisi 27/106 (%25); ganyan≥10 sürpriz 22/107 (%21, taban ~%16). Örnek küçük, fark anlamlı sayılmaz.
- **#2 sürpriz tanımları (✅ sayım, canlı sisteme dokunulmadı):** 107 koşuda ganyan≥10: 22, kapanış AGF<%10: 35, AGF<%5: 14, sabah AGF<%10: 41. Ganyan≥10 olanların **hepsi** AGF<%10'un içinde (22/22); AGF<%10 ek 13 koşu getiriyor. Kazanan atın "jokey değişti" oranı sürprizlerde %82 (G), %80 (A10), tüm koşularda %63: fark var ama taban zaten yüksek, ayırt edici sayılmaz. Sabah AGF<%10 (41), kapanıştan (35) fazla: sabah kısmi AGF'ye (TAM öncesi) güven yok. `kazanan_profil.py` DEĞİŞTİRİLMEDİ (kullanıcı "Kalsın" dedi).
- **#3 SHAP (✅ düzeltilmiş, `scripts/shap_surpriz.py`):** yaş sütunu `<yaş>y <renk> <cinsiyet>`: 3. harf cinsiyet (e genç erkek, a aygır, d genç dişi, k kısrak, g iğdiş; yaşla doğrulandı), 2. harf renk. İlk taslakta 2. harf cinsiyet sayılmıştı, **o "cinsiyet" etkisi yanlıştı (renk/ırk vekili)**. LightGBM piyasasız model (143 bin at, 14,8 bin koşu, ilk %60 eğitim): test 5.713 koşuda kazananın ort. log-olasılığı model −1,876, piyasa −1,835 (piyasa daha iyi, beklenen). Model 1. sıraya %32,4, ilk 3'e %62,7. Test sürpriz kazananları (865, ganyan≥10): model sırası ort. 6,4 (tüm kazananlar 3,4). SHAP: hp_fark +0,266 (%80 pozitif; tüm uzun atlarda +0,173), jokey_oran −0,116, hp_sira −0,090, bas_basa −0,042, cinsiyet ≈0. Okuma: sürpriz kazananlarda model "HP ortalamadan yüksek" diye hafifçe yukarı itmiş, jokey/HP sırası aşağı; özellikler tek başına sürprizi öngörmüyor. Neden-sonuç değil, model açıklaması.
- **#4 v9 kalibrasyonu (✅ elle çalıştırıldı, betik kaydedilmedi):** AGF'li v9 üstte aşırı güvenli, AGF'siz daha iyi kalibre; canlı örnek az (106 koşu), karar için yeterli değil.
- **#5 özellik ekleme (✅ `scripts/ozellik_ekleme_testi.py`, 14.847 koşu, test 5.713):** piyasaya eklenince koşu başına log kazancı, %95 aralık: tabela −0,00056 [−0,0027, +0,0018]; uzmanlık +0,0012 [−0,0015, +0,0038]; baş_başa +0,0018 [−0,0005, +0,0042]; aynı_jokey, kilo_fark, orta_kilo b=0 (katkı yok). **Hiçbiri anlamlı değil** (hepsinin aralığı sıfırı kapsıyor); baş_başa en umutlusu ama bu ölçütte kanıtlanmadı (önceki lider A/E testi z +7,3 ayrı ölçüt).
- **#6 altılı ikramiye (✅ fizibilite, `scripts/altili_ikramiye.py`):** 2.003 altılı (2024+). Ödeme ile altı ayak kazanan ganyanlarının çarpımı r = 0,93 (iki yarıda 0,932 / 0,939). Sürpriz ayak sayısı 0/1/2/3/4+ için ortanca ödeme 4.799 / 31.573 / 148.162 / 956.270 / 3.769.145 TL. **Devir/havuz verisi sonuç CSV'lerinde yok**, devirde beklenen getiri farkı bu veriyle test edilemez (havuz büyüklüğü ayrı toplanmalı).
- **#15 veri sağlık (✅ `tests/test_veri_saglik.py`):** eBayi JSON biçimi (koşuda 3–20 at, ganyan 1–1000), TAM kayıtlarda AGF toplamı %85–101, TAM TJK altılı tespiti; 53 test geçti. Biçim bozulursa pytest hemen kırılır.
- **#16 ganyan 999.99 (✅):** `kazanan_profil.csv` ve `para_takip.csv`'de ≥500 değer yok. 999.99 yalnızca ham `*_ganyan.json` görüntülerinde (117 dosya) ve dondurulmuş tahmin dosyalarının bilgi amaçlı `ganyan` alanında (1031 attan 706'sı, havuz erken açılmamış): v9 olasılıklarına girmiyor, yalnızca `analiz3` ekranında "piyasa oturmamış" uyarısını tetikliyor. Değişiklik gerekmedi.
- **#17 dondurma saati (✅ doğrulandı):** her dondurulmuş tahminin git ilk-ekleme saati ile hipodromun ilk koşu saati karşılaştırıldı: 21.11 ve sonrasında 18/18 dosya çifti ilk koşudan ÖNCE (09:11–12:15). **19.11 İzmir ve 20.11 Antalya** ilk koşudan sonra eklenmiş (16:50, ilk kurulum günleri): bu iki hipodromun 19–20.11 koşuları geçerli test sayılmamalı (en çok 29 koşu).
- **#23 yenibeygir karşılaştırma (✅):** 25.11 08:49 görüntüsü Elazığ 08:26 ile aynı (0/96 değişim); bizim TAM'la ayrıntılı kıyas yarın/ilerleyen günlerde, yalnızca elle kayıt.
- **#24 pytest (✅):** `tests/test_agf_tam.py` (9) + `tests/test_veri_saglik.py`: toplam 53 geçti.
- Beklemede (veri biriksin): #7 (≥500 koşu −60 dk), #9 (≥7 düzeltmeli gün), #10 (≥10 gün ilk_zaman), #11/#11a, #12 (≥300 koşu; şimdi 106), #13 (≥100 ayrışan koşu), #14 (~1 ay). #8 yapılamaz (2022–23 verisi yok). #22 (TAM geriye dönük) ve #25 (BİRLEŞİK puanlama) sonra.
- **#25 BİRLEŞİK puanlama betiği (✅ hazır, `scripts/birlesik_puan.py <tarih>`):** ilk ara sonuç 25.11, 13 koşu bitmişken: 1. seçim kazandı birleşik 3, v9 AGF'li 4, v9 AGF'siz 2, piyasa 3; kazananın ort. log-olasılığı −2,241 / −2,809 / −2,050 / −2,232. Örnek çok küçük, anlam çıkarılmaz; Elazığ bitince (≈21:45) yinelenir. Elazığ'ın v9 AGF'li kolu kısmi AGF'liydi (⚠).

## yenibeygir "Blt" (Bülten Ortalama Puanı) ve ikramiye takibi (25.11.2026 akşam)
- **Blt nedir:** yenibeygir'in yarın bülteninde (`/26-11-2026/<hipodrom>`; `2026-11-26` biçimi 404) AGF sütununun yerinde "Blt" var; sütun başlığının ipucu (title) "Bülten Ortalama Puanı". Kullanıcı ekran görüntüsüyle gösterdi. Anlamı sayfada başka açıklanmıyor; kaynağı bilinmiyor. Koşu başına toplamı 92–98 (yüzdeye benziyor). Bugünün sayfasında aynı sütun AGF.
- **Veri alma dersi:** özetleyici model üzerinden okuma (WebFetch) Blt değerlerini yanlış verdi (1. koşu için 4–6. atlarda uydurma sayılar, toplamlar 754 gibi). Doğrusu ham HTML'den ayrıştırmak: `<th title="Bülten Ortalama Puanı">Blt</th>`, satırın ilk `<td><span>` değeri. Elle tek istek (`curl`), ayrıştırma `scripts/yenibeygir_blt_kayit.py <html> <tarih> <hipodrom>` (ağa çıkmaz).
- **İlk kayıt:** 26.11 İzmir, 69 at, 7 koşu (`veri/yenibeygir_el_kayit/blt_2026-11-26.csv`, sütunlar: zaman_tr, tarih, hipodrom, kosu, ikramiye_tl, at_no, at_adi, blt). 1. koşu ekran görüntüsüyle birebir aynı (20, 34, 31, 9, 2, 1). Sayfa ikramiyeyi de veriyor (1. koşu 305.000 TL … 5. koşu 695.000 TL).
- **Test planı (veri birikince):** Blt'yi sabah gerçek AGF ile karşılaştır (aynı mı, farklı mı); Blt'nin en yükseği kazanıyor mu (A/E); piyasaya koşullu logit ile ek bilgi var mı. Tarihsel Blt yok, en az birkaç yüz koşu gerekir. Otomatik çekim YOK (site şartları); elle, seyrek.
- **İkramiye analizi (✅ `scripts/ikramiye_analiz.py`, 10.018 koşu, 2024+, kaynak sonuç CSV 1. ödülü):** ikramiye çeyrekleri (150–390 bin / 390–490 / 490–600 / 600 bin+): ganyan favorisi kazandı %33,7 / 35,1 / 33,4 / 37,0; sürpriz (ganyan≥10) %17,3 / 16,7 / 15,8 / 13,3; ort. at sayısı 10,3 / 10,4 / 10,0 / 9,1. Yüksek ikramiyede sürpriz az, ama at sayısı da az. At sayısı 9–11'e sabitlenince fark kayboluyor (düşük %14,6, yüksek %15,4 sürpriz; favori %32,8 / 34,7, aralıklar örtüşüyor). Yani ikramiye büyük ölçüde at sayısı ve sınıfın vekili; ek bilgi görülmedi. İki yarıda yön aynı.
- **Sonraki adım (ikramiye takibi):** canlı kayıtlara (`kazanan_profil`) ikramiye sütunu eklemek canlı sistem değişikliği; kullanıcı onayı bekler. Bugünlük ikramiye zaten sayfadan ve sonuç CSV'sinden alınabiliyor.
- **Blt–resmi AGF karşılaştırması (hazır):** `scripts/blt_agf_karsilastir.py <tarih> <hipodrom>`: koşu başına ort. mutlak fark, Spearman, en yüksek aynı mı. Deneme (25.11 Elazığ eBayi AGF'sinden üretilen sahte Blt ile) çalıştı. Gerçek karşılaştırma 26.11 sabah ~09:40 (zamanlı hatırlatma kuruldu): gece Blt kaydı ile TAM AGF.

## Web taraması: akademik fikirler (25.11.2026, yalnızca fikir; arama özetleri, tam makaleler okunmadı)
- **Son dakika parası bilgi taşır:** JRA (Japonya, 2004–2023) çalışması: son 5 dakikada oranı düşen atlar aynı kapanış oranlı diğerlerinden fazla kazandırıyor; kapanış oranı tek başına yetersiz (arxiv 2509.14645). Diğer çalışmalar (ABD, Avustralya) son dakika parasını "akıllı para" bulur. Bizim için: −10/−5 dk ganyan hareketi toplamak (B grubu #7) doğru yön; şu an −60/−30/−10 var, son 5 dk görüntüsü eklenebilir.
- **Benter (1994) / Bolton-Chapman (1986):** temel model ile piyasa olasılığını koşullu logitle birleştirmek; iki aşamalı yöntem (önce temel model, sonra piyasa ile birleştir) tek aşamalıdan daha iyi (Sung-Johnson 2007, özet). Bizim BİRLEŞİK modelimiz aynı fikir. Bar yüksek: model piyasa kadar kapsamlı olmalı.
- **Favori–uzun at yanlılığı:** Snowberg-Wolfers (NBER w15923): egzotik bahisler (ikili/sıralı) hangi açıklamanın doğru olduğunu ayırt eder; Green-Lee-Rothschild: yanlılığın büyüklüğü hipodromdan hipodroma değişir. Bizim hipodrom bazlı A/E bulgularıyla uyumlu (İzmir, Antalya).
- Türkçe istatistik: web aramasında kullanılabilir akademik/istatistik kaynak çıkmadı (yalnızca canlı oran sayfaları).

## "Hepsini yap" sonuçları: web taraması fikirleri (25.11.2026)
- **Son 5 dk görüntüsü: zaten var.** `agf_plan.py` her koşu için −60, −30, −10 ve −3 dk görüntü alıyor. `para_takip.csv`'de son görüntü 872/≈1.000 satırda −3 dk (diğerleri −2, −4, −9; geç kalan yüzde birkaç). Canlı sisteme dokunmaya gerek yok; JRA çalışmasındaki "son 5 dk" penceresi −3 dk görüntüsüyle karşılanıyor. Test (#7) ≥500 koşuyla yapılacak.
- **Egzotik (ikili / sıralı ikili) testi: daha önce yapılmış** (`scripts/harville_test.py` 2.446 koşu; `scripts/ikili_test.py` 9.068 koşu, gerçek TJK ödemeleri). Sonuç: Harville ilk ikiye girmeyi %0–70'te 1–3 puan içinde tutturuyor, çok güçlü favorilerde abartıyor (%84 tahmin → %76 gerçek); ikili 1 TL getirisi %77–92, sıralı ikili %78–89, değer eşikleri (model>1,3× piyasa) getiriyi pozitife çevirmiyor (n küçülünce 134% görülen tek hücre 81 bahis, anlamsız). Yani egzotiklerde de kesinti aşılmıyor.
- **Hipodrom bazlı kalibrasyon yenilendi** (`scripts/surpriz_nerede.py`, ganyan≥10 oranı gerçek/beklenen, ilk yarı → ikinci yarı): İzmir 0,92 → **0,74 (z −4,4)**, Antalya 0,81 → 0,73 (iki yarıda da z ≈ −2,4), Adana 0,95 → 0,82 (z −2,6), Bursa 0,87 → 0,88, İstanbul 0,92 → 0,91, Elazığ 1,03 → 1,00, Kocaeli 0,85 → 1,01, Ankara 1,04 → 0,94, Şanlıurfa 0,94 → 0,94. İzmir ve Antalya'da uzun atlar iki yarıda da fazla fiyatlanıyor (daha az kazanıyor); kalıcı görünüyor ama bir kısmı çoklu karşılaştırma olabilir. 1 ay sonra canlı verilerle yinele.

## Blt–AGF karşılaştırması ve TAM kontrolü (26.11.2026 sabah, İzmir; zamanlı iş)
- **TAM çalıştı:** İzmir TAM eBayi 09:06 TR, TJK 09:10; Antalya 09:10 / 09:15 (`ilk_zaman.json`). v9 tahminleri TAM ile donduruldu (İzmir 09:12, Antalya 09:16 TR), her ikisinde AGF=0 at oranı 0,000 (dün Elazığ/İstanbul'da kısmi AGF vardı). Düzeltme işe yaradı.
- **TAM anında AGF henüz oturmamış:** 09:42'de yenibeygir AGF'sini (tamsayı) eBayi görüntüleriyle karşılaştırdım: 06:06 UTC (TAM anı) görüntüsünden ort. mutlak fark 5,5 puan (en çok 38,7), 06:10'da 1,8, 06:15'te 1,05, 06:23'te 0,29, 06:38'de 0,32 (yuvarlama düzeyi). Yani dondurma anı (06:12 UTC, fark ≈1,8–5 puan) AGF'nin yerleşmesinden ~10–15 dk önce. İzmir'in dondurulmuş girdisi kapanış AGF'sine göre ortalama birkaç puan oynak. Karar kullanıcıya bırakıldı: dondurmayı TAM'dan ~15 dk sonraya ertelemek (canlı sistem değişikliği, yapılmadı).
- **yenibeygir sütunu:** gece 'Blt' idi; sabah 09:42'de altılı koşularda (2–7) sütun 'AGF'ye döndü, **1. koşuda (altılı dışı) 'Blt' olarak kaldı** ve gece değerleriyle birebir aynı (statik). yenibeygir'in sabah AGF'si resmi eBayi AGF'siyle aynı (fark 0,3, yuvarlama): yenibeygir AGF'si resmi kaynağın kopyası, ek bilgi yok.
- **Blt AGF'nin önceden yazılmış hali değil:** altılı koşularda gece Blt ile resmi AGF ort. mutlak fark 5,0–8,7 puan (Spearman 0,63–1,00), en yüksek aynı at 3/6 koşuda; altılı dışı 1. koşuda Blt–AGF farkı 16,2 puan. Blt bülten ortalamasıdır, AGF'den bağımsız ama ilişkili bir sinyal. Test için günlük gece Blt kaydı + sonuç gerekli (örnek 1 gün, 7 koşu: sonuç yok henüz).
- Kayıt: `veri/yenibeygir_el_kayit/blt_2026-11-26.csv` (gece 21:29 Blt, sabah 09:42 AGF/Blt). Karşılaştırma dosyası `veri/yenibeygir_el_kayit/blt_agf_2026-11-26_İzmir_AGF.md`.

## Dondurma TAM'dan 15 dk sonraya ertelendi; TAM geriye dönük türetildi (26.11.2026, kullanıcı onaylı)
- **Neden:** 26.11 ölçümü: TAM anındaki AGF kapanışa göre ort. 1,8–5,5 puan oynak, 15–20 dk sonra yerleşiyor (0,3). Sorun iki katmandı: (1) dondurma TAM'dan hemen sonra yapılıyordu; (2) `gunluk.py` AGF'yi TAM dosyasından (TAM anındaki içerik) okuyordu, yani yalnızca beklemek yetmezdi.
- **Değişiklik:** `agf_tam.py`: `olgun(kd,hip,simdi_utc)` (iki kaynaktan geç TAM saati + 15 dk; saat yoksa beklemez) ve `en_son_tam_csv(kd,hip)` (en son DOLU TJK görüntüsü; kısmi/titreyen görüntüler `tam_tjk` ile elenir). `agf_sonrasi_analiz.py` ve `agf_plan.py` (`agf_hazir`): bugünün TAM'ı ancak olgunsa dondurulur (geçmiş gün ve ILK yedeği 10:15 aynı). `gunluk.py` (dondurma modu, `AGF_TAM_KULLAN=1`): en son dolu görüntüyü kullanır, yoksa TAM dosyası. Yedek mantığı aynı: TAM oluşmazsa 10:15'te ILK.
- **Testler:** `tests/test_agf_tam.py` 13 test (olgun saatleri, saat yoksa beklememe, en son dolu görüntü seçimi, kısmi görüntüyü atlama); toplam 61 pytest geçti. `agf_sonrasi_analiz.py` bugün çalıştırıldı (hepsi dondurulmuş), hata yok. Gerçek sınav yarın sabah: dondurma ~TAM+15 dk (≈09:25–09:35 TR) olmalı.
- **#22 geriye dönük TAM (`scripts/tam_geriye_donuk.py`, yalnızca ekler):** `veri/agf_kayit/<tarih>/retro_TAM.json` + `retro_TAM_<hip>.csv` (22, 23, 24 Kasım). İlk yayın doluluğu ve TAM gecikmesi: 23.11 Bursa ilk %45 dolu, TJK TAM 06:23 UTC (ilk yayından +17 dk); Şanlıurfa %36, TAM 06:28 (+22); 24.11 Adana %70, TAM 06:09 (+4); Antalya %54, TAM 06:17 (+12). 22.11: ilk görüntü zaten %100 dolu (ilk kayıt 09:15 TR'ydi, ilk yayın kaçmıştı). TAM, ilk yayından 4–22 dk sonra oluşuyor; ilk yayın kısmiliği 23–24'te gerçek.
- Kalan (isteğe bağlı): `kazanan_profil` sabah AGF/hareket alanlarını bu `retro_TAM` görüntüsüyle yeniden hesaplamak (ayrı dosyaya).

## Son dakika piyasa özeti (26.11.2026, kullanıcı onaylı canlı sistem eklemesi)
- `scripts/son_dakika_ozet.py <tarih> <hip> <koşu>`: koşudan ~10 dk önce (−10 dk görüntüsünden sonra) `agf_plan.py` çağırır; çıktı `veri/son_dakika/<tarih>/<hip>_<koşu>.md`. At başına: piyasa % (AGF, yoksa ganyan), sabah AGF (TAM+15 dk sonraki oturmuş görüntü), ganyan −60 dk → şimdi, v9 AGF'li / AGF'siz / BİRLEŞİK (varsa) olasılık, işaretler (💰 ganyan −60 dk'ya göre ≥%30 düştü; 📈/📉 AGF sabaha göre ±%30 ve ±3 puan; ⚖ bizim olasılık piyasanın ≥1,3 katı). Altında: bizim kollar ve piyasa favorisi aynı mı, para girişi olan atlar. **İşaretler yalnızca bilgi, test edilmedi.**
- Sınav: bugünkü verilerle elle çalıştı (İzmir 1/5, Antalya 3); plan deneme modunda (PLAN_DENEME) 14:52'de İzmir 1. koşu için −10 dk kaydı ve özeti sırayla çalıştırdı, ikinci turda tekrarlamadı. Gerçek sınav bu akşam İzmir 15:00 öncesi.
- Not: `.github/workflows/kayit.yml` commit listesine `veri/son_dakika` ve `veri/hata_raporu` eklendi (hata raporu şimdiye kadar Actions tarafından commit'lenmiyordu; gün sonu raporunu yalnızca elle ben push'luyordum).

## −10 dk tahmini: tüm koşular, tutturma yüzdesi (26.11.2026, kullanıcı isteği)
- **Ne:** Her koşudan ~10 dk önce (`agf_plan.py`, −10 dk görüntüsünden hemen sonra) `scripts/tahmin_10dk.py` tahmin üretip `veri/tahminler_10dk/<tarih>.json` içine EKLER (bir koşu bir kez, üzerine yazılmaz; `.md` özeti yanında). Kol: **BİRLEŞİK_10** = −10 dk piyasa (AGF; AGF yoksa ganyan^1,05) + 0,5 × baş-başa skoru; karşılaştırma için aynı kayıtta piyasa_10 (yalnızca piyasa) ve sabah dondurulmuş v9 AGF'li / AGF'siz olasılıkları. Seçim: ilk 1 ve ilk 3 at, güven (net/orta/düşük).
- **Puanlama:** `scripts/puan_10dk.py` (gün sonu otomatik, `agf_plan.py` doğruluk raporunda) → `veri/tahminler_10dk/SONUC.md`: 1. seçim kazandı %, kazanan ilk 2'de/ilk 3'te %, kazananın ort. log-olasılığı, Wilson %95 aralığı; ≥100 koşuda BİRLEŞİK_10 − piyasa_10 eşli bootstrap. Yalnızca eBayi görüntüsü koşuya ≤20 dk kala alınmış tahminler "geçerli" (bayat sayılan ayrıca raporlanır); sonucu gelmeyenler ayrı sayılır.
- **Beklenti (dürüst):** piyasa favorisi tarihsel olarak koşuların ~%33–35'ini kazanır; BİRLEŞİK_10 piyasayla neredeyse aynı seçecek (baş-başa katkısı küçük). Yani "tutturma yüzdesi" ~%30–35 olması normal; rastgele ~%10. İlk 3'te bulma ~%65–70. Anlamlı fark için ≥300 koşu gerekir.
- **Sınav:** 25.11 Elazığ 9 koşuyla (yalnızca mekanik testi; görüntü saati bayat olduğundan sahte işaretlendi, gerçek tahmin değil): çalışıyor. Gerçek ilk veri bu akşam. `agf_plan.py` dene modunda 14:52'de İzmir 1. koşu için sırayla −10 dk kaydı, son dakika özeti, tahmin_10dk çalıştı. `.github/workflows/kayit.yml` commit listesine `veri/tahminler_10dk` eklendi.

## Koşu çeşidi bazlı kayıt ve değerlendirme (26.11.2026, kullanıcı isteği)
- **Çeşitler (2024+ geçmişte 33 farklı ham tür, 7 aile):** Maiden (+Şartlı 19/27 kazanmamışlar), Şartlı 1–5, Handikap 13–24, KV-6…9 (kısa vade), Satış 1–4, Grup 1–3, Amatör/Kadın binici; ırk (Arap/İngiliz), yaş grubu, mesafe bandı, pist ayrı boyutlar. Adlandırma `veri/kosu_turu_analiz.json` ile aynı (`scripts/kosu_tipi.py`: `tur`, `aile`, `sinif`).
- **Kayıt:** `veri/kosu_tipi_kayit.csv` (gün sonu yeniden üretilir; 19.11'den beri 112 koşu): koşu başına çeşit, mesafe/pist, kazanan, ganyan, sürpriz, favori kazandı mı, v9 AGF'li / AGF'siz / BİRLEŞİK_10 / piyasa_10 ilk seçimi tuttu mu. `tahmin_10dk` kayıtlarına çeşit eklendi, `puan_10dk` `veri/tahminler_10dk/kosu_sonuclari.csv` yazıyor.
- **Rapor:** `veri/kosu_tipi_rapor.md` (aile×ırk, ayrıntılı tür×ırk n≥3, mesafe bandı): tarihsel taban (koşu sayısı, ort. at, favori %, sürpriz %) yanında canlı sicilimiz. İlk bakış: n küçük (aile başına 2–24), anlam çıkarılmaz.
- **Kullanım:** `son_dakika_ozet.py` her koşunun özetine "Koşu çeşidi" bölümü ekliyor: tarihsel taban oranlar + o çeşitteki canlı sicilimiz ("aynı çeşit koşu geldiğinde tahmini bu verilerle birlikte değerlendir").
- **Gün sonu:** `agf_plan.py` doğruluk raporuna `kosu_tipi_kayit.py` ve `kosu_tipi_rapor.py` eklendi; `kayit.yml` commit listesine `veri/kosu_tipi_kayit.csv`, `veri/kosu_tipi_rapor.md`. Çeşit bazlı "hangi kolu tercih edelim" kararı için çeşit başına ≥30 koşu gerekir (en kalabalık çeşitlerde aile başına ~2–4 hafta).

## Sürpriz riskli koşularda daha uzun liste (26.11.2026, kullanıcı isteği)
- **Risk ölçüsü:** piyasada (AGF, yoksa ganyan) %10 altı atların toplam payı. 17.873 geçmiş koşuda (2024+, kapanış ganyanı) terzil eşikleri: ≤0,198 düşük, ≤0,31 orta, üstü yüksek. Yüksek riskli koşularda ort. 12,2 at ve ganyan≥10 sürpriz oranı %23 (düşük riskte 7,2 at, %8).
- **Geçmişte kazananın piyasa sırasına göre ilk K'da olma oranı:** düşük risk K3 %77 (K5 %94); orta K4 %81 (K3 %71); **yüksek K5 %76, K3 yalnızca %60** (K6 %82). İki yarıda tutarlı (yüksek riskte K5 %76 / %76). Kural: **yüksek risk 5 at, orta 4, düşük 3**; böylece her risk grubunda kazananı listeye alma ~%76–81 olur.
- **Uygulama:** `tahmin_10dk.py` kayda `surpriz_riski`, `surpriz_p`, `liste_uzunlugu`, `secim_liste` ekliyor (liste BİRLEŞİK_10 sırasıyla); `puan_10dk.py` "kazanan listede %" ve risk grubu başına tabloyu `SONUC.md`'ye yazıyor; `son_dakika_ozet.py` her özete "Sürpriz riski → liste" satırı ekliyor.
- **Dikkat:** liste uzadıkça isabet artar ama bahis maliyeti de artar (5 atlı ganyan kuponu = 5 bahis); getiri hesabı ayrı. Ayrıca bu "kazanan listede" oranı, piyasa sırasıyla aynı yaklaşık değerlerde; BİRLEŞİK_10'un liste seçimini piyasadan iyi yapıp yapmadığı ≥300 koşuda ölçülecek.

## Tavily denemesi ve AGF geçmişi arayışı (26.11.2026)
- **Tavily:** API anahtarı güvenli formla ortam gizli anahtarı olarak `api.tavily.com` için eklendi (`curl -X POST https://api.tavily.com/search`; proxy anahtarı enjekte ediyor). Arama çalışıyor (200, ~1,3 sn); alakasız sonuç oranı yüksek (ör. "AGF" adlı şirket sayfaları), `include_domains` ile siteye daraltmak işe yarıyor. Bu oturumda 8 arama yapıldı (kota bilinmiyor).
- **AGF geçmişi bulundu: agftablosu.com.** Tarih bazlı arşiv sayfaları `https://www.agftablosu.com/agf-tablosu/YYYY-MM-DD` (Tavily dizininde 2023-01-31, 2025-02-11, 2025-09-13, 2025-09-25, 2026-01-19, 2026-07-16, 2026-11-24 görüldü): altılı/ayak başına at no ve AGF %. Ayrıca sonuç ve bülten sayfaları (2025+). Doğrudan erişimimiz bu siteden 403 almıştı (bot engeli), kullanım şartları OKUNMADI.
- **Arşivdeki AGF kapanış AGF'si değil:** 24.11 Adana 1. ayak: arşiv 4 (%31,51), 2 (%16,44), 1 (%13,95), 12 (%12,50); bizim kayıtlarımızda en yakın görüntü ≈ 08:09–08:24 UTC (≈11:10 TR), ort. mutlak fark 0,7–1,0 puan; kapanışta (11:20 UTC sonrası) 4 %43,6, 12 ise %4,3'tü. Yani arşiv gün içi bir anlık görüntüyü tutuyor (saati sayfalarda belirtilmiyor, sayfadan sayfaya değişebilir; tek örnek). AGF gün içinde çok oynuyor (12 numara %12,5 → %4,3).
- **Kullanım kararı:** toplu çekim yok (şartlar okunmadı, sunucu bot engeli var). Seçenekler: şartları oku/site sahibinden izin iste; tek tek sayfalara elle bakmak. Arşiv değeri: geçmişe dönük gün-içi AGF; sınırı: kapanış değil, zaman damgası belirsiz.
- **DÜZELTME (26.11, kullanıcı ekran görüntüleriyle, 22.11 İzmir):** agftablosu arşivi gün içi anlık görüntü DEĞİL, **kapanış (resmî nihai) AGF'yi** tutuyor. Önceki sonuç (24.11 Adana'nın öğle görüntüsüne benzemesi) yanlıştı: o değerler Tavily'nin sayfayı taradığı andaki (gün içi, sayfa 5 dk'da bir güncelleniyor) içerikti, arşivin kendisi değil. 22.11 İzmir 1. ve 2. altılının 1.–2. ayakları (ekran görüntüsü, kazananlar yeşil, koşmaz üstü çizili) bizim kayıtlarımızla karşılaştırıldı: kapanışa yakın görüntülerimizle fark 0,0 (ayak başına ort. mutlak, 12:50 UTC sonrası tüm ayaklarda 0,0; ilk ayaklarda 11:51 UTC'den itibaren). Altılı eşleme (altılı 1: koşu 1–6, altılı 2: koşu 3–8) doğrulandı. Sonuç: arşiv **geçmiş kapanış AGF'si** veriyor (2023-01-31'e kadar sayfa görüldü, Tavily dizininde). Çok değerli ama toplu erişim izinsiz olamaz; elle ekran görüntüsü ölçeklenmez. Site şartları okunmadı; izin için site sahibine yazmak en temiz yol.
- **DÜZELTME 2 (26.11): AGF geçmişi zaten bizde.** `veri/at_gecmisi` (2024-01'den beri) `agf` sütunu atların %63–78'inde dolu (altılıya giren koşular; aylık: 2024-05 %64, 2025-02 %78, 2026-11 %70): kapanış AGF'si. "AGF yalnızca 19.11'den beri" ifadem yalnızca **koşu öncesi AGF hareketi** (−60/−30/−10/−3 dk görüntüleri) için doğru; kapanış AGF geçmişi 2024'e kadar var. agftablosu'na ihtiyaç yok.
- **Resmî kaynak daha geriye gidiyor:** TJK'nın kendi geçmiş program ve sonuç CSV'leri (`medya-cdn.tjk.org/raporftp/TJKPDF/<yıl>/<tarih>/CSV/GunlukYarisProgrami|GunlukYarisSonuclari/<GG.AA.YYYY>-<Hipodrom>-...-TR.csv`; zaten kullandığımız host) geçmiş günlerde de AGF değerlerini koruyor. Doğrulama: 22.11.2026 İzmir koşu 1–2 AGF'si (3 %28,00; 4 %18,64; 1 %14,90 / 4 %39,05; 3 %25,15; 5 %14,01) agftablosu arşivi ve kendi kapanış kaydımızla birebir aynı. Erişilebilen geçmiş tarihler (tek istek denemeleri): 2022-06-15 İstanbul, 2023-01-31 Adana, 2025-09-13 İzmir/Ankara (program ve sonuç CSV'si 200); 2022-01-12, 2021-04-28, 2023-09-10 Ankara için 404 (o gün yarış olmayabilir; yaklaşım kesin değil). Sonuç: 2022 ortasından 2023 sonuna kadar yaklaşık 1.5 yıllık ek geçmiş (AGF dahil) indirilebilir görünüyor; çok istek gerektirir (yaklaşık 6–8 bin dosya, 2 sn arayla ~4 saat), YAPILMADI, kullanıcı onayı bekleniyor. Bu, YAPILACAK #8'i ("2022–23 verisi yok") geçersiz kılar: veri TJK'da var, bizde yok.
- **Diğer aranan siteler:** agftahmin.com (agftablosu ile aynı şablon, 2021'e kadar sayfa görüldü) aynı Cloudflare doğrulamasına sahip (403, atlanmadı); pegadrom.com sonuç sayfalarında AGF verisi YOK (yalnızca ganyan; açıklamada AGF geçse de tablo yok); altiliganyan.com, sonduzluk.com, atyarisi.com yalnızca güncel AGF gösteriyor görünüyor.
- **DÜZELTME 3 (26.11, kullanıcı kontrol ettirdi): 2020–2021 verisi zaten indirilmişti.** `veri/arsiv/ebayi` (ebayi sonuç JSON.gz): 2020-01-01 → 2021-10-05 (kısmi; 83 yarışsız gün `.yok`; 2020-04/05 koşu yok, Mart–Haziran 2020 pandemi) + 2024-01-01 → 2026-11-18. **Boşluk: 2021-10-06 → 2023-12-31** (indirme 21.11 09:30'da kesildi; `.gunluk/ebayi_indir_eski.log` son satır 20211004; konteyner kapanmış olabilir). `veri/at_gecmisi` 2020 (284 gün) ve 2021-01-01 → 2021-06-08 (159 gün) + 2024+ ; ebayi arşivindeki 2021-06-09 → 2021-10-05 günleri henüz at_gecmisi'ne işlenmedi (`at_gecmisi.py kur` ile yeniden kurulacak). AGF doluluğu 2020–2021'de %61–88 (altılıya giren koşular), ganyan %100. Kalan indirme komutu: `python3 scripts/ebayi_indir.py veri/arsiv/ebayi 2021-10-06 2023-12-31` (1 sn arayla, var olanı atlar, ~820 gün × ~3 istek ≈ 45–60 dk). TJK CSV yolu (önceki madde) gerekmez, ebayi aynı veriyi veriyor. #8 yeniden ele alınabilir.

## İlk canlı −10 dk tahmini ve özet (26.11.2026, İzmir 1. koşu 15:00)
- **Çalıştı:** 14:52'de otomatik: eBayi görüntüsü koşuya 9 dk kala, risk düşük, BİRLEŞİK_10 listesi: BAŞ YARGIÇ, KÜÇÜK HASO, HIRÇIN DADAŞ (ilk seçim Baş Yargıç). **Sonuç:** 1. KÜÇÜK HASO, 2. BAŞ YARGIÇ, 3. HIRÇIN DADAŞ. İlk seçim 2. oldu, kazanan listemizin 2. sırasındaydı (3 atlık listede, ilk 3 doğru sırasız). Özette 💰 işareti tam olarak kazanan ata düştü (ganyan 6,2 → 2,9 son saatte). Tek koşu, anekdot; ≥300 koşuda ölçülecek.
- **Hata bulundu ve düzeltildi:** son dakika özeti 14:52'de "Sürpriz riski → liste" satırında ve BİRLEŞİK sütununda **sabahki** BİRLEŞİK'i kullanmıştı (liste HIRÇIN DADAŞ, SONEJDER, SUPHRA gösterdi; tahmin_10dk'nın gerçek listesiyle uyuşmuyordu). Sebepler: özet, tahmin_10dk'dan önce çalışıyordu ve −10 dk kaydını okumuyordu. Düzeltme: plan sırası tahmin_10dk → özet; özet `veri/tahminler_10dk` kaydından listeyi, riski ve BİRLEŞİK_10 sütununu okuyor. `veri/son_dakika/2026-11-26/İzmir_1.md` düzeltme öncesi çıktı olduğundan bu tutarsızlığı taşıyor (bilerek bırakıldı, tahmin kaydı doğru); sonraki koşular düzeltilmiş betikle üretilecek.
- Not: özet betiğini koşu bittikten sonra yeniden çalıştırmak, o anki (koşu sonrası) eBayi görüntüsüyle farklı rakam üretir; −10 dk özetini yeniden üretme.
- **Tetik −12 dk'ya çekildi (26.11, kullanıcı onaylı):** `agf_plan.py`: görüntü saatleri −30, **−12**, −10, −3 dk; son dakika özeti ve `tahmin_10dk` koşudan 12 dk önce tetikleniyor (tur gecikirse de gerçekte ≈−10 dk'da çıkar; 12 ile 10 dk arası piyasa bilgisi pratikte aynı). Sahte saatli deneme: 14:47'de tetik yok, 14:49'da −12 dk kaydı + özet + tahmin, 14:55'te yalnızca −10 dk kaydı (tekrar yok). Kayıtlardaki `goruntu_koşuya_dk` ≈12 olacak; puanlama geçerlilik aralığı (0–20 dk) aynı. Ad "−10 dk tahmini" olarak kaldı. İlk gerçek sınav: İzmir 2. koşu (15:30) ve sonrası.
- **Sonuç ganyanları kaydediliyor (26.11, kullanıcı isteği):** `puan_10dk.py` (gün sonu otomatik) artık `veri/tahminler_10dk/sonuc_ganyan.csv` yazıyor: her at için sonuç sırası, **kesin (kapanış) ganyan**, p_birlesik10, p_piyasa10, listede mi (her çalıştırmada yeniden üretilir; kaynak eBayi sonuç JSON'u). `SONUC.md`'ye ganyan getirisi satırı eklendi: tüm liste (her listedeki ata 1 TL) ve yalnızca ilk seçim için, kapanış ganyanıyla; tarihsel düz oyun getirisi ~%70–80 olduğundan ≥300 koşuda bu rakamların %100'ü anlamlı geçip geçmediğine bakılacak. İlk gün (İzmir 1): 3 atlık liste 3 TL → 3,3 TL (%110), ilk seçim %0; tek koşu, anlamsız. Zaten kayıtlı olanlar: `veri/para_takip.csv` (kesin ganyan, para), `veri/kazanan_profil.csv` (kazananın kesin ganyanı), ertesi gün `veri/at_gecmisi` (tüm atların kesin ganyanı).

## Lodato analizi ve kullanıcı uyarıları (26.11.2026)
- **Lodato (İzmir 2, 2. oldu, ganyan 11,45):** 4y a aygır, Lion Heart yavrusu; son altı K5 K6 K9 K1 K3 K1 (son üç 1-3-1), HP 59 → 66 (kariyer zirvesi), M. Göl (aynı jokey son 3 koşu), 1400 m rahat aralığı (≤1400: 16 koşu, 5 birinci, 8 ilk üç; 1401–1900: 8 koşu, 0 birinci). Derece 1.26,64 (mesafedeki önceki en iyisi 1.27,99). Piyasa: AGF %6,9; ganyan gün içinde 8,4 → 13,7 (para çıkışı), kapanış 11,45. Modeller: v9 AGF'li %6,9, AGF'siz %5, BİRLEŞİK %6,9; listemizde yoktu.
- **Kullanıcı uyarısı 1: para giren/çıkan atlar yanıltıcı olabilir.** Lodato örneğinde ganyanın yükselmesi ("para çıkıyor") sinyali yanıltıcıydı (at 2. oldu); İzmir 2'de 💰 Angel On The Right tutmadı, Last Sword'un 💰'ü tuttu. Para hareketi işaretleri (💰/📈/📉) test edilmemiş bilgi amaçlı işaretlerdir; aşırı giren/çıkan atlarda (ör. ganyan ±%50+) küçük havuz, tek büyük bahis ve eküri/AGF çifte etkisi gibi gürültü olasılığı var. Karar kuralı yapılmadan önce #7 testinde (≥500 koşu) ayrı "aşırı hareket" grubu olarak ölçülecek.
- **Kullanıcı uyarısı 2: Lion Heart yavruları kısa mesafeyi sever.** Geçmiş veriyle test (`at_gecmisi` 2020–2021 + 2024+; kapanış ganyanından normalize beklenen olasılığa göre A/E): ≤1400 m n=2.110, A/E 1,01 (z +0,2); 1500–1900 m n=1.381, A/E 1,02 (z +0,3); 2000+ m n=585, A/E 0,87 (z −1,2, anlamsız sınırda). Yani kısa mesafe eğilimi (uzun mesafede düşüş) yönünde ama **piyasa bunu zaten fiyatlıyor**, kısada ek avantaj yok. Soy bilgisi zaten v9'da (`soy_*`); kısa-mesafe soy etkisi için `soy_mesafe.json` mevcut.

## Koşul tercihleri: at ve baba bugünkü koşula uyuyor mu (26.11.2026, kullanıcı isteği: "atların türleri hangi koşulları seviyor çıkar")
- **Ne:** `tahmin_10dk.py` geçmişten (2020–2021 + 2024+, `at_gecmisi`) her at için ve babası (yavruları) için **mesafe bandı** (≤1200, 1300-1400, 1500-1700, 1800-2100, 2200+) ve **pist** (Kum/Çim/Sentetik) bazında: atın kendi koşu/birinci/ilk üç sayısı; babanın yavruları için kapanış ganyanına göre piyasa-düzeltmeli A/E ve z (n≥30). Bugünkü koşunun mesafe bandı ve pistine göre eşleştirip kayda (`atlar[].tercih`) yazıyor; `son_dakika_ozet.py` her listedeki at için "Koşul uyumu" satırı gösteriyor (n küçükse gösterge değil).
- **Düzeltme (Lodato):** önceki analizde "≤1400 m'de 16 koşu, 5 birinci" birleşikti; 1200 ve 1300–1400 ayrılınca Lodato'nun **1300–1400 m'deki kaydı bugüne kadar 5 koşu, 0 birinci, 0 ilk üç**; galibiyetleri 1200'de. Bugünkü 2. liği bu bantta ilk ilk-üç sonucuydu. Baba Lion Heart yavruları bu bantta A/E 0,98 (n=838, z −0,2): piyasa zaten fiyatlıyor.
- **Bugünün örneği (İzmir 2):** kazanan Last Sword'un 1300–1400 m kaydı 14 koşu 3 birinci 6 ilk üç, babası Touch The Wolf bu bantta A/E 1,17 (n=287, z +1,4): önceden görülebilen hafif olumlu uyum. Blue Reflection'ın babası bu bantta A/E 0,66 (z −1,8), Bocce'nin 0,85 (z −1,3).
- **Önceki testler:** soy×mesafe, ilk kez mesafe/pist, mesafe uyumu daha önce test edilmişti (`soy_mesafe.json`, `mesafe_uyum_test.json`); ek bilgi çoğunlukla piyasada fiyatlı çıkmıştı. Bu kayıt karar kuralı değil, her koşuya yan bilgi; ≥300 koşuda "tercihi olumlu olan atların A/E'si" ayrıca ölçülecek.
- **Koşul tercihleri genişletildi (26.11):** at ve baba tercihi artık **mesafe bandı, pist, koşu türü (aile: Maiden/Şartlı/Handikap/KV/Satış/Grup) ve hipodrom** boyutlarında; `tahmin_10dk` kaydında (`atlar[].tercih`) ve her koşunun son dakika özetinde "Koşul uyumu" satırı olarak (atın kendisi birinci/ilk3/koşu + babanın yavruları için A/E). Önceki sürüm yalnızca mesafe ve pist veriyordu.
- **Kalıcı tablo: `veri/soy_tercih.csv` ve `.md`** (`scripts/soy_tercih.py`, gün sonu otomatik): her baba × boyut × değer için n, birinci, beklenen, A/E, z ve **yalnızca ikinci yarıdaki A/E** (kalıcılık); 3.342 hücre (n≥60), 41'i n≥150 ve |z|≥2,5. En belirgin: KAYAYÜREKLİ yavruları Handikap'te A/E 1,57 (z 4,5; 2. yarı 1,73), GOOD CURRY Kum'da 1,42 (z 3,9; 1,43), TAMERİNOĞLU Şartlı'da 0,70 (z −3,5; 0,80), ŞİMŞEĞİNOĞLU Şanlıurfa'da 1,47 (z 3,5; 1,62), KINOWA Maiden'da 0,25 (n=180, 4 birinci), ARTOS 1300–1400 m'de 1,70. **Uyarı:** ~3.300 hücre bakıldığı için |z|≥2,5 olanların bir kısmı şans olabilir (iki yarıda aynı yönde kalanlar daha güvenilir); bunlar tarihsel kapanış ganyanına göre, canlı piyasa bunu zaten yansıtabilir. Canlı sınav: bu tabloda "iki yarıda da |z|≥2 olan" baba×koşul eşleşmelerinin yeni koşularda (ilgili atların) A/E'si ≥300 koşuda ölçülecek.
- **Mesafe odaklı görünüm (26.11, kullanıcı: "koşu türünden ziyade mesafe"):** son dakika özetindeki ek satır artık **mesafe profili**: atın kendisi her mesafe bandında (≤1200, 1300-1400, 1500-1700, 1800-2100, 2200+) birinci/ilk3/koşu ve babasının yavruları her bantta A/E; bugünkü bant [köşeli]. Tür ve hipodrom tercihi kayıtta (`atlar[].tercih`) ve `veri/soy_tercih.csv`'de duruyor ama özette gösterilmiyor. **Lodato:** kendi ≤1200 m'de 11 koşu, 5 birinci, 8 ilk üç (sprint uzmanı); 1300–1400'de 5 koşu 0 ilk üç; 1500+ m'de 0 birinci. Babası **Lion Heart yavruları tüm bantlarda A/E ≈1,0** (≤1200: 0,93; 1300–1400: 0,98; 1500–1700: 1,03; 1800–2100: 0,89): "Lion Heart kısayı sever" hipotezi yavru kitlesinde belirgin değil; Lodato'nun kısa/en kısa mesafe eğilimi **bireysel**.

## Mesafe profili testi (26.11.2026, `scripts/mesafe_profil_testi.py`, kullanıcı isteği)
- **Soru:** atın kendi ve babasının bugünkü mesafe bandındaki geçmişi piyasanın ötesinde bilgi taşıyor mu? Kronolojik, sızıntısız; test 5.731 koşu (2025-12-09 sonrası, 14.865 koşudan; b ilk %60'ta öğrenildi), geçmiş özellikleri 2020–2021-06 ve 2024+ verisinden (2021-06→2024-01 boşluğu nedeniyle bir miktar gürültü).
- **Sonuç: ek bilgi yok.** Koşullu logitte (piyasa + özellik) öğrenilen katsayı tüm özelliklerde **0** çıktı (kendi bant ilk-3 oranı farkı, babanın bant A/E'si, ikisi birlikte): kazanç/koşu +0,00000. Gruplar: "uyumlu at" (bantta ≥4 koşu, ilk-3 ≥%50 ve genel orandan ≥15 puan iyi) A/E 0,95 (z −1,2) ilk yarı, 1,01 (z +0,3) ikinci yarı; "uyumsuz at" (bantta ≥4 koşu, hiç ilk-3 yok) 0,95 (z −0,6) / 0,92 (z −1,0). Yani piyasa mesafe uyumunu zaten fiyatlıyor; kâr getiren bir "mesafe uyumu" kuralı yok. Önceki `mesafe_uyum_test.json` sonucuyla tutarlı.
- **Yorum:** Özetteki "mesafe profili" insan için bağlam bilgisi olarak kalıyor (örn. Lodato'nun 1200 m uzmanlığı), tahmin hesabına katılmıyor. 2021-10→2023 boşluğu dolunca (indirme sürüyor) `at_gecmisi` yeniden kurulup test tekrarlanabilir (daha çok geçmiş, daha az gürültü).
- **Sürpriz odaklı bakış (26.11, kullanıcı: "bunları sürprizde arıyoruz, piyasa bilemez"):** yalnızca uzun atlar (piyasa p<%10; 92 bin at-koşu, test dönemi 2024-07+), A/E ilk yarı | ikinci yarı: **tüm uzun atlar 0,94 (z −2,6) | 0,94 (z −3,0)**: uzun atlar piyasada fazla fiyatlanıyor (favori–uzun at yanlılığı), yani "uzun atı seçmek" varsayılan olarak kaybettirir; ancak süzgeç değer taşır. Mesafeye uyumlu uzun at (n=2.001 | 2.407): **1,02 | 1,00** (yanlılığı ortadan kaldırıyor, ≥1'in üstüne çıkarmıyor); uyumsuz: 0,87 | 0,95; **baba bant log(A/E) ≤ −0,10 olanlar 0,84 (z −3,4) | 0,93** (kaçınılacak grup), baba ≥ +0,10: 0,99 | 1,03; **uyumlu at + baba olumlu (n=777 | 954): 1,11 | 1,18** (z +0,7 | +1,3; birleşik ≈ +1,4: umut verici ama anlamsız). Beklenmedik: atın kendi bant farkı ≤ −0,15 olanlar 1,13 | 1,24 (z +1,1 | +2,2) ve ≥ +0,15 olanlar 1,11 | 0,98: kendi bant farkı tek başına tutarlı yön vermiyor (küçük bantta az koşu, ortalamaya dönüş olabilir; 9 grup × 2 yarı bakıldığı için bir kısmı şans). **Sonuç:** mesafe profili uzun atlarda esas olarak **kötü uzun atları ayıklıyor** (özellikle babası o bantta kötü olanlar); pozitif avantaj (uyumlu + baba olumlu, A/E ≈1,1–1,2) işaret var ama kanıtlanmadı. ≥1.000 uzun at örneğiyle (özellikle 2021-10→2023 verisi eklenince) tekrar test edilecek; canlı olarak sürpriz adaylarının özetine "mesafe uyumlu + baba olumlu" işareti eklenebilir (şimdilik bilgi amaçlı).
- **🎯 işareti eklendi (26.11, kullanıcı onaylı, yalnızca bilgi):** `tahmin_10dk` kaydında `tercih.mesafe_uyum` (uyumlu/uyumsuz/None), `tercih.baba_log_ae` ve `tercih.hedef`; son dakika özetinde 🎯 = uzun at (piyasa <%10) + atın bugünkü mesafe bandında ≥4 koşusu, ilk-3 ≥%50 ve genel orandan ≥15 puan iyi + babası bu bantta büzülmüş log(A/E) ≥ +0,05 (testteki "uyumlu at + baba olumlu" tanımı; geçmişte uzun atlarda A/E 1,11 | 1,18, anlamsız). İzmir 2'de 🎯 yok (Bocce uyumlu ama babası olumsuz; Lodato 'uyumsuz' sınıfındaydı, 2. oldu: o grup geçmişte A/E 0,87–0,95). Canlı sınav: 🎯 atlarının sonuçları `sonuc_ganyan.csv` ve özet dosyalarından toplanıp ≥100 🎯'da A/E ölçülecek.
- **Anne tarafı (26.11, kullanıcı: "babaya bakma, anası da var"):** Lodato: baba LION HEART (USA), anne RUMBA, anne babası DEHERE (USA) (Dehere yavruları ≤1200 m'de A/E 1,26 (n=168), diğer bantlarda ≈0,93–0,98). Özet ve tahmin kaydı artık **anne babası**nın bant A/E'sini de gösteriyor (`tercih.annebaba`, `annebaba_mesafe_hepsi`). **Uzun atlarda test** (`mesafe_profil_testi.py`, ilk yarı | ikinci yarı A/E): anne babası olumlu (log A/E ≥ +0,10) 0,99 | 0,89; olumsuz 0,94 | 0,93; **anne (dam)** olumlu (n≥8) 1,03 | 0,91, olumsuz 0,93 | 0,96; baba VE anne babası olumlu 0,98 | 0,97, ikisi de olumsuz 0,90 | 0,88; uyumlu at + baba + anne babası olumlu (n=293 | 337) 0,87 | 1,08. **Sonuç: anne tarafı ek bilgi vermiyor**; "uyumlu at + baba olumlu" grubuna anne babası koşulu eklenince önceki 1,11 | 1,18 işareti kayboluyor (bu da o işaretin şans olabileceğini destekliyor). Anne tarafı özette bağlam bilgisi olarak duruyor, 🎯 tanımına katılmadı.
- **LODATO soy ağacı (26.11, kullanıcı sorusu):** baba LION HEART (USA), anne RUMBA, anne babası DEHERE (USA). Annenin verimizde yalnızca 2 yavrusu var (Lodato 25 koşu; Rumbita, babası Super Saver, 4 koşu): anne düzeyinde bilgi yok. Lodato'nun kendi mesafe kaydı: ≤1200 m 11 koşu 5 birinci 8 ilk üç; 1300–1400 m 5 koşu 0 ilk üç; 1500–1700 m 7 koşu 1 ilk üç; 1800–2100 m 2 koşu 0. **Aynı çaprazlama (Lion Heart × anne babası Dehere), Lodato dahil:** ≤1200 m 44 koşu 9 birinci beklenen 4,4 (A/E 2,05); 1300–1400 49 koşu A/E 1,04; 1500+ A/E 0,86 ve 0. **Lodato hariç yalnızca 7 at:** ≤1200 m 33 koşu 4 birinci beklenen 2,8 (A/E 1,43); 1300–1400 m 44 koşu A/E 1,20; 1500+ m 27 koşu 1 birinci beklenen 1,9 (A/E 0,53). Yön tutarlı (kısa iyi, uzun kötü) ama örnek çok küçük (7 at, 4–5 birincilik): gösterge, kanıt değil. Çaprazlama (baba × anne babası) bazında test henüz yok; yeterli at/koşu olan çaprazlamalar için ayrı test (≥150 koşu) yapılabilir.
- **Yalnızca baba (26.11, kullanıcı kararı):** son dakika özetindeki mesafe profili satırından anne babası kaldırıldı; özet yalnızca atın kendisi ve **babası**nı gösteriyor. Anne babası verisi kayıtta (`tercih.annebaba*`) duruyor, görüntülenmiyor. Baba × anne babası çaprazlama testi yapılmadı (kullanıcı istemedi).

## ebayi indirmesi tamamlandı, at_gecmisi yeniden kuruldu, mesafe testi tekrarlandı (26.11.2026)
- **Veri:** `veri/arsiv/ebayi` 2021-10-06 → 2023-12-31 tamam (817 gün, 0 eksik; Şubat 2023'te yalnızca 16 yarış günü, deprem dönemi; 5 geçici ağ hatası yeniden denemeyle geçti). `at_gecmisi.py kur`: 2.409 gün, **402.395 satır, 24.943 at, 41.890 koşu** (önce 1.502 dosya → 2.416). Mevcut günlerin içeriği değişmedi (git'te değişen dosya 0), yalnızca yeni günler eklendi (2022, 2023 klasörleri, ~9 MB). Boşluk 2020-01 → 2026-11 arasında kapandı (2020 Mart–Haziran pandemi hariç). **#8 çözüldü.**
- **Mesafe profili testi tekrarı** (`mesafe_profil_testi.py`, test dönemi aynı: 2024-07 sonrası; geçmiş özellikleri artık 2020–2026 tam veriden): uzun atlarda (piyasa p<%10) "mesafeye uyumlu at + baba olumlu" **A/E 0,98 | 0,98** (n=896 | 967); önceki 1,11 | 1,18 işareti **şans çıktı**. Mesafeye uyumlu at 1,03 | 0,93; uyumsuz 0,90 | 0,94; baba bant log(A/E) ≤ −0,10 olanlar 0,87 (z −2,4) | 0,95 (kaçınılacak grup yönü korundu); baba ≥ +0,10: 1,00 | 1,02. Koşullu logitte kendi+baba kombinasyonu **anlamlı negatif** (−0,0033/koşu, aralık −0,0057…−0,0007): özellik katmak zarar veriyor. Anne tarafı yine ek bilgi vermedi. **Sonuç: mesafe profili uzun atlarda pozitif avantaj sağlamıyor; esas işlevi (kötü uzun atları ayıklama, zayıf) dışında bağlam bilgisi.** 🎯 işaretinin dayanağı kalmadı; özette "avantaj YOK; yalnızca bilgi" notuyla duruyor.

## Terim: "sürpriz" yerine "gözden kaçan / gelmesi muhtemel" (26.11.2026, kullanıcı)
- Kullanıcı: sürprizi bulmak kolay değil; bu atlar ayrı takip ediliyor ki **genel özellikleri anlaşılsın** ve gelmesi muhtemel olanlar gözden kaçmasın. Ekranda görünen metinlerde "sürpriz" yerine **"gözden kaçan kazanan"** (ganyan ≥10 ya da AGF <%10 olan kazanan) ve koşu düzeyinde **"açık koşu riski"** (3/4/5 atlık liste kuralı) yazılıyor: `son_dakika_ozet.py`, `tahmin_10dk.py` (md), `puan_10dk.py`, `hata_raporu.py`, `kosu_tipi_rapor.py`. Dosya ve alan adları (`surpriz_*`, `surpriz_riski`) uyumluluk için aynı kaldı.
- **Gözden kaçan kazananların genel özellikleri (`scripts/gozden_kacan_ozellik.py` → `veri/gozden_kacan_ozellik.md`, gün sonu otomatik):** uzun atlar (piyasa p<%10; 256.559 at-koşu, 10.425 kazanan, 2020–2026), tipik uzun ata göre **göreli A/E** (genel uzun at A/E 0,93; 1,00 = tipik uzun at) ve iki yarıda tutarlılık. Öne çıkanlar (|z|≥2,5, iki yarıda aynı yön): **HP rakiplerine yakın (orta) 1,10 (z +6,2) ve yüksek 1,05 (+2,7); HP düşük (ortalamanın ≥4 altında) 0,86 (z −8,8); aygır 1,07 (+4,4); genç dişi 0,90 (−4,9), kısrak 0,93; Handikap çeşidi 1,06; mesafesi kısalan 1,06; iç start (1–3) 1,05; Diyarbakır 1,21 (n=5.897; hipodrom bazlı tek çıkış); 90+ gün aradan gelen 0,82 (ikinci yarıda 0,73); ilk koşusu olanlar (geçmiş yok) 0,89.** Yaş ve jokey değişimi ayırt edici değil (≈1,0). Etkiler küçük (±%5–15): en iyi grupların bile A/E'si ≈ 0,93 × 1,10 ≈ 1,0, yani uzun at yanlılığını yalnızca ortadan kaldırıyor; pozitif avantaj yok. Yorum: gelmesi muhtemel uzun atlar tipik olarak rakiplerine yakın HP'li, aygır, handikap koşusunda, iç startlı, mesafesi kısalan atlar; düşük HP'li, dişi, uzun aradan dönen ve ilk koşusu olan uzun atlar daha az geliyor.

## ⚠ HATA BULUNDU VE DÜZELTİLDİ: HP sırasındaki eşitlik sızıntısı (26.11.2026)
- **Ne oldu:** `gozden_kacan_model.py` ilk çalıştırmada uzun atlarda mucize gibi sonuç verdi (en iyi %1 diliminde ROI +%319, kazanma %30). Teşhis: `hp_sira` özelliği `argsort().argsort()` ile hesaplanıyordu; **HP eşit olunca (özellikle HP=0 olan koşularda) sıra satır sırasıyla bozuluyordu ve at_gecmisi satırları bitiş sırasına göre dizili** (ebayi sonuç JSON'u da bitiş sırasında). Yani eşitlikte kazanan hep 1. sıra alıyordu: etiket sızıntısı.
- **Etkilenen önceki sonuçlar (hepsi düzeltildi/geri çekildi):** (1) `surpriz_ortak.py` (20.11): "HP sırası ilk 3 A/E 1,30 (z 7,1)" ve "gny≥10 + AGF≥1,3× + HP ilk 3 → 1 TL getirisi %127" → düzeltilince **HP ilk 3 A/E 0,95 (z −1,4), 4-6: 0,90, 7+: 0,88**: avantaj YOK; %127 iddiası **geçersiz**. (2) `para_takip.py` canlı `sinyal` sütunundaki "HP ilk 3" (19.11'den beri) aynı hatalıydı, düzeltildi; eski satırlar önyargılı. `analiz3.py` ⭐ etiketi ve `hata_raporu.py` HP notu metinleri değiştirildi. (3) `shap_surpriz.py` ve `taslak_kalibrasyon_shap.py` düzeltildi: düzeltilmiş SHAP (test 5.731 koşu) modelin kazananın ort. log-olasılığı −1,998 (piyasa −1,835; önceki −1,876 sızıntılıydı), model 1. seçim %26,7 (önceki %32,4); sürpriz kazananlarda hp_fark katkısı −0,004 (önceki +0,266 sızıntıydı), jokey_oran −0,143, hp_sira −0,066. (4) `kazanan_profil.py` `sira()` (kazananın HP sırası) eşitlikte kazananı öne alıyor (sonuç JSON'u bitiş sırasında); CSV'deki `hp_sira` sütunu yalnızca eşitsiz HP'lerde güvenilir. Düzeltme gerekiyor (canlı sistem; onay bekliyor).
- **Düzeltilmiş uzun at modeli** (`gozden_kacan_model.py`, piyasa logit'i sabit, yalnızca artığı öğreniyor; test 101.546 uzun at-koşu, 4.127 kazanan, eğitim<2024-04-03): test log-kaybı yalnızca piyasa 0,16066 → piyasa+model 0,15938, **fark +0,00128 (%95 [+0,00101, +0,00155])**: küçük ama anlamlı. Modelin piyasaya göre oranına göre onluk dilimlerde A/E: **0,34 | 0,60 | 0,71 | 0,83 | 0,83 | 0,93 | 0,93 | 1,01 | 1,13 | 1,30** (üst dilim 757 kazanan / 582 beklenen, alt dilim 56 / 163): yani model uzun atlar arasında "gelmesi muhtemel olanları" gerçekten ayırt ediyor ama etkisi orta. Gain önemi: hp_fark %11, p_logit %8, kgs %7, jokey_oran %7, bas_basa %7, kilo_fark %7, antrenor_oran %5, start %4, yaş %4; **tek bir gizli faktör yok, çok sayıda küçük etki.** SHAP (kazananlarda): p_logit +0,059, hp_fark +0,047, jokey_oran +0,019, antrenor_oran +0,013, bas_basa +0,012. **Gerçek ganyan getirisi (1 TL, kapanış ganyanı):** en iyi %1 ROI −%15,8 [−34, +4] (ilk yarı +13%, ikinci −41%: kararsız); en iyi %5 −%8,5; **en iyi %10 −%9,0 [−16, −2]**; en iyi %20 −%14,9; tüm uzun atlar −%40,1. Yani süzgeç kaybı −%40'tan −%9'a indiriyor ama kâra geçmiyor.
- **Ders:** özellik hesaplarında satır sırasına bağımlı (argsort/sort bağı) işlemler yasak; sıralı veride eşitlikte sıra ayrıştırması etiketi sızdırır. Yeni testlerde "çok güzel" sonuç çıkarsa ilk iş sızıntı aranacak.
- **Düzeltmeler tamamlandı (26.11, kullanıcı "hata varsa düzelt" dedi):** `kazanan_profil.py` `sira()` ve `analiz3.py` HP sırası (`_hps`, ⭐ işareti) eşitlikte sıra vermeyecek şekilde (kesin büyük olan sayısı + 1) düzeltildi; deneme: HP 38,38,30,boş → sıralar 1,1,3,4. **Kalan etki:** `veri/kazanan_profil.csv` ve `veri/para_takip.csv`'nin 19–26.11 arası satırlarındaki `hp_sira` / `sinyal` (HP ilk 3) değerleri eski hatalı hesapla yazılmış (eşitlikte kazanan öne alınmış): bu sütunlara güvenme, yeni satırlar düzeltilmiş kodla yazılacak. Tüm `scripts/` ve `tests/` sözdizimi kontrolünden geçti, 61 pytest geçti.
- **HP sırası düzeltmesi uygulandı (26.11, `scripts/hp_sira_duzelt.py`, kullanıcı onaylı):** `veri/kazanan_profil.csv` 116 kazanan satırı yeniden hesaplandı: **hiçbir `hp_sira` değişmedi** (kazanan için "1 + HP'si kesin büyük at sayısı" eski sıralı-sort yöntemiyle aynı sonucu verir; hata yalnızca kazananla kaybedenleri karşılaştıran testlerde sızıntı yaptı, yalnızca kazananların tablosunda değil). Yani önceki "kazanan_profil hp_sira güvenilmez" uyarım fazlaydı: bu sütun doğru. `veri/para_takip.csv` `sinyal` (HP ilk 3): **8 satır değişti, sinyal=1 toplamı 16 → 24** (eşitlikte kaybeden atlar eskiden dışarıda kalıyordu); yeni değerler doğru hesapla yazıldı. Eski "para_takip.csv/kazanan_profil.csv güvenme" notu yalnızca para_takip.csv `sinyal` için geçerliydi ve artık giderildi.

## 26.11.2026 gün sonu özeti (İzmir 7 + Antalya 7 = 14 koşu, −12 dk tahmini)
- **Kazanan listede 14/14** (yüksek risk 5 at: 7/7; orta 4 at: 3/3; düşük 3 at: 4/4). İlk seçim kazandı: BİRLEŞİK_10 5/14 (%36), piyasa_10 5/14, **v9 AGF'li (sabah) 7/14 (%50)**, v9 AGF'siz 6/14 (%43); ilk 3'te bulma %71 / %71 / %86 / %86; kazananın ort. log-olasılığı −1,67 / −1,66 / −1,59 / −1,50 (aralıklar çok geniş, kol üstünlüğü kanıtlanmaz). Ganyan getirisi (1 TL/at, kapanış ganyanı): tüm liste 59 TL → 58,9 TL (**%100**); yalnızca ilk seçim 14 TL → 11,2 TL (%80).
- **Gözden kaçan kazanan (ganyan ≥10): 1/14** — Antalya 5 Çelikgiller (10,80; listede 4. sırada, yüksek risk 5 at; 💰 38,85 → 11,3; aynı koşuda 💰'lü 3 at daha vardı ve kazanamadı). Beklenen ~%16 (≈2,2 koşu). Bugün çok sayıda kazanan 1–2 favori oynamış: kazananların ganyanı 1,20–6,45 (Çelikgiller hariç), bu nedenle liste isabeti şişkin, geçmiş beklenti %76–81.
- **Sabah v9 AGF'li kolu bugün −12 dk BİRLEŞİK_10'dan iyi** (7/14 ilk seçim; İzmir 5'te Cabbar Efe'yi 1. seçmişti). 14 koşu anlamsız; ≥300 koşuda ölçülecek.
- **Hatalar/düzeltmeler (bugün):** HP sırası eşitlik sızıntısı bulundu, eski "HP ilk 3, getiri %127" bulgusu geri çekildi; kodda iki sözdizimi hatası (tırnak) yapıldı ve aynı saat içinde düzeltildi; 🎯 işaretinin dayanağı kalmadı (A/E 0,98). −12 dk tetiği, mesafe profili (at+baba), koşu çeşidi kaydı, sonuç ganyanları ve gözden kaçan kazanan raporu eklendi. İndirme tamamlandı: at_gecmisi 2020-01→2026-11 (402 bin satır).
- Yarın sabah beklenen: TAM+15 dk dondurma doğrulaması, yeni gün programı.

## 27.11.2026 hazırlığı
- Program (ebayi, 26.11 akşamı): **Bursa ve İzmir** (+ yabancı hipodromlar). Yenibeygir gece Blt kaydı alındı: `veri/yenibeygir_el_kayit/blt_2026-11-27.csv` (İzmir 6 koşu 53 at, Bursa 7 koşu 74 at; koşu başı toplam 93–97). Sabah 09:40 TR'de otomatik kontrol (plan, TAM saatleri, TAM+15 dk dondurma, Blt–AGF karşılaştırması) zamanlandı. Actions döngüsü yarın 07:55 cron-job.org tetiğiyle başlar. 61 pytest geçti.

## 27.11.2026 sabah kontrolü (otomatik, 09:44 TR)
- **Sorunsuz:** plan oluştu (Bursa 14:00–17:00, 7 koşu; İzmir 19:00–21:30, 6 koşu); ilk yayın 09:05 TR (tjk=ebayi), TAM 09:15; **v9 dondurma 09:33 = TAM+18 dk** (düzeltme çalıştı), AGF=0 at oranı 0,000; Actions 07:55'ten beri kayıt yapıyor (cron-job.org tetiği çalıştı).
- **Blt/AGF (Bursa+İzmir):** yenibeygir sütunu sabah altılı koşularda AGF'ye döndü (Bursa/İzmir 1. koşu Blt kaldı). Yenibeygir sabah AGF'si resmî AGF ile (09:45 görüntü): İzmir ort. fark 1,5 puan (Spearman 0,95; en yüksek aynı 6/6), Bursa 1,1 (0,96; 5/6) = resmî kaynağın kopyası. **Gece Blt'si resmî AGF'ye karşı:** İzmir 7,0 puan fark (Spearman 0,62; en yüksek aynı 3/6), Bursa 5,8 (0,61; 3/7): dünkü sonuçla aynı, Blt AGF'den ayrı ama ilişkili bir sinyal. Kayıt: `veri/yenibeygir_el_kayit/blt_2026-11-27.csv`. Sonuçlarla (Blt'nin kazananı bilme oranı) akşam bakılacak.
- **Kurulum düzeltmesi:** task-observer çalışma kökü sabitlemesi yanlıştı (`.../skill-observations` yerine skill'in kendi eklediği alt klasör için kök `/home/user/at-yarisi` olmalı); `CLAUDE.md` bloğu ve `.claude/hooks/task-observer-start.sh` düzeltildi, çalışma alanı oluşturuldu, ilk oturum başlangıç taraması çalıştı (0 gözlem).
