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
- Kota: 10 dakikalık döngü bağımsız süreç olarak çalışır (model turu harcamaz); 3 saatte bir ve gün sonunda kayıtları kendisi GitHub'a kaydeder. Model turu gerektiren kontrol görevi günde 2 kez (07:03, 13:03): döngü durmuşsa başlatır.
