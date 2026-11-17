/* Bhavan Building: the stepping statements and the room filter. IntersectionObserver only. */
(function () {
  var d = document;

  /* Scene: the statement nearest mid-screen is lit, with its pair of photographs */
  var scene = d.querySelector('.rooms-scene');
  if (scene && 'IntersectionObserver' in window) {
    var set = function (k) {
      scene.querySelectorAll('.sc-i').forEach(function (li) { li.classList.toggle('on', li.getAttribute('data-k') === k); });
      scene.querySelectorAll('.sc-pair').forEach(function (p) { p.classList.toggle('on', p.getAttribute('data-k') === k); });
    };
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) set(e.target.getAttribute('data-k')); });
    }, { rootMargin: '-50% 0px -50% 0px' });
    scene.querySelectorAll('.sc-mark').forEach(function (m) { io.observe(m); });
  }

  /* Room filter: re-hang the wall with the rooms that match */
  d.querySelectorAll('.wall').forEach(function (w) {
    var tiles = [].slice.call(w.querySelectorAll('.pj')), count = w.querySelector('[data-room-count]');
    var words = ['No', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten'];
    var hang = function (room) {
      var n = 0;
      tiles.forEach(function (t) {
        t.className = t.className.replace(/\bp\d+\b/g, '').trim();
        var show = room === 'All' || t.getAttribute('data-room') === room;
        t.hidden = !show;
        if (show) { t.classList.add('p' + n); t.classList.add('in'); n++; }
      });
      var noun = room === 'All' ? 'rooms' : room.toLowerCase();
      if (n === 1) noun = noun === 'laundries' ? 'laundry' : noun.replace(/s$/, '');
      count.textContent = (words[n] || n) + ' ' + noun;
    };
    w.querySelectorAll('[data-room-filter]').forEach(function (b) {
      b.addEventListener('click', function () {
        w.querySelectorAll('[data-room-filter]').forEach(function (x) { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', String(x === b)); });
        hang(b.getAttribute('data-room-filter'));
      });
    });
  });

  /* Service pages: the enquiry form arrives with the project already chosen */
  var hash = location.hash;
  if (hash === '#enquire') { var f = d.getElementById('enquire'); if (f) f.scrollIntoView(); }
})();
