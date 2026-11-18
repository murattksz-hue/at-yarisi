# at-yarisi

Türkiye at yarışları (TJK) için notlar, veri toplama ve analiz araçları. Ayrıntılar ve geri test sonuçları: `BILGI.md`.

| Dosya | Ne yapar |
|---|---|
| `scripts/sonuc_indir.py` | Son N günün TJK sonuç CSV'lerini indirir |
| `scripts/aygir_stat.py` | Sonuçlardan aygır kan istatistiği (ırk/zemin/mesafe A/E) üretir |
| `scripts/idman.py` | Günün programındaki galop (idman) bilgilerini toplar |
| `scripts/analiz2.py` | Günün programını puanlar: HP, s20, form, pist uyumu, baba ve kısrak babası kanı, galop |
| `scripts/geritest.py` | Modelleri geçmiş sonuçlarda sızıntısız karşılaştırır |
| `scripts/analiz_v1.py` | İlk basit model |
| `veri/aygir_istatistik.json` | 180 günlük aygır tablosu (18.11.2026) |

## Kullanım

```bash
python3 scripts/sonuc_indir.py veri/sonuc 180
python3 scripts/aygir_stat.py veri/sonuc veri/aygir_istatistik.json
# günün programı: tjk.org günlük program sayfası (HTML) + CSV
python3 scripts/idman.py program.html idman.json
python3 scripts/analiz2.py program.html program.csv veri/aygir_istatistik.json idman.json
```
