(() => {
  function diffTime(start, end) {
    const [sh, sm] = start.split(':').map(Number);
    const [eh, em] = end.split(':').map(Number);

    let mins = (eh * 60 + em) - (sh * 60 + sm);
    if (mins < 0) mins += 24 * 60; // na wypadek przejścia przez północ

    const h = String(Math.floor(mins / 60)).padStart(2, '0');
    const m = String(mins % 60).padStart(2, '0');
    return `${h}:${m}`;
  }

  document
    .querySelectorAll('.panel-heading strong')
    .forEach(el => {
      const txt = el.textContent;

      if (txt.includes('Czas:')) return; // nie dopisuj drugi raz

      const m = txt.match(/Start:\s*(\d{2}:\d{2})\.\s*Koniec:\s*(\d{2}:\d{2})/);
      if (!m) return;

      const duration = diffTime(m[1], m[2]);
      el.textContent = txt.replace(/\.$/, '') + `. Czas: ${duration}.`;
    });
})();
