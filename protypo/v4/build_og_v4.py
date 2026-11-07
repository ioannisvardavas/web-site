#!/usr/bin/env python3
"""og_card.html -> og-image-v7.jpg: η κάρτα του συνδέσμου σε WhatsApp/Viber, με τη μάρκα (7/11/2026).

Η φωτογραφία είναι η ίδια με του site (το avatar του hero στο standalone.html).
Το Chrome τη «φωτογραφίζει» σε 1200×630 και βγαίνει JPEG < 300 KB — πάνω από αυτό
το WhatsApp δείχνει μόνο μικρό εικονίδιο. Νέο όνομα αρχείου σε κάθε αλλαγή εμφάνισης,
αλλιώς WhatsApp/Viber κρατούν την παλιά εικόνα στη μνήμη τους.

Τρέξιμο:  /usr/bin/python3 protypo/v4/build_og_v4.py [a|b] [--dokimi φάκελος]
          a/b = εκδοχή (βλ. og_card.html)· χωρίς --dokimi γράφει og-image-v7.jpg στη ρίζα + deploy/,
          με --dokimi γράφει og-a.jpg / og-b.jpg εκεί για σύγκριση.
"""
import pathlib, re, subprocess, sys, tempfile
from PIL import Image

ROOT = pathlib.Path("/Users/user/Desktop/Claude dir/Web Site")
SCR = pathlib.Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = "og-image-v7.jpg"
args = sys.argv[1:]
VARIANT = args[0] if args and args[0] in ("a", "b") else "b"  # Β = επιλογή Γιάννη 7/11/2026
DOKIMI = pathlib.Path(args[args.index("--dokimi") + 1]) if "--dokimi" in args else None

def b_mark(gid, ink):
    """Σήμα Β — ίδιο με το b_mark() του build_v4.py."""
    return (
        f'<svg viewBox="0 0 120 120" aria-hidden="true">'
        f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7c5cff"/>'
        f'<stop offset=".55" stop-color="#ff6b4a"/><stop offset="1" stop-color="#f2b544"/></linearGradient></defs>'
        f'<g fill="none" stroke-width="14" stroke-linecap="round" stroke-linejoin="round">'
        f'<path d="M32 14V106" stroke="{ink}"/><path d="M32 14H58A20 20 0 0 1 58 54H32" stroke="{ink}"/>'
        f'<path d="M32 54H64A26 26 0 0 1 64 106H32" stroke="url(#{gid})"/></g></svg>'
    )
MAX_KB = 300

src = (ROOT / "standalone.html").read_text(encoding="utf-8")
i = src.index('<section class="hero" aria-labelledby="hero-title">')
avatar = re.search(r'src="(data:[^"]+)"', src[i:src.index("</section>", i)]).group(1)

html = (SCR / "og_card.html").read_text(encoding="utf-8")
for k in ("__AVATAR__", "__VARIANT__", "__BMARK_INK__", "__BMARK_WHITE__"):
    assert html.count(k) == 1, k
html = (html.replace("__VARIANT__", VARIANT)
            .replace("__BMARK_INK__", b_mark("gTag", "#121414"))
            .replace("__BMARK_WHITE__", b_mark("gBand", "#fff")))
tmp_html = SCR / "_og_render.html"  # δίπλα στο πρότυπο, ώστε να βρει τις γραμματοσειρές
tmp_html.write_text(html.replace("__AVATAR__", avatar), encoding="utf-8")

try:
    with tempfile.TemporaryDirectory() as td:
        png = pathlib.Path(td) / "og.png"
        subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
             "--force-device-scale-factor=1", "--window-size=1200,630",
             "--virtual-time-budget=3000", f"--user-data-dir={td}/prof",
             f"--screenshot={png}", tmp_html.as_uri()],
            check=True, capture_output=True,
        )
        img = Image.open(png).convert("RGB")
        assert img.size == (1200, 630), img.size
        dests = [DOKIMI / f"og-{VARIANT}.jpg"] if DOKIMI else [ROOT / OUT, ROOT / "deploy" / OUT]
        for dest in dests:
            img.save(dest, "JPEG", quality=88, optimize=True, progressive=True)
finally:
    tmp_html.unlink(missing_ok=True)

out = dests[0]
kb = out.stat().st_size / 1024
assert kb < MAX_KB, f"{kb:.0f} KB — το WhatsApp θα δείξει μόνο μικρό εικονίδιο"
print(f"OK  {out}  εκδοχή {VARIANT}  1200×630  {kb:.0f} KB")
