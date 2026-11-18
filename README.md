# at-yarisi

Türkiye at yarışları (TJK) için notlar ve analiz araçları.

- `BILGI.md`: program sütunları, koşu türleri, bahis türleri, analiz çerçevesi
- `analiz.py`: TJK günlük program CSV'sini okuyup her koşudaki atları sıralar

## Kullanım

```bash
curl -o ist.csv "https://medya-cdn.tjk.org/raporftp/TJKPDF/2026/2026-11-18/CSV/GunlukYarisProgrami/18.11.2026-%C4%B0stanbul-GunlukYarisProgrami-TR.csv"
python3 analiz.py ist.csv
```

Skor: HP %40, s20 %30, son 6 koşu %30. Zemin, mesafe ve kilo henüz modelde yok.
