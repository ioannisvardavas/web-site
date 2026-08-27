#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Παίρνει τα παιχνίδια από τον φάκελο ELI5 και τα ετοιμάζει για το site.

Ο φάκελος ELI5 παραμένει η ΜΟΝΗ πηγή αλήθειας — εδώ τίποτα δεν γράφεται με το
χέρι. Ό,τι αλλάζει, αλλάζει εκεί και ξανατρέχει αυτό.

Τι κάνει:
  1. Αντιγράφει τα δέκα αρχεία με λατινικά ονόματα (οι ελληνικές ονομασίες
     γίνονται σπασμένες διευθύνσεις όταν στέλνονται σε κάποιον).
  2. Ξαναγράφει τους μεταξύ τους συνδέσμους.
  3. Στο «Παζάρι της ημέρας» βγάζει κάθε αναφορά σε εταιρεία και σε τιμολόγιο,
     κλείνει την ανάλυση τιμής, και το παρουσιάζει ως ενδεικτικό κόστος κάλυψης.
  4. Στο ταμπλό βάζει επιστροφή στο site και κάρτα κοινοποίησης.
  5. Στο τέλος ελέγχει ότι δεν ξέφυγε τίποτα.

Τρέξιμο:  python3 tools/sync_paixnidia.py
"""

import re
import sys
from pathlib import Path
from urllib.parse import quote

PIGI = Path("/Users/user/Desktop/ELI5")
RIZA = Path(__file__).resolve().parent.parent
STOXOS = RIZA / "paixnidia"

SITE = "https://vardavas-site.pages.dev"

# ελληνικό όνομα αρχείου -> λατινικό, όπως θα ζει στο site
ONOMATA = {
    "ΤΑΜΠΛΟ.html":                      "index.html",
    "ΠΟΣΟ_ΕΚΑΝΕ_ΠΑΙΧΝΙΔΙ.html":         "poso-ekane.html",
    "ΠΑΝΩ_Η_ΚΑΤΩ_ΠΑΙΧΝΙΔΙ.html":        "pano-i-kato.html",
    "ΧΙΛΙΟΙ_ΣΑΝ_ΕΣΕΝΑ_ΠΑΙΧΝΙΔΙ.html":   "xilioi-san-esena.html",
    "ΘΑ_ΣΟΥ_ΦΤΑΣΟΥΝ_ΠΑΙΧΝΙΔΙ.html":     "tha-sou-ftasoun.html",
    "ΠΑΖΑΡΙ_ΗΜΕΡΑΣ_ΠΑΙΧΝΙΔΙ.html":      "kostos-imeras.html",
    "ΜΥΘΟΣ_Η_ΑΛΗΘΕΙΑ_ΠΑΙΧΝΙΔΙ.html":    "mythos-i-alitheia.html",
    "ΛΟΓΙΑ_Η_ΕΝΣΤΙΚΤΟ_ΠΑΙΧΝΙΔΙ.html":   "logia-i-enstikto.html",
    "ΠΟΣΕΣ_ΦΟΡΕΣ_ΑΚΟΜΑ.html":           "poses-fores-akoma.html",
    "ΠΛΗΘΩΡΙΣΜΟΣ_ELI5.html":            "plithorismos.html",
    "ΚΛΑΣΜΑΤΙΚΑ_ΑΠΟΘΕΜΑΤΙΚΑ_ELI5.html": "pios-ftiaxnei-ta-evro.html",
}

lathi = []


def allakse(keimeno, palio, neo, arxeio, fores=1):
    """Αντικατάσταση που σταματάει αν δεν βρει ΑΚΡΙΒΩΣ όσα περίμενε."""
    vrethikan = keimeno.count(palio)
    if vrethikan != fores:
        lathi.append(f"{arxeio}: περίμενα {fores}, βρήκα {vrethikan} → {palio[:70]!r}")
        return keimeno
    return keimeno.replace(palio, neo)


def allakse_motivo(keimeno, motivo, neo, arxeio, fores=1):
    neo_keimeno, n = re.subn(motivo, neo, keimeno, flags=re.DOTALL)
    if n != fores:
        lathi.append(f"{arxeio}: περίμενα {fores} ταίριασμα, βρήκα {n} → {motivo[:70]!r}")
        return keimeno
    return neo_keimeno


# ───────────────────────── ΤΟ ΠΑΖΑΡΙ: ανώνυμο ─────────────────────────

NEO_YPOSELIDO = (
    '<b>Τι είναι αυτή η τιμή:</b> <b>ενδεικτικό κόστος κάλυψης ζωής</b> για την ηλικία, '
    'το κεφάλαιο και τη διάρκεια που διάλεξες, βάσει ισχύοντος τιμοκαταλόγου ασφαλιστικής '
    'εταιρείας. Καμία τιμή δεν είναι εκτίμηση.\n'
    '  Η τιμή ανά ημέρα είναι το <b>ασφάλιστρο του 1ου έτους ÷ 365</b>, δηλαδή η <b>υψηλότερη</b> '
    'χρονιά: περιλαμβάνει το δικαίωμα συμβολαίου και την εισφορά εγγυητικού κεφαλαίου.\n'
    '  Στη ζωή <b>δεν υπάρχει φόρος ασφαλίστρων</b>. Εγγύηση ΤτΕ έως 60.000 € ανά συμβόλαιο.\n'
    '  Στο <b>μειούμενο</b> κεφάλαιο η κάλυψη ακολουθεί την καμπύλη του δανείου, γι\' αυτό είναι '
    'φθηνότερη· στο <b>σταθερό</b> μένει ίδια ως τη λήξη.\n'
    '  <b>Ενδεικτικός υπολογισμός, όχι προσφορά.</b>'
)


def pazari(t, arx):
    # 1. το υποσέλιδο: καμία εταιρεία, κανένας αριθμός τιμολογίου
    t = allakse_motivo(
        t,
        r'<b>Πηγή τιμών:</b>.*?<b>Ενδεικτικός υπολογισμός βάσει τιμοκαταλόγου, όχι προσφορά\.</b>',
        NEO_YPOSELIDO.replace('\\', '\\\\'),
        arx,
    )
    # 2. φεύγει το πτυσσόμενο «Πώς βγήκε η τιμή — ανάλυση»
    t = allakse_motivo(
        t,
        r'\s*<details>\s*<summary>Πώς βγήκε η τιμή — ανάλυση</summary>\s*'
        r'<div class="dl" id="dl"></div>\s*</details>',
        '',
        arx,
    )
    # 3. και ο κώδικας που τη γέμιζε
    t = allakse_motivo(
        t,
        r'\n\s*/\* --- ανάλυση --- \*/\s*\n\s*\$\("dl"\)\.innerHTML =.*?η πρώτη\.`;\n',
        '\n',
        arx,
    )
    # 4. το όνομα προϊόντος γίνεται περιγραφή κάλυψης
    t = allakse(t, "<b>SAFE PLAN — μειούμενο κεφάλαιο</b>",
                   "<b>Πρόσκαιρη — μειούμενο κεφάλαιο</b>", arx)
    return t


# ───────────────────────── ΤΟ ΤΑΜΠΛΟ ─────────────────────────

KARTA = f'''<meta name="description" content="Επτά σύντομα παιχνίδια για τα λεφτά, τον χρόνο και τον κίνδυνο. Χωρίς παρουσίαση, χωρίς εγγραφή.">
<meta property="og:type" content="website">
<meta property="og:title" content="Το κέρασμα — επτά σύντομα παιχνίδια">
<meta property="og:description" content="Τρία λεπτά το καθένα. Τα νούμερα είναι αληθινά, από ΕΛΣΤΑΤ, Eurostat και ΕΚΤ.">
<meta property="og:url" content="{SITE}/paixnidia/">
<meta property="og:image" content="{SITE}/og-image-v2.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/og-image-v2.png">
<link rel="canonical" href="{SITE}/paixnidia/">
'''

PISO = ('<a class="noprint" href="/" style="display:inline-block; margin-bottom:18px; '
        'font-family:var(--disp); font-size:.86rem; font-weight:700; letter-spacing:.06em; '
        'text-transform:uppercase; color:var(--soft); text-decoration:none">'
        '← Γιάννης Βαρδαβάς</a>\n\n<h1>Το κέρασμα</h1>')


def tamplo(t, arx):
    # κάρτα κοινοποίησης (Viber/WhatsApp/LinkedIn)
    t = allakse(t, '<link rel="preconnect" href="https://fonts.googleapis.com">',
                   KARTA + '<link rel="preconnect" href="https://fonts.googleapis.com">', arx)
    # επιστροφή στο site
    t = allakse(t, '<h1>Το κέρασμα</h1>', PISO, arx)
    # καμία εταιρεία στο υποσέλιδο
    t = allakse(t, 'και τα επίσημα τιμολόγια Allianz.',
                   'και ισχύοντα τιμολόγια ασφαλιστικής εταιρείας.', arx)
    return t


EIDIKA = {"ΠΑΖΑΡΙ_ΗΜΕΡΑΣ_ΠΑΙΧΝΙΔΙ.html": pazari, "ΤΑΜΠΛΟ.html": tamplo}


# ───────────────────────── Η ΥΠΟΓΡΑΦΗ ─────────────────────────
# Κάθε παιχνίδι ταξιδεύει μόνο του: στέλνεται σε WhatsApp, προωθείται, ανοίγει
# χωρίς να έχει περάσει κανείς από το site. Ως τώρα ο παραλήπτης δεν μάθαινε
# ποτέ ποιος το έφτιαξε. Από εδώ και πέρα κάθε αρχείο κλείνει με όνομα,
# τηλέφωνο και έναν δρόμο πίσω.

TILEFONO = "698 388 0746"
TIL_LINK = "+306983880746"
WHATSAPP = "306983880746"

# Ο τίτλος του κάθε παιχνιδιού — μπαίνει στο έτοιμο μήνυμα του WhatsApp,
# ώστε ο Γιάννης να ξέρει από πού ήρθε ο κόσμος χωρίς να ρωτήσει.
TITLOI = {
    "index.html":               "Το κέρασμα",
    "poso-ekane.html":          "Πόσο έκανε;",
    "pano-i-kato.html":         "Πάνω ή κάτω;",
    "xilioi-san-esena.html":    "Χίλιοι σαν εσένα",
    "tha-sou-ftasoun.html":     "Θα σου φτάσουν;",
    "kostos-imeras.html":       "Το παζάρι της ημέρας",
    "mythos-i-alitheia.html":   "Μύθος ή αλήθεια;",
    "logia-i-enstikto.html":    "Λόγια εναντίον Ενστίκτου",
    "poses-fores-akoma.html":   "Πόσες μέρες ακόμα μαζί;",
    "plithorismos.html":        "Τι κάνει ο χρόνος στα λεφτά σου",
    "pios-ftiaxnei-ta-evro.html": "Ποιος φτιάχνει τα ευρώ",
}

# Μία γραμμή ανά παιχνίδι: πιάνει το νήμα που μόλις άφησε ο παίκτης.
# Γενική ατάκα σε όλα θα διαβαζόταν ως διαφήμιση· η συνέχεια της κουβέντας όχι.
AGKISTRIA = {
    "index.html":
        "Τα παιχνίδια είναι το κέρασμα. Η κουβέντα για τους <b>δικούς σου</b> αριθμούς "
        "είναι κι αυτή δωρεάν.",
    "poso-ekane.html":
        "Χάνουμε όλοι — και προς την ίδια μεριά. Θέλεις να δούμε τι σημαίνει αυτό "
        "για τα <b>δικά σου</b> λεφτά;",
    "pano-i-kato.html":
        "Στα λίγα χρόνια η αγορά είναι θόρυβος· στα πολλά, τάση. "
        "Πόσα χρόνια έχουν <b>τα δικά σου</b> μπροστά τους;",
    "xilioi-san-esena.html":
        "Τα νούμερα λένε τι συμβαίνει στους χίλιους. Εσύ είσαι ο ένας — "
        "και το πλάνο γίνεται πάντα για <b>τον έναν</b>.",
    "tha-sou-ftasoun.html":
        "Είδες αν φτάνουν στο παράδειγμα. Θες να δούμε αν φτάνουν "
        "<b>στα δικά σου</b>;",
    "kostos-imeras.html":
        "Αυτή ήταν ενδεικτική τιμή. Η <b>δική σου</b> βγαίνει σε δέκα λεπτά, "
        "στο τηλέφωνο.",
    "mythos-i-alitheia.html":
        "Αν σε ξάφνιασαν οι μισές, αξίζει μισή ώρα κουβέντα για "
        "<b>τα δικά σου</b>.",
    "logia-i-enstikto.html":
        "Το ένστικτο είναι καλός σύμβουλος στα μικρά και κακός στα μεγάλα. "
        "Για <b>τα μεγάλα</b>, πάρε με.",
    "poses-fores-akoma.html":
        "Αυτό δεν λύνεται με λεφτά. Ό,τι <b>λύνεται</b> όμως, ας λυθεί "
        "όσο υπάρχει χρόνος.",
    "plithorismos.html":
        "Ο χρόνος δουλεύει ήδη πάνω στα λεφτά σου. Το ερώτημα είναι αν δουλεύει "
        "<b>για σένα ή εναντίον σου</b>.",
    "pios-ftiaxnei-ta-evro.html":
        "Τώρα ξέρεις ποιος φτιάχνει τα ευρώ. Το επόμενο ερώτημα είναι τι κάνεις "
        "εσύ με <b>τα δικά σου</b>.",
}

YPOGRAFI_CSS = """<style>
/* ── η υπογραφή (μπαίνει αυτόματα από το tools/sync_paixnidia.py) ── */
.ypog{width:100%; max-width:620px; margin:34px auto 4px; box-sizing:border-box;
  background:var(--card); border:1px solid var(--line); border-radius:18px;
  padding:20px 20px 18px; box-shadow:var(--shadow);
  font-family:var(--disp); color:var(--ink); text-align:left}
