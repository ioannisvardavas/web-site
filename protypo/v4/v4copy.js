
/* Πρόταση 4 — νέα κείμενα (EL/EN) για τα κομμάτια που άλλαξαν μορφή. */
(function () {
  const paint = (word) =>
    '<span class="paint">' + word +
    '<svg viewBox="0 0 400 40" preserveAspectRatio="none" aria-hidden="true"><path d="M6 26 C 90 8, 210 6, 394 20" stroke="#f2b544" stroke-width="22" stroke-linecap="round" fill="none" pathLength="1000"/></svg></span>';
  Object.assign(copy.el, {
    v4Brand: "Βαρδαβάς",
    v4NavNumbers: "Νούμερα",
    v4NavGames: "Παιχνίδια",
    v4NavCta: "Κλείσε 30 λεπτά",
    v4Tag: "Γιάννης Βαρδαβάς · 25 χρόνια στα οικονομικά",
    v4HeroTitle: "Τα λεφτά σου,<br />με " + paint("σχέδιο."),
    v4Lead: "Ασφάλιση, σύνταξη, επενδύσεις και κίνδυνοι επιχείρησης — σε μία καθαρή εικόνα, με πραγματικά νούμερα. Χωρίς ψιλά γράμματα, χωρίς πίεση.",
    v4Cta1: "Κλείσε μια συζήτηση",
    v4Cta2: "Παίξε με τα νούμερα ↓",
    v4Cred1b: "25+ χρόνια",
    v4Cred1: "Τράπεζα Εργασίας → Allianz",
    v4Cred2: "διεθνής πιστοποίηση",
    v4Cred3: "Αρ. Μητρώου ΕΕΑ",
    v4BandKicker: "Πριν μιλήσουμε",
    v4BandTitle: "Βάλε δύο νούμερα.<br />Δες τι χτίζεις.",
    v4BandText: "Εδώ, τώρα, χωρίς εγγραφή και χωρίς να δώσεις κανένα στοιχείο. Ό,τι γράφεις μένει στη δική σου οθόνη.",
    v4TipC: "Αν τα χρήματα απέδιδαν σταθερά 3% τον χρόνο. Είναι υπόθεση για σύγκριση — όχι εγγύηση.",
    v4TipB: "Αν τα χρήματα απέδιδαν σταθερά 6% τον χρόνο. Στην πραγματικότητα οι αποδόσεις ανεβοκατεβαίνουν.",
    v4TipD: "Αν τα χρήματα απέδιδαν σταθερά 8% τον χρόνο. Μεγαλύτερη πιθανή απόδοση, μεγαλύτερα σκαμπανεβάσματα.",
    philosophyCredo: "Καλύτερα <mark>καμμία πώληση</mark> παρά μία λάθος πώληση."
  });
  Object.assign(copy.en, {
    v4Brand: "Vardavas",
    v4NavNumbers: "Numbers",
    v4NavGames: "Games",
    v4NavCta: "Book 30 minutes",
    v4Tag: "Ioannis Vardavas · 25 years in finance",
    v4HeroTitle: "Your money,<br />with a " + paint("plan."),
    v4Lead: "Insurance, retirement, investments and business risk — in one clear picture, with real numbers. No fine print, no pressure.",
    v4Cta1: "Book a conversation",
    v4Cta2: "Play with the numbers ↓",
    v4Cred1b: "25+ years",
    v4Cred1: "Ergasias Bank → Allianz",
    v4Cred2: "international certification",
    v4Cred3: "Athens Chamber Reg. No.",
    v4BandKicker: "Before we talk",
    v4BandTitle: "Enter two numbers.<br />See what you build.",
    v4BandText: "Right here, with no sign-up and without giving any details. Whatever you enter stays on your own screen.",
    v4TipC: "If the money earned a steady 3% a year. It is an assumption for comparison — not a guarantee.",
    v4TipB: "If the money earned a steady 6% a year. In reality, returns go up and down.",
    v4TipD: "If the money earned a steady 8% a year. Higher possible return, bigger ups and downs.",
    philosophyCredo: "Better <mark>no sale</mark> than the wrong sale."
  });
})();
