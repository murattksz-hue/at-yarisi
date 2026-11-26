---
name: uyar-esitlikte-sira
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: scripts/.*\.py$
  - field: new_text
    operator: regex_match
    pattern: argsort\(\)\.argsort\(\)|sorted\(range\(len
---

🔍 **Sıralama hesabı: eşitlikte sızıntı riski!**

Sonuç/at_gecmisi satırları BİTİŞ SIRASINA göre dizili. `argsort().argsort()` veya `sorted(...)` ile sıra hesaplarsan eşitlikte kazanan öne geçer (26.11.2026 HP sırası hatası).
Doğrusu: sıra = 1 + (değeri kesin büyük olan sayısı). Çok güzel sonuç çıkarsa önce sızıntı ara.
