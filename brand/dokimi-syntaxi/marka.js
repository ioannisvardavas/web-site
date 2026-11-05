// Στρώμα μάρκας: προσθέτει σήμα στην επάνω μπάρα, γραμμή μάρκας κάτω αριστερά,
// και τον διακόπτη δοκιμής «Πριν / Μετά» + «Σχέδιο Β / IV». Δεν αγγίζει δεδομένα ή υπολογισμούς.
(function () {
  const G = '<defs><linearGradient id="mkv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7c5cff"/><stop offset=".55" stop-color="#ff6b4a"/><stop offset="1" stop-color="#f2b544"/></linearGradient></defs>';
  const MARKS = {
    B: G + '<g fill="none" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"><path d="M32 14V106" stroke="#121414"/><path d="M32 14H58A20 20 0 0 1 58 54H32" stroke="#121414"/><path d="M32 54H64A26 26 0 0 1 64 106H32" stroke="url(#mkv)"/></g>',
    IV: G + '<g fill="none" stroke="#121414" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"><path d="M22 18V74"/><path d="M44 18L72 74L100 18"/></g><path d="M72 85C72 85 60 98 60 104.5A12 12 0 0 0 84 104.5C84 98 72 85 72 85Z" fill="url(#mkv)"/>'
  };
  let mark = 'B', on = true;
  // προαιρετικά: <script src="marka.js" data-othoni="Κανόνες μελέτης"> ανοίγει κατευθείαν εκείνη την οθόνη
  const othoni = document.currentScript && document.currentScript.dataset.othoni;
  const css = document.getElementById('marka-css');

  function brandNode() {
    const d = document.createElement('div');
    d.className = 'mk-brand';
    d.innerHTML = `<svg viewBox="0 0 120 120" aria-label="Σήμα">${MARKS[mark]}</svg><div class="mk-who">Γιάννης Βαρδαβάς<small>Financial Planning · LUTCF</small></div><span class="mk-sep"></span>`;
    return d;
  }
  function apply() {
    css.disabled = !on;
    document.querySelectorAll('.mk-brand,.mk-foot,.mk-fam').forEach(n => n.remove());
    if (!on) return;
    const top = document.querySelector('.top');
    if (top) {
      top.insertBefore(brandNode(), top.firstChild);
      const app = top.querySelector('.top__app');
      if (app) { const f = document.createElement('span'); f.className = 'mk-fam'; f.innerHTML = '<i></i>Σύνταξη'; app.appendChild(f); }
    }
    const foot = document.querySelector('.nav__foot');
    if (foot) { const m = document.createElement('div'); m.className = 'mk-foot'; m.innerHTML = '<b>Γιάννης Βαρδαβάς</b> · Πρόβα του μέλλοντος<br>Χωρίς αστεράκι: κάθε παραδοχή έχει πηγή.'; foot.after(m); }
  }
  function toggle() {
    const t = document.createElement('div');
    t.className = 'mk-test';
    t.innerHTML = '<span>Δοκιμή μάρκας</span><button data-k="off">Πριν</button><button data-k="on">Μετά</button><i></i><button data-m="B">Σχέδιο Β</button><button data-m="IV">IV</button>';
    t.addEventListener('click', e => {
      const b = e.target.closest('button'); if (!b) return;
      if (b.dataset.k) on = b.dataset.k === 'on';
      if (b.dataset.m) { mark = b.dataset.m; on = true; }
      apply(); sync();
    });
    function sync() {
      t.querySelectorAll('[data-k]').forEach(b => b.setAttribute('aria-pressed', String((b.dataset.k === 'on') === on)));
      t.querySelectorAll('[data-m]').forEach(b => b.setAttribute('aria-pressed', String(on && b.dataset.m === mark)));
    }
    document.body.appendChild(t); sync();
  }
  // Η εφαρμογή (React) ζωγραφίζει την οθόνη λίγο μετά το φόρτωμα· περιμένουμε την επάνω μπάρα.
  const wait = setInterval(() => {
    if (document.querySelector('.top')) { clearInterval(wait); apply(); toggle();
      if (othoni) { const b = [...document.querySelectorAll('.nav__item')].find(n => n.textContent.includes(othoni)); if (b) b.click(); }
      // αν η εφαρμογή ξαναζωγραφίσει την μπάρα, ξαναβάζουμε το σήμα
      new MutationObserver(() => { if (on && !document.querySelector('.mk-brand')) apply(); }).observe(document.getElementById('root'), { childList: true, subtree: true });
    }
  }, 60);
})();
