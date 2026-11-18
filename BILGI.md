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
