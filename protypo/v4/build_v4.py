#!/usr/bin/env python3
"""standalone.html -> standalone_v4.html: ίδιο περιεχόμενο, νέο ύφος (πρόταση 4)."""
import re, sys, pathlib

ROOT = pathlib.Path("/Users/user/Desktop/Claude dir/Web Site")
SCR = pathlib.Path(__file__).parent
src = (ROOT / "standalone.html").read_text(encoding="utf-8")
h = src


def rep(old, new, count=1):
    global h
    n = h.count(old)
    assert n == count, f"expected {count}, found {n}: {old[:80]!r}"
    h = h.replace(old, new)


def cut(start, end):
    """Return (block) between start marker and end marker inclusive."""
    i = h.index(start)
    j = h.index(end, i) + len(end)
    return i, j


CAL = "https://cal.com/ioannis-vardavas-0yon6x/30min"

# ---------- avatar data URI (μία φορά, ως CSS) ----------
hero_i, hero_j = cut('<section class="hero" aria-labelledby="hero-title">', "</section>")
hero_old = h[hero_i:hero_j]
avatar = re.search(r'src="(data:[^"]+)"', hero_old).group(1)

# ---------- head ----------
rep(
    '<meta name="theme-color" content="#0f6f6a" />',
    '<meta name="theme-color" content="#f4f1ec" />\n'
    '    <meta name="robots" content="noindex" />\n'
    '    <link rel="preconnect" href="https://fonts.googleapis.com" />\n'
    '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
    '    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&amp;family=Inter:wght@400;500;600;700&amp;display=swap" rel="stylesheet" />',
)
v4css = (SCR / "v4.css").read_text(encoding="utf-8").replace("__AVATAR__", avatar)
rep("</style>\n  </head>", "</style>\n    <style id=\"v4\">\n" + v4css + "\n    </style>\n  </head>")

# ---------- header ----------
bi, bj = cut('<a class="brand" href="#top" aria-label="Homepage">', "</a>")
h = h[:bi] + (
    '<a class="brand" href="#top" aria-label="Homepage">'
    '<span data-i18n="v4Brand">Γιάννης Βαρδαβάς</span><small>lutcf</small></a>'
) + h[bj:]

ni, nj = cut('<nav class="nav-links" id="primary-nav"', "</nav>")
h = h[:ni] + f'''<nav class="nav-links" id="primary-nav" aria-label="Main navigation">
        <a href="#arithmoi" data-i18n="v4NavNumbers">Νούμερα</a>
        <a href="#services" data-i18n="navServices">Υπηρεσίες</a>
        <a href="#method" data-i18n="navMethod">Μεθοδολογία</a>
        <a href="#games" data-i18n="v4NavGames">Παιχνίδια</a>
        <a href="#about" data-i18n="navAbout">Σχετικά</a>
        <a href="https://risk-radar-2yr.pages.dev" class="nav-risk" data-i18n="navRisk">Εργαλεία Ρίσκου →</a>
        <a href="{CAL}" class="nav-menu-cta" target="_blank" rel="noreferrer" data-i18n="v4NavCta">Κλείσε 30 λεπτά</a>
      </nav>''' + h[nj:]

rep(
    '''        <button class="lang-button" type="button" data-lang="en">EN</button>
      </div>
''',
    f'''        <button class="lang-button" type="button" data-lang="en">EN</button>
      </div>

      <a class="pill dark small nav-cta" href="{CAL}" target="_blank" rel="noreferrer" data-i18n="v4NavCta">Κλείσε 30 λεπτά</a>
''',
)

