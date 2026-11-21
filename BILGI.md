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
