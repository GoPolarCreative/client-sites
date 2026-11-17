/* Go Polar kit runtime. Shared behaviour only: nav, reveals, stuck header, lightbox, Web3Forms.
   No scroll listeners: everything is IntersectionObserver. Site-specific behaviour lives in site.js. */
(function () {
  var d = document, reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Year */
  d.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* Mobile nav */
  d.querySelectorAll('[data-nav-toggle]').forEach(function (btn) {
    var nav = d.getElementById(btn.getAttribute('aria-controls'));
    if (!nav) return;
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
      d.body.classList.toggle('nav-open', !open);
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) { btn.setAttribute('aria-expanded', 'false'); nav.classList.remove('is-open'); d.body.classList.remove('nav-open'); }
    });
  });

  /* Stuck header state from a sentinel at the top of the body */
  var sentinel = d.querySelector('.gp-sentinel');
  if (sentinel && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (es) { d.body.classList.toggle('scrolled', !es[0].isIntersecting); }).observe(sentinel);
  }

  /* Reveals: .rv gets .in once on screen. Stagger children with --i set by the site. */
  var rv = d.querySelectorAll('.rv');
  if (reduce || !('IntersectionObserver' in window)) {
    rv.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    rv.forEach(function (el) { io.observe(el); });
  }

  /* Lightbox: any [data-lb] link inside a [data-gallery] */
  var groups = d.querySelectorAll('[data-gallery]');
  if (groups.length) {
    var box = d.createElement('dialog');
    box.className = 'gp-lb';
    box.setAttribute('aria-label', 'Photo viewer');
    box.innerHTML = '<figure><img alt=""><figcaption></figcaption></figure>' +
      '<button class="gp-lb-x" type="button" aria-label="Close">Close</button>' +
      '<button class="gp-lb-p" type="button" aria-label="Previous photo">Prev</button>' +
      '<button class="gp-lb-n" type="button" aria-label="Next photo">Next</button>';
    d.body.appendChild(box);
    var im = box.querySelector('img'), cap = box.querySelector('figcaption'), list = [], at = 0, sx = 0;
    var show = function (i) {
      at = (i + list.length) % list.length;
      var a = list[at];
      im.src = a.getAttribute('href');
      im.alt = (a.querySelector('img') || {}).alt || '';
      cap.textContent = a.getAttribute('data-cap') || im.alt;
    };
    groups.forEach(function (g) {
      g.addEventListener('click', function (e) {
        var a = e.target.closest('[data-lb]');
        if (!a) return;
        e.preventDefault();
        list = Array.prototype.slice.call(g.querySelectorAll('[data-lb]'));
        show(list.indexOf(a));
        box.showModal();
      });
    });
    box.querySelector('.gp-lb-x').onclick = function () { box.close(); };
    box.querySelector('.gp-lb-p').onclick = function () { show(at - 1); };
    box.querySelector('.gp-lb-n').onclick = function () { show(at + 1); };
    box.addEventListener('click', function (e) { if (e.target === box) box.close(); });
    box.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') show(at - 1);
      if (e.key === 'ArrowRight') show(at + 1);
    });
    box.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    box.addEventListener('touchend', function (e) {
      var dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 50) show(at + (dx < 0 ? 1 : -1));
    });
  }

  /* Web3Forms: submit with fetch, keep the visitor on the page */
  d.querySelectorAll('form[data-w3f]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var st = f.querySelector('[data-status]'), btn = f.querySelector('button[type=submit]');
      if (f.botcheck && f.botcheck.checked) return;
      btn.disabled = true; f.classList.add('is-sending');
      if (st) st.textContent = 'Sending...';
      var data = Object.fromEntries(new FormData(f));
      fetch(f.action, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          if (!j.success) throw new Error(j.message || 'failed');
          f.classList.remove('is-sending'); f.classList.add('is-sent');
          if (st) st.textContent = f.getAttribute('data-thanks') || 'Thanks, your message is in. We will be in touch shortly.';
          f.reset();
          if (window.gtag) gtag('event', 'generate_lead', { form: data.subject });
        })
        .catch(function () {
          f.classList.remove('is-sending');
          if (st) st.textContent = 'That did not send. Please call us instead.';
        })
        .finally(function () { btn.disabled = false; });
    });
  });

  /* Count calls in GA4 when it is installed */
  d.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="tel:"]');
    if (a && window.gtag) gtag('event', 'phone_call', { link_url: a.href });
  });
})();
