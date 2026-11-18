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
          var ar = f.getAttribute('data-autoreply');
          if (ar && data.email) {
            fetch(ar, { method: 'POST', mode: 'no-cors', headers: { 'Content-Type': 'text/plain;charset=utf-8' },
              body: JSON.stringify({ site: f.getAttribute('data-site'), name: data.name || '', email: data.email }) }).catch(function () {});
          }
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

  /* Live Google reviews. The section ([data-gr-section]) stays hidden until /api/reviews returns
     reviews, so a client with no Google reviews yet simply has no section. Fetched only when a visitor
     scrolls near it: Google bills per call and its terms forbid caching review text. */
  d.querySelectorAll('[data-gr]').forEach(function (mount) {
    var sec = mount.closest('[data-gr-section]') || mount;
    var star = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5l2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3 6.1 20.6l1.3-6.6L2.5 9.4l6.6-.8z"/></svg>';
    var stars = function (n) {
      var row = new Array(6).join(star), pct = Math.max(0, Math.min(5, n || 0)) / 5 * 100;
      return '<span class="gr-stars" role="img" aria-label="' + (Math.round((n || 0) * 10) / 10) + ' out of 5 stars">' +
        '<span class="gr-stars-base">' + row + '</span><span class="gr-stars-fill" style="width:' + pct + '%">' + row + '</span></span>';
    };
    var esc = function (t) { var e = d.createElement('div'); e.textContent = t == null ? '' : String(t); return e.innerHTML; };
    var b1 = mount.getAttribute('data-btn1') || 'gr-btn', b2 = mount.getAttribute('data-btn2') || 'gr-btn';
    var render = function (j) {
      var cards = j.reviews.map(function (r) {
        var name = esc(r.author || 'Google user');
        var who = r.authorUrl ? '<a class="gr-name" href="' + esc(r.authorUrl) + '" target="_blank" rel="noopener">' + name + '</a>' : '<span class="gr-name">' + name + '</span>';
        var av = r.photo ? '<img class="gr-av" src="' + esc(r.photo) + '" alt="" width="44" height="44" loading="lazy" referrerpolicy="no-referrer">' :
          '<span class="gr-av gr-av-i" aria-hidden="true">' + name.charAt(0) + '</span>';
        return '<article class="gr-card" role="listitem"><div class="gr-head">' + av + '<div class="gr-who">' + who +
          '<span class="gr-when">' + esc(r.when || '') + '</span></div></div>' + stars(r.rating) +
          '<p class="gr-text">' + esc(r.text) + '</p><button class="gr-more" type="button" hidden>Read more</button></article>';
      }).join('');
      var count = j.count ? 'from ' + j.count + ' Google review' + (j.count === 1 ? '' : 's') : 'on Google';
      mount.innerHTML =
        '<div class="gr-summary"><div class="gr-score"><span class="gr-num">' + (j.rating ? j.rating.toFixed(1) : '') + '</span>' +
        '<div>' + stars(j.rating) + '<p class="gr-count">' + count + '</p></div></div><div class="gr-actions">' +
        (j.url ? '<a class="' + b1 + '" href="' + esc(j.url) + '" target="_blank" rel="noopener">Read all on Google</a>' : '') +
        (j.writeUrl ? '<a class="' + b2 + '" href="' + esc(j.writeUrl) + '" target="_blank" rel="noopener">Leave a review</a>' : '') +
        '</div></div><div class="gr-track" role="list" tabindex="0" aria-label="Google reviews">' + cards + '</div>' +
        '<div class="gr-foot"><p class="gr-attr">Most relevant reviews, from Google Maps</p>' +
        '<div class="gr-nav"><button class="gr-prev" type="button" aria-label="Previous reviews"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.4"/></svg></button>' +
        '<button class="gr-next" type="button" aria-label="Next reviews"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.4"/></svg></button></div></div>';
      sec.classList.add('gr-ready');
      var track = mount.querySelector('.gr-track');
      var by = function (dir) { var c = track.querySelector('.gr-card'); track.scrollBy({ left: dir * (c ? c.offsetWidth + 16 : 320), behavior: reduce ? 'auto' : 'smooth' }); };
      mount.querySelector('.gr-prev').onclick = function () { by(-1); };
      mount.querySelector('.gr-next').onclick = function () { by(1); };
      mount.querySelectorAll('.gr-card').forEach(function (c) {
        var t = c.querySelector('.gr-text'), m = c.querySelector('.gr-more');
        if (t.scrollHeight > t.clientHeight + 4) {
          m.hidden = false;
          m.onclick = function () { var o = c.classList.toggle('open'); m.textContent = o ? 'Show less' : 'Read more'; };
        }
      });
    };
    var load = function () {
      fetch(mount.getAttribute('data-src') || '/api/reviews', { headers: { Accept: 'application/json' } })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (j) { if (j && j.reviews && j.reviews.length) render(j); })
        .catch(function () {});
    };
    if (window.__grDemo) { render(window.__grDemo); return; }
    if (!('IntersectionObserver' in window)) { load(); return; }
    var s = d.createElement('div');
    s.style.height = '1px';
    s.setAttribute('aria-hidden', 'true');
    sec.parentNode.insertBefore(s, sec);
    var io2 = new IntersectionObserver(function (es) {
      if (es[0].isIntersecting) { io2.disconnect(); load(); }
    }, { rootMargin: '900px 0px' });
    io2.observe(s);
  });

  /* Count calls in GA4 when it is installed */
  d.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="tel:"]');
    if (a && window.gtag) gtag('event', 'phone_call', { link_url: a.href });
  });
})();
