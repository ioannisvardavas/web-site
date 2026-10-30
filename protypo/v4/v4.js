/* Πρόταση 4 — γέμισμα των sliders, εξηγήσεις (tooltip) στα σενάρια. */
(function () {
  const lang = () => (document.documentElement.lang === "en" ? "en" : "el");
  document.querySelectorAll('.bubble[data-i18n]').forEach((b) => {
    if (!b.textContent.trim()) b.textContent = copy[lang()][b.dataset.i18n] || "";
  });

  const sliders = document.querySelectorAll('.band input[type="range"]');
  const paint = () =>
    sliders.forEach((el) =>
      el.style.setProperty("--p", ((el.value - el.min) / (el.max - el.min)) * 100 + "%")
    );
  sliders.forEach((el) => el.addEventListener("input", paint));
  document.querySelectorAll(".band .goal-btn").forEach((b) => b.addEventListener("click", paint));
  paint();

  document.querySelectorAll(".hint").forEach((t) => {
    t.addEventListener("click", (e) => {
      e.stopPropagation();
      t.classList.toggle("open");
    });
    t.addEventListener("keydown", (e) => {
      if (e.key === "Escape") t.classList.remove("open");
    });
  });
  document.addEventListener("click", () =>
    document.querySelectorAll(".hint.open").forEach((t) => t.classList.remove("open"))
  );
  /* Στη δοκιμή (localhost) τα κουμπιά του Ραντάρ ανοίγουν την τοπική, νέα
     μορφή του· στο ζωντανό site μένει ο κανονικός σύνδεσμος. Η δοκιμαστική
     διεύθυνση στο Cloudflare τα αλλάζει ήδη στο ανέβασμα (tools/anevasma_dokimis.sh). */
  if (/^(localhost|127\.0\.0\.1)$/.test(location.hostname)) {
    document.querySelectorAll('a[href^="https://risk-radar-2yr.pages.dev"]').forEach((a) => {
      a.href = a.getAttribute("href").replace("https://risk-radar-2yr.pages.dev", "/risk-radar");
      if (!/\/risk-radar\//.test(a.href)) a.href = "/risk-radar/";
    });
  }

  /* Μεθοδολογία: οι τέσσερις περιγραφές κρατούν ίδιο ύψος, ώστε τα
     «Αναλυτικά» να πέφτουν στην ίδια γραμμή σε κάθε πλάτος και γλώσσα.
     (Το CSS min-height μόνο του δεν αρκεί: άλλο πλάτος ή τα αγγλικά
     αλλάζουν τον αριθμό των γραμμών.) */
  const stepTexts = document.querySelectorAll("#method .step-head p");
  const evenStepTexts = () => {
    if (!stepTexts.length) return;
    stepTexts.forEach((p) => (p.style.minHeight = ""));
    if (window.innerWidth < 641) return;
    const tallest = Math.max(...[...stepTexts].map((p) => p.getBoundingClientRect().height));
    stepTexts.forEach((p) => (p.style.minHeight = Math.ceil(tallest) + "px"));
  };
  evenStepTexts();
  window.addEventListener("resize", evenStepTexts);
  document.querySelectorAll(".lang-button").forEach((b) =>
    b.addEventListener("click", () => setTimeout(evenStepTexts, 60))
  );
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(evenStepTexts);

  const heroTitle = document.getElementById("hero-title");
  setTimeout(() => heroTitle.classList.add("anim-done"), 1400);

  const header = document.querySelector(".site-header");
  const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 8);
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
})();
