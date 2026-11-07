#!/usr/bin/env python3
"""Δύο ΔΟΚΙΜΑΣΤΙΚΕΣ εκδοχές της αρχικής με το σλόγκαν (7/11/2026) — ΜΟΝΟ για τη δοκιμαστική διεύθυνση.

  Εκδοχή 1: το σλόγκαν «Ο φόβος φεύγει όταν το χειρότερο έχει νούμερο.» γίνεται ο μεγάλος τίτλος·
            ο σημερινός τίτλος κατεβαίνει στη μικρή γραμμή από κάτω.
  Εκδοχή 2: ο τίτλος μένει ίδιος· το σλόγκαν μπαίνει ως «υπογραφή» δίπλα στο σήμα Β
            (κορυφή, κλείσιμο σελίδας, κάτω μέρος).

Και οι δύο: σήμα Β δίπλα στο όνομα, το κουμπί μένει «Κλείσε μια συζήτηση» (δεν ξαναλέει το σλόγκαν),
και ένα μικρό κουμπάκι κάτω αριστερά για εναλλαγή εκδοχής.

Διαβάζει το standalone_v4.html ΧΩΡΙΣ να το αλλάξει. Το ζωντανό site δεν αγγίζεται.
Χρήση:  python3 tools/marka_ekdoxes.py <φάκελος εξόδου>   → index.html (εκδοχή 1) + ekdoxi-2.html
"""
import pathlib
import sys

SRC = pathlib.Path(__file__).resolve().parent.parent / "standalone_v4.html"
SLOGAN_EL = "Ο φόβος φεύγει όταν το χειρότερο έχει νούμερο."
SLOGAN_EN = "Fear fades when the worst case has a number."

# Σήμα Β: το κάτω μισό (το δίχτυ) μεγαλύτερο και σε χρώμα — ίδιο με brand/gyros-3.html
def mark(size, gid, ink="currentColor"):
    return (
        f'<svg class="b-mark" width="{size}" height="{size}" viewBox="0 0 120 120" aria-hidden="true">'
        f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7c5cff"/>'
        f'<stop offset=".55" stop-color="#ff6b4a"/><stop offset="1" stop-color="#f2b544"/></linearGradient></defs>'
        f'<g fill="none" stroke-width="14" stroke-linecap="round" stroke-linejoin="round">'
        f'<path d="M32 14V106" stroke="{ink}"/><path d="M32 14H58A20 20 0 0 1 58 54H32" stroke="{ink}"/>'
        f'<path d="M32 54H64A26 26 0 0 1 64 106H32" stroke="url(#{gid})"/></g></svg>'
    )


def rep(h, old, new):
    n = h.count(old)
    assert n == 1, f"βρέθηκε {n} φορές: {old[:70]!r}"
    return h.replace(old, new)


PAINT = ('<span class="paint">{w}<svg viewBox="0 0 400 40" preserveAspectRatio="none" aria-hidden="true">'
         '<path d="M6 26 C 90 8, 210 6, 394 20" stroke="#f2b544" stroke-width="22" stroke-linecap="round" '
         'fill="none" pathLength="1000"/></svg></span>')

COMMON_CSS = """
/* ── ΔΟΚΙΜΗ ΜΑΡΚΑΣ 7/11/2026 (μόνο στη δοκιμαστική) ── */
.brand .b-mark { flex: none; margin-right: 10px; }
.footer-slogan { display:block; margin-top:10px; font-family: Manrope, Inter, sans-serif; font-weight: 800;
  font-size: 17px; letter-spacing: -0.02em; color: inherit; margin-bottom: 6px; }
.ekdoxi-switch { position: fixed; left: 14px; bottom: 14px; z-index: 9999; display: flex; gap: 4px; align-items: center;
  background: #121414; color: #fff; border-radius: 99px; padding: 5px; font: 600 12.5px Inter, sans-serif;
  box-shadow: 0 10px 24px rgba(0,0,0,.25); }
.ekdoxi-switch span { padding: 0 8px 0 10px; opacity: .7; }
.ekdoxi-switch a { color: #fff; text-decoration: none; padding: 7px 12px; border-radius: 99px; }
.ekdoxi-switch a[aria-current] { background: #fff; color: #121414; }
@media (max-width: 640px) { .brand .b-mark { width: 22px; height: 22px; margin-right: 6px; }
  .brand { font-size: 19px !important; } .site-header { gap: 8px !important; } .nav-toggle { flex: none; } .ekdoxi-switch span { display: none; } }
"""