# ---------- hero ----------
hero_new = f'''<section class="hero" aria-labelledby="hero-title">
        <div class="hero-mesh" aria-hidden="true"><span class="hb hb1"></span><span class="hb hb2"></span><span class="hb hb3"></span><span class="hb hb4"></span><span class="hb hb5"></span><span class="hb hb6"></span></div>
        <div class="hero-copy">
          <a class="tag" href="#about"><span class="me-photo" aria-hidden="true"></span><span data-i18n="v4Tag">Σύμβουλος ασφαλίσεων &amp; επενδύσεων · 25 χρόνια</span><span class="tag-go" aria-hidden="true">→</span></a>
          <h1 id="hero-title" data-i18n="v4HeroTitle">Τα χρήματά σου,<br />με <span class="paint">σχέδιο.<svg viewBox="0 0 400 40" preserveAspectRatio="none" aria-hidden="true"><path d="M6 26 C 90 8, 210 6, 394 20" stroke="#f2b544" stroke-width="22" stroke-linecap="round" fill="none" pathLength="1000"/></svg></span></h1>
          <p class="lead" data-i18n="v4Lead">Ασφάλιση, σύνταξη, επενδύσεις και κίνδυνοι επιχείρησης — σε μία καθαρή εικόνα, με πραγματικά νούμερα. Χωρίς ψιλά γράμματα, χωρίς πίεση.</p>
          <div class="ctas">
            <a class="pill dark" href="{CAL}" target="_blank" rel="noreferrer" data-i18n="v4Cta1">Κλείσε μια συζήτηση</a>
            <a class="pill ghost" href="#arithmoi" data-i18n="v4Cta2">Παίξε με τα νούμερα ↓</a>
          </div>
          <div class="creds">
            <span><b data-i18n="v4Cred1b">25+ χρόνια</b><span data-i18n="v4Cred1">Τράπεζα Εργασίας → Allianz</span></span>
            <span><b>LUTCF</b><span data-i18n="v4Cred2">διεθνής πιστοποίηση</span></span>
            <span><b>177766</b><span data-i18n="v4Cred3">Αρ. Μητρώου ΕΕΑ</span></span>
          </div>
        </div>
      </section>'''

# ---------- calculator: από το modal στη σελίδα ----------
mi = h.index('<div class="tool-modal-overlay" id="toolModal" hidden>')
mj = h.index('<div class="tool-modal-overlay" id="policyModal" hidden>', mi)  # χωρίς να φάμε το επόμενο
modal = h[mi:mj]
ci = modal.index('<div class="calc-goals"')
cj = modal.index('<a class="calc-cta"')
calc_inner = modal[ci:cj]
calc_inner = (calc_inner
              .replace('style="background:#9cc3bf"', 'style="background:#9fd8d3"')
              .replace('style="background:#9cc3bf;', 'style="background:#9fd8d3;')
              .replace('style="background:var(--petrol)"', 'style="background:var(--teal)"')
              .replace('style="background:var(--petrol);', 'style="background:var(--teal);'))
for key, tip in (("calcConservative", "v4TipC"), ("calcBalanced", "v4TipB"), ("calcDynamic", "v4TipD")):
    m = re.search(r'<span data-i18n="%s">([^<]+)</span>' % key, calc_inner)
    assert m, key
    calc_inner = calc_inner.replace(
        m.group(0),
        f'<span class="hint" tabindex="0"><span data-i18n="{key}">{m.group(1)}</span>'
        f'<span class="bubble" data-i18n="{tip}"></span></span>',
    )
band = f'''

      <section class="band" id="arithmoi" aria-labelledby="calc-title">
        <div class="mesh" aria-hidden="true"><span class="blob b1"></span><span class="blob b2"></span><span class="blob b3"></span><span class="blob b4"></span><span class="blob b5"></span></div>
        <div class="band-grid">
          <div class="band-copy reveal">
            <p class="kicker" data-i18n="v4BandKicker">Πριν μιλήσουμε</p>
            <h2 data-i18n="v4BandTitle">Βάλε δύο νούμερα.<br />Δες τι χτίζεις.</h2>
            <p data-i18n="v4BandText">Εδώ, τώρα, χωρίς εγγραφή και χωρίς να δώσεις κανένα στοιχείο. Ό,τι γράφεις μένει στη δική σου οθόνη.</p>
          </div>
          <div class="calc-card reveal">
            <h3 id="calc-title" class="calc-title" data-i18n="calcTitle">Τι κεφάλαιο μπορώ να χτίσω;</h3>
          {calc_inner}<a class="pill dark calc-cta" href="#contact" data-i18n="calcCta">Θέλεις να δούμε μαζί ποιο σενάριο σου ταιριάζει;</a>
            </div>
          </div>
        </div>
      </section>'''
h = h[:mi] + h[mj:]  # βγάζει το modal
hero_i, hero_j = cut('<section class="hero" aria-labelledby="hero-title">', "</section>")
h = h[:hero_i] + hero_new + band + h[hero_j:]

