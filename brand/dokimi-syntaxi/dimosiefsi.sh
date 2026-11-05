#!/bin/bash
# Φτιάχνει τον φάκελο «dimosiefsi/»: ΑΥΤΟΤΕΛΗ εκδοχή της δοκιμής μάρκας (όλα τα αρχεία μέσα,
# χωρίς «../»), για να ανέβει ως ιδιωτικός σύνδεσμος. Ανοίγει κατευθείαν στους «Κανόνες μελέτης».
# Προϋπόθεση: έχει τρέξει πρώτα το ftiakse.sh (φτιάχνει το app/).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
out="$here/dimosiefsi"
[ -f "$here/app/index.html" ] || { echo "Τρέξε πρώτα το ftiakse.sh"; exit 1; }
rm -rf "$out"; cp -R "$here/app" "$out"
mkdir -p "$out/fonts"
cp "$here/../../assets/fonts/"*.woff2 "$here/../../assets/fonts/fonts.css" "$here/../../assets/fonts/"OFL-*.txt "$out/fonts/"
cp "$here/marka.css" "$here/marka.js" "$out/"
# η Βοήθεια (στιγμιότυπα) δεν χρειάζεται για τη δοκιμή μιας οθόνης· μένει έξω για να μείνει μικρό
rm -rf "$out/voitheia" "$out/voitheia.html"
python3 - "$out/index.html" <<'PY'
import sys; p=sys.argv[1]; s=open(p,encoding='utf-8').read()
rep=[('href="../../../assets/fonts/fonts.css"','href="fonts/fonts.css"'),
     ('href="../marka.css"','href="marka.css"'),
     ('<script src="../marka.js" defer>','<script src="marka.js" data-othoni="Κανόνες μελέτης" defer>'),
     ('<title>Μελέτη Συνταξιοδοτικού Προγραμματισμού</title>','<title>Δοκιμή μάρκας Σύνταξη</title>')]
for a,b in rep:
    assert s.count(a)==1, a; s=s.replace(a,b,1)
open(p,'w',encoding='utf-8').write(s)
PY
echo "Έτοιμο: $out ($(find "$out" -type f | wc -l | tr -d ' ') αρχεία, $(du -sh "$out" | cut -f1))"
