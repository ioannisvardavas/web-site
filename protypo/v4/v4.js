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
     μορφή του· στο ζωντανό site μένει ο κανονικός σύνδεσμος. */
  if (/^(localhost|127\.0\.0\.1)$/.test(location.hostname)) {
    document.querySelectorAll('a[href^="https://risk-radar-2yr.pages.dev"]').forEach((a) => {
      a.href = a.getAttribute("href").replace("https://risk-radar-2yr.pages.dev", "/risk-radar");
      if (!/\/risk-radar\//.test(a.href)) a.href = "/risk-radar/";
    });
  }

  const header = document.querySelector(".site-header");
  const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 8);
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
})();
