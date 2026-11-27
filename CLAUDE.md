# at-yarisi: Claude için proje notları

Türkiye at yarışları (TJK): her koşuyu kaydet, koşudan önce tahmin yap, sonucu ölç, hatalarımızdan öğren. **Önce `ANALIZ_INDEKSI.md` oku** (tüm analizler ve sonuçları tek tabloda; geri çekilen/geçersiz bulgular işaretli). Ayrıntılı bulgular `BILGI.md` (tarihli bölümler), bekleyen testler `YAPILACAK_TESTLER.md`.

## Kullanıcı tercihleri (uy)
- **Kısa ve net Türkçe**, laf kalabalığı yok. Telefondan adım adım yönlendir. Belirsizliği açıkça söyle.
- **Repoyu bozma.** Canlı sisteme (`agf_plan.py`, `agf_kayit.py`, `.github/workflows/kayit.yml`) dokunmadan önce onay al; değişiklikten sonra sahte saatle dene (`PLAN_DENEME=1 PLAN_SIMDI=...`).
- **KURAL (kullanıcı koydu, kupon):** kalabalık ve riskli koşuya (açık koşu riski yüksek, çok at) daha ÇOK at, düşük riskli koşuya az at. Kupon kurarken önce risk sınıfı ve liste uzunluğu (3/4/5), kolon sayısı sonra. TEK AT yalnızca açık koşu riski DÜŞÜK sınıfta VE piyasa favori payı >=%50 iken (kullanıcı kuralı 27.11; İzmir 4'te %37'lik Canvelo tek at yatıp 30 kolonu birden yaktı); aksi halde en az 2 at, orta ve yüksek riskte liste. Riskli koşuya ASLA tek at koyma, kupon ayarı gerekse bile (kullanıcı tekrar vurguladı 27.11). Bütçe yetmezse altılıdan vazgeç, daha kısa bahis öner. Bunu ihlal etme, gerekçe yazma, uzatma.
- **KURAL (risk sınıfı, kullanıcı koydu 27.11):** her öneri/kupon öncesi koşunun risk sınıfını tüm analizlerle belirle (AGF riski `tahmin_10dk` sınıfı + `kosu_riski_modeli.py` + çeşit/at sayısı). Ölçüler çelişirse DAHA RİSKLİ olanı al. Hatasız ayırt etmek mümkün değil (AUC ~0,66), bunu söylemeden kesinmiş gibi sunma.
- **KURAL (AGF ile v9 ayrışırsa, 27.11):** atı listeden ÇIKARMA, EKLE. AGF'nin yükselttiği at gelir, v9'un tuttuğu at da kalır. "AGF'ye uy" kararı test edilmedi (Bursa 5'te Sinoplu Merve çıkarılıp Havzalı konmuş, Sinoplu 2., Havzalı 6. bitirdi). Liste uzunluğu risk sınıfına göre kalır, ayrışma için ek kolon gerekirse bütçeyi değil riski öncele.
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

## Araçlar (claude-plugins-official)
- `.claude/settings.json` marketplace'i ve şu plugin'leri açar: claude-md-management, hookify, code-review, pr-review-toolkit, code-simplifier, session-report, security-guidance, pyright-lsp (yeni oturumda yüklenir; onay istenirse kabul et).
- `.claude/skills/root-cause-investigation/` (nimrodfisher/data-analytics-skills, MIT; 27.11 kuruldu): beklenmeyen sonucun (gözden kaçan kazanan, tutmayan kupon) nedenini sistematik arama; betik yalnızca csv okur.
- `.claude/skills/analysis-qa-checklist/` ve `data-quality-audit/` (nimrodfisher, MIT; 27.11 kuruldu): analizi paylaşmadan önce kalite kontrol listesi ve etiket/veri hatası denetimi (Arap etiketi, HP sızıntısı tipi hataları yakalamak için). Betikler yalnızca pandas, ağ yok.
- `.claude/hookify.*.local.md` kuralları: canlı betik/CSV düzenleme uyarısı, eşitlikte sıralama sızıntı uyarısı, push öncesi kontrol hatırlatması, bota kapalı sitelere (agftablosu, agftahmin, liderform) istek **engeli**.

## task-observer (oturum gözlemleri → skill iyileştirmeleri)
Skill: `.claude/skills/task-observer/` (CC-BY-4.0, kaynak rebelytics/one-skill-to-rule-them-all). Gözlemler `skill-observations/` içinde (çalışma kökü `/home/user/at-yarisi`, skill `skill-observations/` alt klasörünü kendisi ekler), **her oturum sonunda commit+push** edilir (public repo: kişisel bilgi/anahtar yazma). Yanıtlarda gözlem raporu **tek satır**, laf kalabalığı yok. Aktivasyon `SessionStart` kancasıyla da zorlanır (`.claude/hooks/task-observer-start.sh`, `.claude/settings.json`); sorun çıkarsa `settings.json`'dan `hooks` bölümünü silmek yeter.

```text
(task-observer activation block — template of v3.12.0)
Before the first tool call of any session, the first turn after a
compaction included, and before writing or proposing a plan, invoke the
task-observer skill AND run its Session Start Protocol: loading alone
activates nothing, and a harness note not to re-execute earlier skills does
not cover this protocol. The first call is one batch: an `ls` of the
workspace path below, the skill load and its per-skill lookup. A host that
requires its plan call first puts it in that batch, the protocol as its
first item, revised after the scan. Every turn with a tool call counts,
however simple it looks. Report a step you did not run in one line before
the answer when the user can act on it; every skipped step is recorded in
session-starts.log, which the user can read. If the skill does not resolve,
tell the user in your first reply, never only in a log, naming the probe
(the skill listing, or the directory on disk); re-check the listing on
every later turn with a tool call and run the protocol the first time it
resolves. On disk but unlisted, or refused ("Unknown skill"): read its
SKILL.md directly and run the protocol; that is the activation, said once.

After each task, list this session's observation records and append, in the
same turn, a one-line summary of that listing to checkpoints.log (ids and
titles, or "none logged" plus one line per user correction and per
incident, each with why it is not an observation), never from memory. The
reply names what was logged, or says nothing was logged, in one line;
details are in checkpoints.log. It catches a skill that never ran.

The task-observer workspace for this project is:
  /home/user/at-yarisi
Every path the skill uses derives from that root, never from the working
directory. A subagent dispatched by a session that runs this protocol does
not run it and does not write to the log; it reports its findings to its
caller.
```

```text
The user's repositories live under:
  /home/user
Runs that cannot write here or get an approval answered write their output to:
  none
Findings about these skills also arrive through:
  none
```
