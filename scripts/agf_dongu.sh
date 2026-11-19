#!/bin/bash
# Koşu günü AGF + ganyan kaydı: 10 dakikada bir, İstanbul saatiyle 22:15'e kadar. Kilit dosyasıyla tek kopya çalışır.
K="$(cd "$(dirname "$0")/.." && pwd)"; KILIT=/tmp/agf_dongu.kilit
if [ -f "$KILIT" ] && kill -0 "$(cat $KILIT)" 2>/dev/null; then echo "döngü zaten çalışıyor (pid $(cat $KILIT))"; exit 0; fi
echo $$ > "$KILIT"
while true; do
  saat=$(TZ=Europe/Istanbul date +%H%M)
  [ "$saat" -gt 2215 ] && break
  python3 -I "$K/scripts/agf_kayit.py" >> "$K/.gunluk/agf_dongu.log" 2>&1
  sleep 600
done
rm -f "$KILIT"; echo "döngü bitti $(date)" >> "$K/.gunluk/agf_dongu.log"