# το κουμπί «Δοκίμασε τον υπολογιστή» πάει πια στη ζώνη
rep('<button type="button" class="module-tool" data-target="toolModal" data-i18n="moduleToolCalc">Δοκίμασε τον υπολογιστή →</button>',
    '<a class="module-tool" href="#arithmoi" data-i18n="moduleToolCalc">Δοκίμασε τον υπολογιστή →</a>')

# ---------- φιλοσοφία: πρώτα η φράση, μετά η εξήγηση ----------
pi_, pj_ = cut('<p class="philosophy-credo" data-i18n="philosophyCredo">', "</p>")
credo = h[pi_:pj_]
h = h[:pi_] + h[pj_:]
rep('<p class="philosophy-label" data-i18n="philosophyLabel">Πριν οτιδήποτε άλλο</p>',
    '<p class="philosophy-label" data-i18n="philosophyLabel">Πριν οτιδήποτε άλλο</p>\n          '
    + credo.replace("«Καλύτερα καμμία πώληση παρά μία λάθος πώληση.»",
                    "Καλύτερα <mark>καμμία πώληση</mark> παρά μία λάθος πώληση."))

# ---------- διακοσμητικά νούμερα έξω ----------
for num in ("84%", "7", "3"):
    rep(f"</span>\n              <strong>{num}</strong>\n            </span>",
        '</span>\n              <strong class="plus" aria-hidden="true">+</strong>\n            </span>')
mpi, mpj = cut('<div class="metric-panel" aria-label="Planning indicators">', "</div>\n        </div>")
h = h[:mpi] + h[mpj:]

# ---------- παιχνίδια: χρώματα, το πρώτο φαρδύ ----------
gi, gj = cut('<div class="games-grid">', "</a>\n        </div>")
grid = h[gi:gj]
cards = re.findall(r'          <a class="game-card reveal" href="paixnidia/[^"]+">.*?</a>\n', grid, re.S)
assert len(cards) == 7, len(cards)
colors = {"tha-sou-ftasoun": "c-teal wide", "poso-ekane": "c-gold", "pano-i-kato": "c-coral",
          "xilioi-san-esena": "c-violet", "kostos-imeras": "c-sky", "mythos-i-alitheia": "c-ink",
          "logia-i-enstikto": "c-gold"}
def colorize(c):
    slug = re.search(r'paixnidia/([^".]+)\.html', c).group(1)
    return c.replace('class="game-card reveal"', f'class="game-card {colors[slug]} reveal"', 1)
cards = [colorize(c) for c in cards]
cards.sort(key=lambda c: 0 if "tha-sou-ftasoun" in c else 1)
h = h[:gi] + '<div class="games-grid">\n' + "".join(cards) + "        </div>" + h[gj:]

# ---------- σχετικά: φωτογραφία με πινελιά ----------
rep('<section class="about-section" id="about" aria-labelledby="about-title">',
    '''<section class="about-section" id="about" aria-labelledby="about-title">
        <div class="portrait reveal">
          <svg viewBox="0 0 100 100" aria-hidden="true"><path d="M50 4 C 78 2, 98 26, 96 52 C 94 80, 70 98, 46 96 C 20 94, 2 74, 4 48 C 6 22, 24 6, 50 4 Z" fill="#fbe2a9"/></svg>
          <span class="me-photo" role="img" aria-label="Γιάννης Βαρδαβάς, lutcf"></span>
        </div>''')

# ---------- κείμενα (EL/EN) + μικρό script ----------
v4copy = (SCR / "v4copy.js").read_text(encoding="utf-8")
rep("\n};\n\nconst languageButtons", "\n};\n" + v4copy + "\nconst languageButtons")
v4js = (SCR / "v4.js").read_text(encoding="utf-8")
rep("</body>", "<script>\n" + v4js + "\n</script>\n</body>")

assert 'id="toolModal"' not in h
for must in ('id="calcSave"', 'id="calcYears"', 'id="calcR1"', 'id="calcBar3"', 'id="calcTotalGain"',
             'id="contact-form"', 'id="bookLink"', 'id="privacyModal"', 'id="bizChecklist"'):
    assert h.count(must) == 1, must
(ROOT / "standalone_v4.html").write_text(h, encoding="utf-8")
print("ok", len(src), "->", len(h))
