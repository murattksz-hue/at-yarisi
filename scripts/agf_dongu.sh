#!/bin/bash
# Koşu günü AGF + ganyan kaydı: 5 dakikada bir, İstanbul saatiyle 22:15'e kadar. Kilit dosyasıyla tek kopya çalışır.
K="$(cd "$(dirname "$0")/.." && pwd)"; KILIT=/tmp/agf_dongu.kilit
if [ -f "$KILIT" ] && kill -0 "$(cat $KILIT)" 2>/dev/null; then echo "döngü zaten çalışıyor (pid $(cat $KILIT))"; exit 0; fi
echo $$ > "$KILIT"
while true; do
  saat=$(TZ=Europe/Istanbul date +%H%M)
  [ "$saat" -gt 2215 ] && break
  python3 -I "$K/scripts/agf_kayit.py" >> "$K/.gunluk/agf_dongu.log" 2>&1
  # beygir.com muhtemelleri: 15 dakikada bir (siteyi yormamak için)
  [ $(( 10#$(TZ=Europe/Istanbul date +%M) % 15 )) -lt 5 ] && python3 -I "$K/scripts/muhtemel_kayit.py" >> "$K/.gunluk/agf_dongu.log" 2>&1
  # her kayıttan sonra GitHub'a kaydet (model turu gerektirmez)
  (cd "$K" && git add -A veri/agf_kayit veri/muhtemel_kayit && git commit -q -m "AGF/ganyan kaydı (otomatik)" >/dev/null 2>&1 && git -c push.negotiate=true push -q >/dev/null 2>&1)
  sleep 300
done
# gün sonu: kayıtları GitHub'a kaydet (model turu gerektirmez)
cd "$K" && git add -A veri/agf_kayit veri/muhtemel_kayit && git commit -q -m "AGF/ganyan kaydı (gün sonu, otomatik)" >/dev/null 2>&1; for i in 1 2 3 4; do git -c push.negotiate=true push -q >/dev/null 2>&1 && break; sleep $((i*15)); done
rm -f "$KILIT"; echo "döngü bitti $(date)" >> "$K/.gunluk/agf_dongu.log"
