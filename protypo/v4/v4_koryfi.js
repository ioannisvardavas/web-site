/* Το site ανοίγει πάντα από την κορυφή: από το Dock (η εφαρμογή του Safari έχει
   κρατήσει διεύθυνση με #about), με πληκτρολόγηση, από σελιδοδείκτη, με ανανέωση.
   Τρέχει στο <head>, πριν ο browser προλάβει να κατέβει στην ενότητα.
   Εξαιρέσεις: το «Πίσω» κρατά τη θέση του, και ένας σύνδεσμος από άλλη σελίδα προς
   ενότητα (π.χ. το «πίσω στα παιχνίδια» → /#games) πάει εκεί που λέει. */
(function () {
  var nav = performance.getEntriesByType("navigation")[0];
  var type = nav ? nav.type : "navigate";
  if (type === "back_forward") {
    history.scrollRestoration = "auto";
    return;
  }
  if (type === "navigate" && document.referrer && location.hash) return;
  history.scrollRestoration = "manual";
  if (!location.hash) return;
  history.replaceState(null, "", location.pathname + location.search);
  window.addEventListener("load", function () {
    window.scrollTo({ top: 0, left: 0, behavior: "instant" });
  });
})();
