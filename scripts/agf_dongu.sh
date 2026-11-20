#!/bin/bash
# Koşu günü kayıt planı (scripts/agf_plan.py): 09:25–10:30 ilk AGF'ye kadar 5 dk'da bir, 12:00, her koşudan 1 saat önce,
# her koşudan sonra sonuç kontrolü. Her dakika plan kontrol edilir; zamanı gelen iş bir kez yapılır. Kilit dosyasıyla tek kopya.
K="$(cd "$(dirname "$0")/.." && pwd)"; KILIT=/tmp/agf_dongu.kilit
if [ -f "$KILIT" ] && kill -0 "$(cat $KILIT)" 2>/dev/null; then echo "döngü zaten çalışıyor (pid $(cat $KILIT))"; exit 0; fi
echo $$ > "$KILIT"
while true; do
  python3 -I "$K/scripts/agf_plan.py" >> "$K/.gunluk/agf_dongu.log" 2>&1; kod=$?
  (cd "$K" && git add -A veri/agf_kayit veri/muhtemel_kayit veri/tahminler veri/canli_takip*.csv veri/para_takip.csv analizler && git commit -q -m "AGF/ganyan kaydı (otomatik)" >/dev/null 2>&1 && git -c push.negotiate=true push -q >/dev/null 2>&1)
  [ "$kod" -eq 3 ] && break
  [ "$(TZ=Europe/Istanbul date +%H%M)" -gt 2330 ] && break
  sleep 60
done
cd "$K" && for i in 1 2 3 4; do git -c push.negotiate=true push -q >/dev/null 2>&1 && break; sleep $((i*15)); done
rm -f "$KILIT"; echo "döngü bitti $(date)" >> "$K/.gunluk/agf_dongu.log"
