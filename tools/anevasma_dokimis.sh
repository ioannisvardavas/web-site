#!/bin/bash
# Ανεβάζει τη δοκιμαστική νέα μορφή (standalone_v4.html + νέο ραντάρ) στο
# https://vardavas-dokimi.pages.dev — ξεχωριστό project, ΔΕΝ αγγίζει το ζωντανό site.
# Το ραντάρ παίρνεται από τον διπλανό φάκελο risk-radar, όπως είναι τώρα (branch restyle-v4).
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="$(mktemp -d)/v4-dokimi"
mkdir -p "$OUT/risk-radar"
cp -R deploy/assets deploy/paixnidia deploy/og-image-v2.png "$OUT/"
rsync -a --exclude .git --exclude .claude --exclude worker --exclude README.md \
  --exclude .DS_Store --exclude .gitignore ../risk-radar/ "$OUT/risk-radar/"
python3 - "$OUT" <<'EOF'
import sys, pathlib
out = pathlib.Path(sys.argv[1])
h = pathlib.Path("standalone_v4.html").read_text()
assert h.count("https://risk-radar-2yr.pages.dev") >= 1
(out / "index.html").write_text(h.replace("https://risk-radar-2yr.pages.dev", "/risk-radar"))
# Τα «πίσω στην ιστοσελίδα» του ραντάρ και των παιχνιδιών μένουν μέσα στη δοκιμή.
r = out / "risk-radar/index.html"
t = r.read_text()
assert t.count('href="https://vardavas-site.pages.dev"') == 1
r.write_text(t.replace('href="https://vardavas-site.pages.dev"', 'href="/"'))
for p in (out / "paixnidia").glob("*.html"):
    p.write_text(p.read_text().replace('href="https://vardavas-site.pages.dev/"', 'href="/"'))
EOF
printf '/*\n  X-Robots-Tag: noindex, nofollow\n' > "$OUT/_headers"
npx wrangler pages deploy "$OUT" --project-name=vardavas-dokimi --branch=main --commit-dirty=true
