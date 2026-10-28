#!/usr/bin/env python3
"""og_card.html -> og-image-v5.jpg: η κάρτα του συνδέσμου σε WhatsApp/Viber, στο νέο ύφος.

Η φωτογραφία είναι η ίδια με του site (το avatar του hero στο standalone.html).
Το Chrome τη «φωτογραφίζει» σε 1200×630 και βγαίνει JPEG < 300 KB — πάνω από αυτό
το WhatsApp δείχνει μόνο μικρό εικονίδιο. Νέο όνομα αρχείου σε κάθε αλλαγή εμφάνισης,
αλλιώς WhatsApp/Viber κρατούν την παλιά εικόνα στη μνήμη τους.

Τρέξιμο:  python3 protypo/v4/build_og_v4.py   (γράφει og-image-v5.jpg στη ρίζα + deploy/)
"""
import pathlib, re, subprocess, tempfile
from PIL import Image

ROOT = pathlib.Path("/Users/user/Desktop/Claude dir/Web Site")
SCR = pathlib.Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = "og-image-v5.jpg"
MAX_KB = 300

src = (ROOT / "standalone.html").read_text(encoding="utf-8")
i = src.index('<section class="hero" aria-labelledby="hero-title">')
avatar = re.search(r'src="(data:[^"]+)"', src[i:src.index("</section>", i)]).group(1)

html = (SCR / "og_card.html").read_text(encoding="utf-8")
assert html.count("__AVATAR__") == 1
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
        for dest in (ROOT / OUT, ROOT / "deploy" / OUT):
            img.save(dest, "JPEG", quality=88, optimize=True, progressive=True)
finally:
    tmp_html.unlink(missing_ok=True)

kb = (ROOT / OUT).stat().st_size / 1024
assert kb < MAX_KB, f"{kb:.0f} KB — το WhatsApp θα δείξει μόνο μικρό εικονίδιο"
print(f"OK  {OUT}  1200×630  {kb:.0f} KB")
