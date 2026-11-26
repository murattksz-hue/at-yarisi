---
name: uyar-canli-betik
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: scripts/(agf_plan|agf_kayit|agf_tam|agf_sonrasi_analiz|gunluk|canli_takip|para_takip|kazanan_profil|tahmin_10dk|son_dakika_ozet)\.py$|\.github/workflows/kayit\.yml$
---

⚠️ **Canlı sistem dosyası düzenleniyor.**

- Kullanıcı onayı aldın mı? (canlı kayıt/tahmin akışı)
- Değiştirdikten sonra sahte saatle dene: `PLAN_DENEME=1 PLAN_SIMDI=2026-..T..:..:00 python3 -I scripts/agf_plan.py`
- Push'tan önce tüm betikleri `ast.parse` ile kontrol et, `pytest tests -q` çalıştır.
