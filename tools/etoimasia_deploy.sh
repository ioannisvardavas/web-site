#!/bin/bash
# Ετοιμάζει τον φάκελο deploy/ — ΔΕΝ ανεβάζει τίποτα μόνο του.
# Το ανέβασμα γίνεται μόνο με ρητή εντολή, με την τελευταία γραμμή που τυπώνει.
set -e
cd "$(dirname "$0")/.."

python3 tools/sync_paixnidia.py

cp standalone.html index.html      # ώστε να ανοίγει σωστά και με διπλό κλικ, τοπικά
cp standalone.html deploy/index.html
rm -rf deploy/paixnidia
cp -r paixnidia deploy/paixnidia
mkdir -p deploy/assets && cp -r assets/. deploy/assets/ 2>/dev/null || true

echo ""
echo "✓ Ο φάκελος deploy/ είναι έτοιμος."
echo "  Για να βγει ζωντανά:"
echo "  npx wrangler pages deploy deploy/ --project-name=vardavas-site --commit-dirty=true"
