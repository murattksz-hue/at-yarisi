# at-yarisi: Claude için proje notları

Türkiye at yarışları (TJK): her koşuyu kaydet, koşudan önce tahmin yap, sonucu ölç, hatalarımızdan öğren. **Önce `ANALIZ_INDEKSI.md` oku** (tüm analizler ve sonuçları tek tabloda; geri çekilen/geçersiz bulgular işaretli). Ayrıntılı bulgular `BILGI.md` (tarihli bölümler), bekleyen testler `YAPILACAK_TESTLER.md`.

## Kullanıcı tercihleri (uy)
- **Kısa ve net Türkçe**, laf kalabalığı yok. Telefondan adım adım yönlendir. Belirsizliği açıkça söyle.
- **Repoyu bozma.** Canlı sisteme (`agf_plan.py`, `agf_kayit.py`, `.github/workflows/kayit.yml`) dokunmadan önce onay al; değişiklikten sonra sahte saatle dene (`PLAN_DENEME=1 PLAN_SIMDI=...`).
- Terim: "sürpriz" yerine **"gözden kaçan kazanan"** (ganyan ≥10 ya da AGF <%10), koşu için **"açık koşu riski"**.
- Bota kapalı sitelerden (Cloudflare 403, ör. agftablosu) veri çekme, korumayı aşma. Şartı yasaklayan sitelerden (yenibeygir) otomatik çekim yok; yalnızca elle, seyrek, tek istek. Anahtarları sohbete yazdırma (`request_credential`).
- Sonuçlar `BILGI.md`'ye tarihli bölüm olarak yazılır, her iş commit+push edilir (branch `ccr-3087f440-aokn7a`). `Co-Authored-By` satırı eklenir.
- Repo public, lisans yok (tüm hakları saklıdır, README'de).

## Günlük akış (otomatik, GitHub Actions + cron-job.org)
1. 07:55 TR cron-job.org Actions'ı tetikler (`kayit.yml` → `scripts/agf_plan.py` zincirli döngü). Veri `veri/agf_kayit/<gün>/`.
2. AGF ilk yayın kısmi gelir; **TAM** = altılıdaki her koşuda atların ≥%90'ının AGF'si dolu (`agf_tam.py`). Dondurma **TAM+15 dk** sonra, en son dolu görüntüyle (v9 AGF'li/AGF'siz → `veri/tahminler/`).
3. Her koşu için görüntüler −60, −30, −12, −10, −3 dk (`para_takip.csv`). **−12 dk'da** `tahmin_10dk.py` (BİRLEŞİK_10 = piyasa + baş-başa; liste uzunluğu riske göre **3/4/5 at**) ve `son_dakika_ozet.py` (`veri/tahminler_10dk/`, `veri/son_dakika/`).
4. Koşu sonrası: `canli_takip.py`, `kazanan_profil.py`, `para_takip.py`, `surpriz_ayri.py`. Gün sonu: `puan_10dk.py` (SONUC.md, sonuc_ganyan.csv), `hata_raporu.py`, `kosu_tipi_*`, `soy_tercih.py`, `gozden_kacan_ozellik.py`.
5. Elle: yenibeygir "Blt" (Bülten Ortalama Puanı; altılı koşularda sabah AGF'ye döner): `scripts/yenibeygir_blt_kayit.py`.

## Veri
- `veri/at_gecmisi/<yıl>/<gün>.csv.gz`: 2020-01 → bugün (ebayi sonuçları; `at_gecmisi.py kur .gunluk/ebayi`), `veri/arsiv/ebayi` ham JSON. Kaynaklar: TJK CSV (medya-cdn, `?t=` önbellek atlatır), ebayi.org JSON (`/s/d/sonuclar/<YYYYMMDD>/full/<HIP>.json`).
- Türkiye hipodromları: Adana, Ankara, Antalya, Bursa, Diyarbakır, Elazığ, İstanbul, İzmir, Kocaeli, Şanlıurfa.

## Ders: sızıntı
- Sonuç dosyaları **bitiş sırasında** dizili. `argsort/sorted` ile HP sırası vb. hesaplarken **eşitlikte sıra yok**: sıra = 1 + kesin büyük olan sayısı (26.11'de bu hata "HP ilk 3, getiri %127" bulgusunu üretmişti, geri çekildi). Çok güzel sonuç çıkarsa önce sızıntı ara.
- Python betiği yazarken f-string içindeki tek tırnak (`A/E'si`) sözdizimini bozar; push'tan önce `ast.parse` ile tüm betikleri kontrol et.
- `python3 -I` script dizinini sys.path'e koymaz (`sys.path.insert(0, scripts)`).

## Bilinen bulgular (özet)
- Piyasa (kapanış ganyan/AGF) iyi kalibre; uzun atlar (p<%10) piyasada fazla fiyatlı (A/E 0,93). Mesafe/baba/anne profili, jokey değişimi, HP ilk 3 piyasanın ötesinde bilgi vermedi. Düzeltilmiş uzun at artık-modeli küçük ama anlamlı (+0,0013 log-kayıp), ROI yine negatif (en iyi %10: −%9).
- Liste kuralı (geçmiş): düşük risk K3 %77, orta K4 %81, yüksek K5 %76. 26.11: 14/14.

## Bekleyenler
- ≥300 canlı koşuda: BİRLEŞİK_10 / v9 / piyasa karşılaştırması; 💰 (aşırı hareket ayrı grup), Blt–AGF, çeşit/hipodrom bazlı kol seçimi (YAPILACAK_TESTLER.md B grubu).
- 26 Aralık 10:00 TR: 1 aylık değerlendirme (zamanlı hatırlatma kuruldu).
- Test: `python3 -m pytest tests -q` (61); sözdizimi: `python3 -I -c "import ast,glob;[ast.parse(open(p).read()) for p in glob.glob('scripts/*.py')]"`; tarama: `bash scripts/kor_hata_tara.sh`.
