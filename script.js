// Chase Golden Globe — shared site behaviour (v4, September 2026)

(function () {
  function each(list, fn) { for (var i = 0; i < list.length; i++) fn(list[i], i); }
  function dict() {
    var lang = document.documentElement.getAttribute('lang') || 'en';
    return (typeof CGG_TRANSLATIONS !== 'undefined' && CGG_TRANSLATIONS[lang]) || {};
  }
  function t(key, fallback) { return dict()[key] || fallback; }

  document.addEventListener('DOMContentLoaded', function () {

    // Sticky nav elevation
    var nav = document.getElementById('siteNav');
    if (nav) {
      var onScroll = function () { nav.classList.toggle('scrolled', window.scrollY > 20); };
      onScroll();
      window.addEventListener('scroll', onScroll, { passive: true });
    }

    // Mobile menu — expands in place below the nav bar
    var toggle = document.getElementById('navToggle');
    var links = document.getElementById('navLinks');
    if (toggle && links) {
      var setLabel = function (open) {
        toggle.setAttribute('data-i18n', open ? 'nav.close' : 'nav.menu');
        toggle.textContent = t(open ? 'nav.close' : 'nav.menu', open ? 'Close' : 'Menu');
      };
      var closeMenu = function () {
        links.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
        setLabel(false);
      };
      toggle.addEventListener('click', function () {
        var open = links.classList.toggle('open');
        toggle.setAttribute('aria-expanded', String(open));
        setLabel(open);
      });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenu(); });
      each(links.querySelectorAll('a'), function (a) { a.addEventListener('click', closeMenu); });
    }

    // About — chapter timeline (proper tabs: arrow keys move between tabs)
    var tablist = document.querySelector('.timeline[role="tablist"]');
    if (tablist) {
      var tabs = tablist.querySelectorAll('[role="tab"]');
      var panels = document.querySelectorAll('.chapter[role="tabpanel"]');
      var select = function (tab, focus) {
        each(tabs, function (x) {
          var on = x === tab;
          x.classList.toggle('active', on);
          x.setAttribute('aria-selected', String(on));
          x.setAttribute('tabindex', on ? '0' : '-1');
        });
        each(panels, function (p) {
          var on = p.id === tab.getAttribute('aria-controls');
          p.hidden = !on;
          p.classList.toggle('active', on);
        });
        if (focus) tab.focus();
      };
      each(tabs, function (tab, i) {
        tab.addEventListener('click', function () { select(tab, false); });
        tab.addEventListener('keydown', function (e) {
          var n = null;
          if (e.key === 'ArrowRight' || e.key === 'ArrowDown') n = tabs[(i + 1) % tabs.length];
          if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') n = tabs[(i - 1 + tabs.length) % tabs.length];
          if (e.key === 'Home') n = tabs[0];
          if (e.key === 'End') n = tabs[tabs.length - 1];
          if (n) { e.preventDefault(); select(n, true); }
        });
      });
      select(tablist.querySelector('[aria-selected="true"]') || tabs[0], false);
    }

    // Presence — highlight a country on the map and show its card
    var map = document.getElementById('worldMap');
    var card = document.getElementById('countryCard');
    var list = document.getElementById('countryList');
    if (map && card && list) {
      var paths = map.querySelectorAll('.country.hi');
      var roleEl = card.querySelector('[data-role]');
      var nameEl = card.querySelector('[data-name]');
      var bodyEl = card.querySelector('[data-body]');
      var current = 'Australia';
      var render = function () {
        var key = current.replace(/ /g, '');
        each(paths, function (p) { p.classList.toggle('sel', p.getAttribute('data-name') === current); });
        each(list.querySelectorAll('button'), function (b) {
          var on = b.getAttribute('data-country') === current;
          b.classList.toggle('sel', on);
          b.setAttribute('aria-pressed', String(on));
        });
        roleEl.textContent = t('pres.c.' + key + '.role', roleEl.getAttribute('data-fallback-role') || '');
        nameEl.textContent = t('country.' + current, current);
        bodyEl.textContent = t('pres.c.' + key + '.body', '');
      };
      var pick = function (name) { current = name; render(); };
      each(list.querySelectorAll('button'), function (b) {
        b.addEventListener('click', function () { pick(b.getAttribute('data-country')); });
      });
      each(paths, function (p) {
        p.setAttribute('tabindex', '0');
        p.setAttribute('role', 'button');
        p.setAttribute('aria-label', p.getAttribute('data-name'));
        p.addEventListener('click', function () { pick(p.getAttribute('data-name')); });
        p.addEventListener('keydown', function (e) {
          if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(p.getAttribute('data-name')); }
        });
      });
      document.addEventListener('cgg:lang', render);
      render();
    }

    // Contact — copy email
    var copy = document.getElementById('copyEmail');
    if (copy) {
      copy.addEventListener('click', function () {
        var email = copy.getAttribute('data-email');
        var done = function () {
          copy.textContent = t('contact.copied', 'Copied');
          setTimeout(function () { copy.textContent = t('contact.copy', 'Copy'); }, 1600);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(email).then(done, function () {});
        }
      });
    }
  });
})();
