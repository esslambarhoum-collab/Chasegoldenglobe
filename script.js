// Chase Golden Globe — shared site script
(function () {
  'use strict';

  // nav background on scroll
  var nav = document.querySelector('.site-nav');
  if (nav) {
    window.addEventListener('scroll', function () {
      nav.classList.toggle('solid', window.scrollY > 50);
    }, { passive: true });
  }

  // scroll reveal
  var revealEls = document.querySelectorAll('.rv');
  if (revealEls.length && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) e.target.classList.add('on');
      });
    }, { threshold: 0.12 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('on'); });
  }

  // animated stat counters
  var counters = document.querySelectorAll('.stat-n[data-count]');
  if (counters.length && 'IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        var target = parseInt(el.dataset.count, 10);
        var cur = 0;
        var step = target / 45;
        (function tick() {
          cur += step;
          el.textContent = cur >= target ? target : Math.floor(cur);
          if (cur < target) requestAnimationFrame(tick);
        })();
        cio.unobserve(el);
      });
    }, { threshold: 0.5 });
    counters.forEach(function (n) { cio.observe(n); });
  }

  // mobile hamburger menu
  var toggle = document.getElementById('navToggle');
  var navLinks = document.getElementById('navLinks');
  var backdrop = document.getElementById('navBackdrop');
  if (toggle && navLinks && backdrop) {
    function closeMenu() {
      toggle.setAttribute('aria-expanded', 'false');
      navLinks.classList.remove('open');
      backdrop.classList.remove('open');
      document.body.style.overflow = '';
    }
    function openMenu() {
      toggle.setAttribute('aria-expanded', 'true');
      navLinks.classList.add('open');
      backdrop.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
    toggle.addEventListener('click', function () {
      var isOpen = toggle.getAttribute('aria-expanded') === 'true';
      isOpen ? closeMenu() : openMenu();
    });
    backdrop.addEventListener('click', closeMenu);
    navLinks.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', closeMenu);
    });
    window.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMenu();
    });
  }
})();
