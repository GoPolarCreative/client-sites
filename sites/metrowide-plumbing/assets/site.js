/* Metrowide Plumbing: services dropdown, stat count-up, suburb checker. No scroll listeners. */
(function () {
  var d = document, reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Services dropdown: click for touch and keyboard, hover handled in CSS on desktop */
  d.querySelectorAll('.dd').forEach(function (dd) {
    var btn = dd.querySelector('.dd-btn');
    btn.addEventListener('click', function () {
      var open = !dd.classList.contains('open');
      dd.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', String(open));
    });
    d.addEventListener('click', function (e) {
      if (!dd.contains(e.target) && dd.classList.contains('open') && window.matchMedia('(min-width: 1024px)').matches) {
        dd.classList.remove('open'); btn.setAttribute('aria-expanded', 'false');
      }
    });
    dd.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { dd.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); btn.focus(); }
    });
  });

  /* Count-up on the stat band */
  var nums = d.querySelectorAll('[data-count]');
  if (nums.length && 'IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        io.unobserve(e.target);
        var el = e.target, to = +el.getAttribute('data-count'), t0 = null;
        var step = function (t) {
          if (!t0) t0 = t;
          var p = Math.min((t - t0) / 1200, 1);
          el.textContent = Math.round(to * (1 - Math.pow(1 - p, 3)));
          if (p < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
      });
    }, { threshold: 0.6 });
    nums.forEach(function (n) { io.observe(n); });
  } else {
    nums.forEach(function (n) { n.textContent = n.getAttribute('data-count'); });
  }

  /* Suburb checker */
  d.querySelectorAll('[data-area-filter]').forEach(function (input) {
    var scope = input.closest('section'), note = scope.querySelector('[data-area-note]'), orig = note.innerHTML;
    var items = scope.querySelectorAll('[data-sub]');
    input.addEventListener('input', function () {
      var q = input.value.trim().toLowerCase(), hit = null;
      items.forEach(function (li) {
        var on = q.length > 1 && li.getAttribute('data-sub').indexOf(q) === 0;
        li.classList.toggle('hit', on);
        if (on && !hit) hit = li.textContent;
      });
      note.classList.toggle('hit', !!hit);
      note.innerHTML = hit ? 'Yes, we cover ' + hit + '. Call Dan on <a href="tel:+61423017489">0423 017 489</a>.' :
        (q.length > 2 ? 'Not on our list, but we probably still cover it. <a href="tel:+61423017489">Call and ask.</a>' : orig);
    });
  });
})();