V2_CSS = """
.brand .brand-text { display: flex; flex-direction: column; line-height: 1.05; }
.brand .brand-slogan { font: 600 12.5px Inter, sans-serif; letter-spacing: 0; color: var(--muted, #5d6462); margin-top: 3px; }
@media (max-width: 1280px) { .brand .brand-slogan { display: none; } }
.slogan-band { position: relative; margin: 0 clamp(16px, 4vw, 56px) 72px; border-radius: 32px; background: #1d1b4f; color: #fff;
  padding: clamp(36px, 6vw, 80px) clamp(24px, 6vw, 88px); display: flex; align-items: center; gap: clamp(20px, 4vw, 56px); }
.slogan-band .b-mark { flex: none; width: clamp(72px, 9vw, 132px); height: auto; }
.slogan-band p { margin: 0; font-family: Manrope, Inter, sans-serif; font-weight: 800; letter-spacing: -0.04em; line-height: 1.04;
  font-size: clamp(32px, 4.6vw, 68px); max-width: 18ch; }
.slogan-band p em { font-style: normal; background: linear-gradient(90deg, #f2b544, #ff6b4a); -webkit-background-clip: text;
  background-clip: text; color: transparent; }
@media (max-width: 640px) { .slogan-band { flex-direction: column; align-items: flex-start; border-radius: 24px; } }
"""


