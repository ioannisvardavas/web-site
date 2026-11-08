#!/usr/bin/env python3
"""linkedin_cover.html -> εξώφυλλο προφίλ LinkedIn (8/11/2026), στο ύφος της κάρτας του link.

Βγαίνει 1584×396 (το μέγεθος που ζητά το LinkedIn — ανεβαίνει χωρίς κόψιμο) σε PNG,
στον φάκελο της μάρκας (~/Desktop/brand/eikones/) — ΟΧΙ στο site.
Ελέγχει ότι η στρογγυλή φωτογραφία προφίλ (υπολογιστής/κινητό) δεν σκεπάζει γράμματα·
με --elegxos <αρχείο.png> γράφει και εικόνα με τους κύκλους σχεδιασμένους, για να το δεις.

Τρέξιμο:  /usr/bin/python3 protypo/v4/build_linkedin_v4.py [--elegxos <αρχείο.png>]
"""
import pathlib, subprocess, sys, tempfile
from PIL import Image, ImageDraw

SCR = pathlib.Path(__file__).parent
sys.path.insert(0, str(SCR))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT_DIR = pathlib.Path.home() / "Desktop" / "brand" / "eikones"
OUT = OUT_DIR / "linkedin-exofyllo.png"
args = sys.argv[1:]
CHECK = pathlib.Path(args[args.index("--elegxos") + 1]) if "--elegxos" in args else None
W, H = 1584, 396
MAX_MB = 8  # όριο LinkedIn

def b_mark(gid, ink):
    """Σήμα Β — ίδιο με το b_mark() του build_v4.py / build_og_v4.py."""
    return (
        f'<svg viewBox="0 0 120 120" aria-hidden="true">'
        f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7c5cff"/>'
        f'<stop offset=".55" stop-color="#ff6b4a"/><stop offset="1" stop-color="#f2b544"/></linearGradient></defs>'
        f'<g fill="none" stroke-width="14" stroke-linecap="round" stroke-linejoin="round">'
        f'<path d="M32 14V106" stroke="{ink}"/><path d="M32 14H58A20 20 0 0 1 58 54H32" stroke="{ink}"/>'
        f'<path d="M32 54H64A26 26 0 0 1 64 106H32" stroke="url(#{gid})"/></g></svg>'
    )

html = (SCR / "linkedin_cover.html").read_text(encoding="utf-8")
assert html.count("__BMARK_WHITE__") == 1
tmp_html = SCR / "_linkedin_render.html"  # δίπλα στο πρότυπο, ώστε να βρει τις γραμματοσειρές
tmp_html.write_text(html.replace("__BMARK_WHITE__", b_mark("gCover", "#fff")), encoding="utf-8")

try:
    with tempfile.TemporaryDirectory() as td:
        png = pathlib.Path(td) / "cover.png"
        subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
             "--force-device-scale-factor=1", f"--window-size={W},{H}",
             "--virtual-time-budget=3000", f"--user-data-dir={td}/prof",
             f"--screenshot={png}", tmp_html.as_uri()],
            check=True, capture_output=True,
        )
        img = Image.open(png).convert("RGB")
        assert img.size == (W, H), img.size
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        img.save(OUT, "PNG", optimize=True)
finally:
    tmp_html.unlink(missing_ok=True)

mb = OUT.stat().st_size / 1024 / 1024
assert mb < MAX_MB, f"{mb:.1f} MB — το LinkedIn δέχεται έως {MAX_MB} MB"

# Έλεγχος: πού πέφτει η φωτογραφία προφίλ.
# Υπολογιστής: κάρτα προφίλ ~804px, εξώφυλλο 804×201, φωτογραφία 152px, 24px από αριστερά,
# κέντρο ~30px πάνω από τη βάση του εξωφύλλου → ×1.97 σε pixel εξωφύλλου.
# Κινητό (Android): εξώφυλλο σε όλο το πλάτος, φωτογραφία ~ 26% του πλάτους, 16px από αριστερά.
chk = img.copy()
d = ImageDraw.Draw(chk, "RGBA")
s = W / 804
r = 76 * s; cx = (24 + 76) * s; cy = H - 30 * s
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255, 230), width=4, fill=(255, 255, 255, 60))
m = W / 412  # κινητό 412px πλάτος
rm = 54 * m; cxm = (16 + 54) * m; cym = H - 6 * m
d.ellipse([cxm - rm, cym - rm, cxm + rm, cym + rm], outline=(255, 210, 0, 230), width=4)
d.text((20, 16), "white = profile photo on desktop / yellow = on phone (approx.)", fill=(255, 255, 255, 220))
if CHECK:
    chk.save(CHECK, "PNG")

right_edge_photo = max(cx + r, cxm + rm)
print(f"OK  {OUT}  {W}×{H}  {mb*1024:.0f} KB")
print(f"φωτογραφία προφίλ φτάνει ως x≈{right_edge_photo:.0f} · τα γράμματα ξεκινούν x=560")
assert right_edge_photo < 560, "η φωτογραφία προφίλ σκεπάζει το σήμα/κείμενο"
