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
