(function () {
  'use strict';

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) { return; }

  document.documentElement.classList.add('js-anim');

  function ready(fn) {
    if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', fn); }
    else { fn(); }
  }

  ready(function () {
    var STEP = 90, MAX = 7;

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) { return; }
        var el = e.target;
        io.unobserve(el);
        el.classList.add('is-visible');
        var wait = (parseInt(el.style.getPropertyValue('--d'), 10) || 0) + 900;
        setTimeout(function () {
          el.classList.add('is-settled');
          el.style.removeProperty('--d');
        }, wait);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });

    function mark(list, extra) {
      Array.prototype.forEach.call(list, function (el, i) {
        if (el.classList.contains('reveal')) { return; }
        if (el.parentElement && el.parentElement.closest('.reveal')) { return; }
        el.classList.add('reveal');
        if (extra) { el.classList.add(extra); }
        el.style.setProperty('--d', Math.min(i, MAX) * STEP + 'ms');
        io.observe(el);
      });
    }

    var hero = document.querySelector('[class*="hero"]') || document.querySelector('section');
    if (hero) { mark(hero.querySelectorAll('img, h1, p, a, [class*="stat"]')); }

    mark(document.querySelectorAll('#projects article, #projects [class*="card"]'), 'reveal-card');
    mark(document.querySelectorAll('section [class*="card"]'), 'reveal-card');
    mark(document.querySelectorAll('section h2, section [class*="lede"]'));
    document.querySelectorAll('section ul, section ol').forEach(function (l) { mark(l.children); });

    /* Compteurs du hero */
    if (hero) {
      Array.prototype.forEach.call(hero.querySelectorAll('*'), function (el) {
        if (el.children.length) { return; }
        var m = el.textContent.trim().match(/^(\d{1,3})(\+?)$/);
        if (!m) { return; }
        var end = parseInt(m[1], 10), suffix = m[2], done = false;
        el.textContent = '0' + suffix;

        function run() {
          if (done) { return; }
          done = true;
          var t0 = null;
          function tick(t) {
            if (t0 === null) { t0 = t; }
            var p = Math.min((t - t0) / 1400, 1);
            el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))) + suffix;
            if (p < 1) { requestAnimationFrame(tick); }
          }
          requestAnimationFrame(tick);
        }

        var co = new IntersectionObserver(function (es) {
          if (es[0].isIntersecting) { co.disconnect(); run(); }
        }, { threshold: 0.4 });
        co.observe(el);
        setTimeout(function () { if (!done) { done = true; el.textContent = end + suffix; } }, 6000);
      });
    }

    /* Barre de progression */
    var bar = document.createElement('div');
    bar.className = 'scroll-progress';
    bar.setAttribute('aria-hidden', 'true');
    document.body.appendChild(bar);
    var ticking = false;
    function update() {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(window.scrollY / h, 1) : 0) + ')';
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    update();

    /* Libellé WhatsApp déployé une fois par session */
    var wa = document.querySelector('.wa-float');
    if (wa) {
      var seen = false;
      try { seen = sessionStorage.getItem('wa-hint') === '1'; } catch (e) {}
      if (!seen) {
        setTimeout(function () {
          wa.classList.add('is-hint');
          try { sessionStorage.setItem('wa-hint', '1'); } catch (e) {}
          setTimeout(function () { wa.classList.remove('is-hint'); }, 5000);
        }, 3500);
      }
    }
  });
})();
