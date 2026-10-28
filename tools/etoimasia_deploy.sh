#!/bin/bash
# Ετοιμάζει τον φάκελο deploy/ — ΔΕΝ ανεβάζει τίποτα μόνο του.
# Το ανέβασμα γίνεται μόνο με ρητή εντολή, με την τελευταία γραμμή που τυπώνει.
set -e
cd "$(dirname "$0")/.."

python3 tools/sync_paixnidia.py

# Από το go-live (28/10/2026) το ζωντανό site είναι η ΝΕΑ ΜΟΡΦΗ.
# Το standalone.html παραμένει η πηγή του ΠΕΡΙΕΧΟΜΕΝΟΥ (κείμενα, αριθμομηχανή,
# παράθυρα)· το ύφος ζει στο protypo/v4/ και παράγει το standalone_v4.html.
# Άρα: αλλαγή κειμένου -> standalone.html· αλλαγή ύφους -> protypo/v4/.
python3 protypo/v4/build_v4.py

cp standalone_v4.html index.html      # ώστε να ανοίγει σωστά και με διπλό κλικ, τοπικά
cp standalone_v4.html deploy/index.html
rm -rf deploy/paixnidia
cp -r paixnidia deploy/paixnidia
mkdir -p deploy/assets && cp -r assets/. deploy/assets/ 2>/dev/null || true

echo ""
echo "✓ Ο φάκελος deploy/ είναι έτοιμος."
echo "  Για να βγει ζωντανά:"
echo "  npx wrangler pages deploy deploy/ --project-name=vardavas-site --commit-dirty=true"
