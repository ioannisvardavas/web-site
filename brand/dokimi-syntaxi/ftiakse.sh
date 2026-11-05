#!/bin/bash
# Φτιάχνει ΑΝΤΙΓΡΑΦΟ της Μελέτης Σύνταξης με το στρώμα της μάρκας από πάνω.
# Την πραγματική εφαρμογή (~/Desktop/PENSION) ΔΕΝ την αγγίζει: μόνο διαβάζει το έτοιμο build της (dist).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
src="$HOME/Desktop/PENSION/retirement-planner/dist"
[ -f "$src/index.html" ] || { echo "Δεν βρέθηκε το build της Μελέτης Σύνταξης: $src"; exit 1; }
rm -rf "$here/app"; cp -R "$src" "$here/app"
python3 - "$here/app/index.html" <<'PY'
import sys; p=sys.argv[1]; s=open(p,encoding='utf-8').read()
inj='''    <link rel="stylesheet" href="../../../assets/fonts/fonts.css">
    <link rel="stylesheet" href="../marka.css" id="marka-css">
    <script src="../marka.js" defer></script>
  </head>'''
assert s.count('</head>')==1; s=s.replace('  </head>',inj,1)
open(p,'w',encoding='utf-8').write(s)
PY
echo "Έτοιμο: $here/app/index.html"
