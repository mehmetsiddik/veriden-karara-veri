#!/usr/bin/env bash
# Veri setlerini yeniden üretir ve bütün analizleri çalıştırır.
# Deponun ana klasöründen çalıştırınız:  bash calistir.sh
set -e
cd "$(dirname "$0")"
mkdir -p kod/sonuclar figures/data
python3 kod/01_veri_uret.py
python3 kod/fig_b01.py
for f in kod/b*.py kod/cozumler.py; do
  ad=$(basename "$f" .py)
  echo "Çalıştırılıyor: $ad"
  python3 -W ignore "$f" > "kod/sonuclar/$ad.txt"
done
echo "Tamamlandı. Çıktılar kod/sonuclar/ klasöründedir."
