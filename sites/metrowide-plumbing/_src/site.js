/* Metrowide Plumbing: the job composer, the suburb finder, Melbourne time. */
(function () {
  var d = document;

  /* Job composer: three taps write the message, the text link carries it to Messages */
  d.querySelectorAll('form.composer').forEach(function (f) {
    var msg = f.querySelector('[data-msg]'), sub = f.querySelector('[data-suburb]'), sms = f.querySelector('[data-sms]');
    var touched = false;
    var val = function (n) { var el = f.querySelector('input[name="' + n + '"]:checked'); return el ? el.value : ''; };
    var compose = function () {
      var job = val('job').toLowerCase(), when = val('when'), where = sub.value.trim();
      var nm = (f.querySelector('input[name="name"]').value || '').trim();
      var whenTxt = when === 'Today' ? 'today if you can' : when === 'This week' ? 'some time this week' : 'just after a quote for now';
      var text = 'Hi Dan, I need a plumber for ' + (job === 'something else' ? 'a job' : 'a ' + job) +
        (where ? ' in ' + where : '') + ', ' + whenTxt + '.' + (nm ? ' This is ' + nm + '.' : '');
      if (!touched) msg.value = text;
      sms.href = sms.getAttribute('href').split('?')[0] + '?&body=' + encodeURIComponent(msg.value);
    };
    msg.addEventListener('input', function () { touched = msg.value.length > 0; compose(); });
    f.addEventListener('change', compose);
    f.addEventListener('input', function (e) { if (e.target !== msg) compose(); });
    compose();
  });

  /* Suburb finder */
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

  /* Melbourne local time in the footer */
  var t = d.querySelector('[data-mel-time]');
  if (t && window.Intl) {
    var tick = function () { t.textContent = new Intl.DateTimeFormat('en-AU', { hour: 'numeric', minute: '2-digit', timeZone: 'Australia/Melbourne' }).format(new Date()); };
    tick(); setInterval(tick, 30000);
  }

  /* How a job runs: one stage open at a time */
  var row = d.querySelector('.how-row');
  if (row) row.addEventListener('click', function (e) {
    var b = e.target.closest('.stp button');
    if (!b) return;
    row.querySelectorAll('.stp').forEach(function (s) {
      var on = s === b.parentElement;
      s.classList.toggle('open', on);
      s.querySelector('button').setAttribute('aria-expanded', String(on));
    });
  });
})();
