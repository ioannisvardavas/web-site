#!/bin/bash
# Ανεβάζει τη δοκιμαστική σελίδα (πρόταση 4) + παιχνίδια + το ΝΕΟ ραντάρ (branch restyle-v4)
# σε ξεχωριστή διεύθυνση δοκιμής — ΔΕΝ αγγίζει το ζωντανό vardavas-site ούτε το ζωντανό ραντάρ.
#   https://vardavas-v4-dokimi.ioannis-vardavas.workers.dev
# Όλη η διεύθυνση έχει noindex (δεν μπαίνει στη Google).
set -euo pipefail
cd "$(dirname "$0")/.."
SITE="$PWD"; RADAR="$SITE/../risk-radar"
D="$(mktemp -d)/dokimi_v4"; mkdir -p "$D/risk-radar"

python3 protypo/v4/build_v4.py
cp standalone_v4.html "$D/index.html"
cp -R assets paixnidia "$D/"
cp deploy/og-image*.png "$D/"
rsync -a --exclude .git --exclude worker --exclude README.md --exclude node_modules --exclude '.*' "$RADAR/" "$D/risk-radar/"
# Το «← Στην ιστοσελίδα μου» του ραντάρ γυρνά στη δοκιμαστική σελίδα, όχι στο ζωντανό site.
grep -rl "https://vardavas-site.pages.dev" "$D/risk-radar" --include='*.html' | while read -r f; do
  sed -i '' 's#https://vardavas-site.pages.dev#/#g' "$f"
done
printf '/*\n  X-Robots-Tag: noindex, nofollow\n' > "$D/_headers"

echo "ραντάρ από branch: $(git -C "$RADAR" branch --show-current)"
npx --yes wrangler deploy --name vardavas-v4-dokimi --assets "$D" --compatibility-date 2026-10-23
