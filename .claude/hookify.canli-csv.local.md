---
name: uyar-canli-csv
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: veri/(para_takip|kazanan_profil|canli_takip.*)\.csv$
---

⚠️ **Actions'ın yazdığı canlı CSV.** Elle yazmak push çakışması yaratır (20.11'de oldu). Kullanıcı onayı ve hızlı fetch+merge+push gerekir.