.ypog-hook{font-family:var(--book); font-size:16.5px; line-height:1.5;
  color:var(--ink); margin:0 0 16px}
.ypog-hook b{color:var(--euro); font-weight:700}
.ypog-nm{font-size:19px; font-weight:800; letter-spacing:-.01em; margin:0}
.ypog-nm span{font-size:11.5px; font-weight:700; letter-spacing:.08em;
  color:var(--gold-text, var(--gold)); margin-left:7px; vertical-align:2px}
.ypog-rol{font-family:var(--book); font-size:13.5px; color:var(--soft);
  margin:3px 0 15px; line-height:1.4}
.ypog-act{display:flex; flex-wrap:wrap; gap:9px}
.ypog-b{flex:1 1 auto; min-width:130px; text-align:center; text-decoration:none;
  padding:12px 14px; border-radius:13px; font-size:15.5px; font-weight:700;
  border:1.5px solid var(--line); color:var(--ink); background:var(--paper)}
.ypog-b.kyrio{background:var(--euro); border-color:var(--euro); color:#fff}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .ypog-b.kyrio{color:#08122A}}
:root[data-theme="dark"] .ypog-b.kyrio{color:#08122A}
:root[data-theme="light"] .ypog-b.kyrio{color:#fff}
.ypog-site{display:inline-block; margin-top:15px; font-size:12.5px; font-weight:700;
  letter-spacing:.05em; text-transform:uppercase; color:var(--soft); text-decoration:none}
@media print{.ypog{box-shadow:none; page-break-inside:avoid} .ypog-act{display:none}}
</style>
"""


def ypografi_html(onoma):
    minima = ("Γεια σας κ. Βαρδαβά. Έπαιξα το «" + TITLOI[onoma] +
              "» και θα ήθελα να δούμε τους δικούς μου αριθμούς.")
    return (
        '\n<section class="ypog" id="ypografi">\n'
        '  <p class="ypog-hook">' + AGKISTRIA[onoma] + '</p>\n'
        '  <p class="ypog-nm">Γιάννης Βαρδαβάς <span>LUTCF</span></p>\n'
        '  <p class="ypog-rol">Financial Planning &amp; Business Risk Management</p>\n'
        '  <div class="ypog-act">\n'
        '    <a class="ypog-b kyrio" href="tel:' + TIL_LINK + '">Πάρε με · ' + TILEFONO + '</a>\n'
        '    <a class="ypog-b" href="https://wa.me/' + WHATSAPP + '?text=' + quote(minima) +
        '" target="_blank" rel="noopener">WhatsApp</a>\n'
        '    <a class="ypog-b" href="viber://chat?number=' + quote(TIL_LINK) + '">Viber</a>\n'
        '  </div>\n'
        '  <a class="ypog-site" href="' + SITE + '/">Τα υπόλοιπα εργαλεία &rarr;</a>\n'
        '</section>\n'
    )


def vale_ypografi(t, onoma):
    if onoma not in AGKISTRIA:
        lathi.append(f"{onoma}: δεν έχει οριστεί γραμμή υπογραφής")
        return t
    t = allakse(t, "</head>", YPOGRAFI_CSS + "</head>", onoma)
    t = allakse(t, "</body>", ypografi_html(onoma) + "</body>", onoma)
    return t


# ───────────────────────── Η ΔΟΥΛΕΙΑ ─────────────────────────

def main():
    if not PIGI.is_dir():
        sys.exit(f"Δεν βρέθηκε ο φάκελος: {PIGI}")
    STOXOS.mkdir(exist_ok=True)

    grammena = {}
    for palio_onoma, neo_onoma in ONOMATA.items():
        pigaio = PIGI / palio_onoma
        if not pigaio.is_file():
            lathi.append(f"λείπει από την πηγή: {palio_onoma}")
            continue
        t = pigaio.read_text(encoding="utf-8")

        # οι μεταξύ τους σύνδεσμοι, με τα νέα ονόματα
        for a, b in ONOMATA.items():
            t = t.replace(f'href="{a}"', f'href="{b}"')
            t = t.replace(f'arxeio:"{a}"', f'arxeio:"{b}"')
            t = t.replace(f'arxeio: "{a}"', f'arxeio: "{b}"')

        if palio_onoma in EIDIKA:
            t = EIDIKA[palio_onoma](t, palio_onoma)

        # η υπογραφή μπαίνει τελευταία, σε ΟΛΑ ανεξαιρέτως
        t = vale_ypografi(t, neo_onoma)

        grammena[neo_onoma] = t

    # ───── οι φρουροί: τι ΔΕΝ επιτρέπεται να έχει φύγει στο site ─────
    for onoma, t in grammena.items():
        for apagoreymeno in ("Allianz", "SAFE PLAN", "τιμ. 008", "τιμολόγιο 008", "τιμολόγιο 007"):
            if apagoreymeno in t:
                lathi.append(f"{onoma}: έμεινε μέσα «{apagoreymeno}»")
        for ell in re.findall(r'href="([^"]*\.html)"', t):
            if ell in ONOMATA:
                lathi.append(f"{onoma}: έμεινε ελληνικός σύνδεσμος → {ell}")
    if "index.html" in grammena and "Πώς βγήκε η τιμή" in grammena.get("kostos-imeras.html", ""):
        lathi.append("kostos-imeras.html: η ανάλυση τιμής δεν αφαιρέθηκε")

    # κανένα αρχείο δεν φεύγει ανώνυμο — ούτε μία φορά, ούτε δύο
    for onoma, t in grammena.items():
        if t.count('<section class="ypog" id="ypografi">') != 1:
            lathi.append(f"{onoma}: η υπογραφή δεν μπήκε ακριβώς μία φορά")
        if TIL_LINK not in t:
            lathi.append(f"{onoma}: λείπει το τηλέφωνο")
        if f"{SITE}/" not in t:
            lathi.append(f"{onoma}: λείπει ο δρόμος πίσω στο site")

    if lathi:
        print("✖ ΣΤΑΜΑΤΗΣΑ — δεν γράφτηκε τίποτα:\n")
        for l in lathi:
            print("  •", l)
        sys.exit(1)

    for onoma, t in grammena.items():
        (STOXOS / onoma).write_text(t, encoding="utf-8")

    print(f"✓ {len(grammena)} αρχεία έτοιμα στο {STOXOS.relative_to(RIZA)}/")
    for onoma in grammena:
        print("   ", onoma)


if __name__ == "__main__":
    main()
