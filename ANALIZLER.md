# Analiz dizini (hepsi gerçek veriyle; ayrıntı ve sonuçlar BILGI.md'de)

Günlük rapora (scripts/analiz3.py) eklenenler – at seçmeden önce bakılır, hiçbir at elenmez:
| Analiz | Betik | Sonuç dosyası | Raporda |
|---|---|---|---|
| Hipodrom sürpriz oranı | scripts/hipodrom_surpriz.py | veri/hipodrom_surpriz.json | HİPODROM satırı |
| Koşu türü / maiden | scripts/kosu_turu_analiz.py, maiden_analiz.py | veri/kosu_turu_analiz.json, maiden_analiz.json | KOŞU TÜRÜ / MAİDEN satırı |
| Belirsiz koşuda geniş liste (%85, en çok 8) | analiz3.py | – | aday sayısı |
| At geçmişi (koşu, mesafe bandı, son koşu) | scripts/at_notlari.py | veri/at_gecmisi/ | AT GEÇMİŞİ |
| İlk kez hipodrom / mesafe / en uzun / en kısa | scripts/ilk_kez_test.py | veri/ilk_kez_test.json, mesafe_degisim_test.json | AT GEÇMİŞİ etiketleri |
| Mesafe değişimi (son koşuya göre) | (mesafe_degisim_test) | veri/mesafe_degisim_test.json | AT GEÇMİŞİ |
| Atın mesafe uyumu | scripts/mesafe_uyum_test.py | veri/mesafe_uyum_test.json | AT GEÇMİŞİ (bant kaydı) |
| Sınıf farkı (rakipler daha zayıf/güçlü) | scripts/sinif_dusus.py, sinif_ozellik.py | veri/sinif_dusus.json | AT GEÇMİŞİ, UYARI |
| Soy x ırk x mesafe | scripts/soy_mesafe.py | veri/soy_mesafe.json | AT GEÇMİŞİ (soy) |
| Grup (koşu türü) düşüşü/yükselişi | scripts/tur_seviye.py, ek_ozellik.py | veri/tur_seviye.json | AT GEÇMİŞİ (GRUP DÜŞÜŞÜ/YÜKSELİŞİ), model |
| Baba hattı ve anne babası x ırk x mesafe | scripts/kan_hatti.py | veri/kan_hatti.json | AT GEÇMİŞİ (baba hattı, anne babası) |
| Sürprizlerin ortak noktaları (HP ilk 3, AGF/ganyan) | scripts/surpriz_ortak.py | veri/surpriz_ortak.json | ⭐ SÜRPRİZ ADAYI |
| EK ADAY / UYARI kuralı | analiz3.py | JSON ek_aday | ► EK ADAY, ► UYARI |

Her koşudan sonra otomatik (GitHub Actions):
| Takip | Betik | Dosya |
|---|---|---|
| AGF/ganyan görüntüleri (sabah iki kaynak, öğle, −60/−30/−10/−3) | agf_plan.py, agf_kayit.py | veri/agf_kayit/ |
| Para girişi 💰, sessiz AGF 🤫, ⭐ sinyal | para_takip.py | veri/para_takip.csv |
| Kazanan profili / sürpriz takibi | kazanan_profil.py (ozet) | veri/kazanan_profil.csv |
| Model sonuçları (AGF'li, AGF'siz) | canli_takip.py | veri/canli_takip*.csv |
| At geçmişi günlük ekleme | at_gecmisi.py | veri/at_gecmisi/ |
| Kuponlar | (elle) | veri/kuponlar.csv |

Model testleri (kabul edilmeyenler dahil): eski_veri_test.py, model9 + uzun geçmiş, sinif_fark özelliği, ganyan_ozellik_test.py – BILGI.md.
