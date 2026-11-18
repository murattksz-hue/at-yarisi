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