def build(h, which):
    # Κοινά: σήμα Β δίπλα στο όνομα, σλόγκαν στο κάτω μέρος, κουμπάκι εναλλαγής.
    h = rep(h, "    </style>\n  </head>", COMMON_CSS + (V2_CSS if which == 2 else "") + "    </style>\n  </head>")
    if which == 1:
        h = rep(h, '<a class="brand" href="#top" aria-label="Homepage">',
                '<a class="brand" href="#top" aria-label="Homepage">' + mark(30, "bgN"))
    else:
        h = rep(h, '<a class="brand" href="#top" aria-label="Homepage"><span data-i18n="v4Brand">Γιάννης Βαρδαβάς</span><small>lutcf</small></a>',
                '<a class="brand" href="#top" aria-label="Homepage">' + mark(34, "bgN")
                + '<span class="brand-text"><span><span data-i18n="v4Brand">Γιάννης Βαρδαβάς</span><small>lutcf</small></span>'
                + '<span class="brand-slogan" data-i18n="v4Slogan">' + SLOGAN_EL + '</span></span></a>')
    h = rep(h, '<span class="footer-name" data-i18n="footerName">Γιάννης Βαρδαβάς, lutcf</span>',
            '<span class="footer-name" data-i18n="footerName">Γιάννης Βαρδαβάς, lutcf</span>'
            '<span class="footer-slogan" data-i18n="v4Slogan">' + SLOGAN_EL + '</span>')
    # νέο κλειδί μετάφρασης (αλλιώς η αλλαγή γλώσσας γράφει «undefined»)
    h = rep(h, '    v4Brand: "Γιάννης Βαρδαβάς",', f'    v4Brand: "Γιάννης Βαρδαβάς",\n    v4Slogan: "{SLOGAN_EL}",')
    h = rep(h, '    v4Brand: "Ioannis Vardavas",', f'    v4Brand: "Ioannis Vardavas",\n    v4Slogan: "{SLOGAN_EN}",')

    if which == 1:
        t_el = ('<span class="h-line">Ο φόβος φεύγει όταν</span><span class="h-line">το χειρότερο έχει '
                + PAINT.format(w="νούμερο") + '.</span>')
        h = rep(h, '<h1 id="hero-title" data-i18n="v4HeroTitle"><span class="h-line">Το οικονομικό σου σχέδιο,</span><span class="h-line">'
                + PAINT.format(w="δοκιμασμένο") + ' πριν το χρειαστείς.</span></h1>',
                '<h1 id="hero-title" data-i18n="v4HeroTitle">' + t_el + '</h1>')
        h = rep(h, """    v4HeroTitle: '<span class="h-line">Το οικονομικό σου σχέδιο,</span><span class="h-line">' + paint("δοκιμασμένο") + " πριν το χρειαστείς.</span>",""",
                """    v4HeroTitle: '<span class="h-line">Ο φόβος φεύγει όταν</span><span class="h-line">το χειρότερο έχει ' + paint("νούμερο") + ".</span>",""")
        h = rep(h, """    v4HeroTitle: '<span class="h-line">Your financial plan,</span><span class="h-line">' + paint("tested") + " before you need it.</span>",""",
                """    v4HeroTitle: '<span class="h-line">Fear fades when</span><span class="h-line">the worst case has ' + paint("a number") + ".</span>",""")
        # Η μικρή γραμμή: ο παλιός τίτλος + τι κάνεις (χωρίς να ξαναλέει «νούμερα»)
        lead_el = ("<b>Το οικονομικό σου σχέδιο, δοκιμασμένο πριν το χρειαστείς.</b> Ασφάλιση, σύνταξη, επενδύσεις και "
                   "κίνδυνοι για οικογένειες και επιχειρήσεις, σε μία καθαρή εικόνα. Χωρίς ψιλά γράμματα, χωρίς πίεση.")
        lead_en = ("<b>Your financial plan, tested before you need it.</b> Insurance, retirement, investments and risk "
                   "for families and businesses, in one clear picture. No fine print, no pressure.")
        h = rep(h, '<p class="lead" data-i18n="v4Lead">Για οικογένειες και επιχειρήσεις: ασφάλιση, σύνταξη, επενδύσεις και κίνδυνοι σε μία καθαρή εικόνα, με πραγματικά νούμερα. Χωρίς ψιλά γράμματα, χωρίς πίεση.</p>',
                f'<p class="lead" data-i18n="v4Lead">{lead_el}</p>')
        h = rep(h, '    v4Lead: "Για οικογένειες και επιχειρήσεις: ασφάλιση, σύνταξη, επενδύσεις και κίνδυνοι σε μία καθαρή εικόνα, με πραγματικά νούμερα. Χωρίς ψιλά γράμματα, χωρίς πίεση.",',
                f'    v4Lead: "{lead_el}",')
        h = rep(h, '    v4Lead: "For families and businesses: insurance, retirement, investments and risk in one clear picture, with real numbers. No fine print, no pressure.",',
                f'    v4Lead: "{lead_en}",')
    else:
        band = ('      <section class="slogan-band" aria-label="Σλόγκαν">' + mark(132, "bgBand", "#fff")
                + '<p>Ο φόβος φεύγει όταν το χειρότερο <em>έχει νούμερο.</em></p></section>\n')
        h = rep(h, "    </main>\n\n    <footer class=\"site-footer\">", band + "    </main>\n\n    <footer class=\"site-footer\">")

    links =(('<a href="./" aria-current="page">Εκδοχή 1</a><a href="ekdoxi-2.html">Εκδοχή 2</a>') if which == 1
             else ('<a href="./">Εκδοχή 1</a><a href="ekdoxi-2.html" aria-current="page">Εκδοχή 2</a>'))
    sw =f'\n    <nav class="ekdoxi-switch" aria-label="Δοκιμή μάρκας"><span>Δοκιμή μάρκας</span>{links}</nav>\n  </body>'
    h = rep(h, "\n</body>", sw.replace("\n  </body>", "\n</body>"))
    return h


def main():
    out = pathlib.Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    src = SRC.read_text(encoding="utf-8")
    (out / "index.html").write_text(build(src, 1), encoding="utf-8")
    (out / "ekdoxi-2.html").write_text(build(src, 2), encoding="utf-8")
    print("ok:", out / "index.html", out / "ekdoxi-2.html")


if __name__ == "__main__":
    main()
