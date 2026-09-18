// Chase Golden Globe — shared site behaviour (v5, September 2026)

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
        if (nav) nav.classList.remove('open-bar');
        toggle.setAttribute('aria-expanded', 'false');
        setLabel(false);
      };
      toggle.addEventListener('click', function () {
        var open = links.classList.toggle('open');
        toggle.setAttribute('aria-expanded', String(open));
        if (nav) nav.classList.toggle('open-bar', open);
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
        tablist.style.setProperty('--i', String([].indexOf.call(tabs, tab)));
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
      var render = function (animate) {
        if (animate === true) { card.classList.remove('swap'); void card.offsetWidth; card.classList.add('swap'); }
        var key = current.replace(/ /g, '');
        each(paths, function (p) {
          var n = p.getAttribute('data-name');
          p.classList.toggle('sel', n === current);
          p.setAttribute('aria-label', t('country.' + n, n));
          p.setAttribute('aria-pressed', String(n === current));
        });
        each(list.querySelectorAll('button'), function (b) {
          var on = b.getAttribute('data-country') === current;
          b.classList.toggle('sel', on);
          b.setAttribute('aria-pressed', String(on));
        });
        roleEl.textContent = t('pres.c.' + key + '.role', roleEl.getAttribute('data-fallback-role') || '');
        nameEl.textContent = t('country.' + current, current);
        bodyEl.textContent = t('pres.c.' + key + '.body', '');
      };
      var pick = function (name) { if (name === current) return; current = name; render(true); };
      each(list.querySelectorAll('button'), function (b) {
        b.addEventListener('click', function () { pick(b.getAttribute('data-country')); });
      });
      each(paths, function (p) {
        p.setAttribute('tabindex', '0');
        p.setAttribute('role', 'button');
        p.addEventListener('click', function () { pick(p.getAttribute('data-name')); });
        p.addEventListener('keydown', function (e) {
          if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(p.getAttribute('data-name')); }
        });
      });
      document.addEventListener('cgg:lang', function () { render(false); });
      render(false);
    }

    // Copy email (Contact panel and footer). Falls back to selecting the address if the clipboard is blocked.
    each(document.querySelectorAll('.copybtn[data-email]'), function (btn) {
      btn.addEventListener('click', function () {
        var email = btn.getAttribute('data-email');
        var flash = function (key, fallback) {
          var msg = t(key, fallback);
          if (/Mac|iPhone|iPad/.test(navigator.platform || '')) msg = msg.replace('Ctrl+C', '⌘C');
          btn.textContent = msg;
          btn.classList.add('done');
          clearTimeout(btn._reset);
          btn._reset = setTimeout(function () { btn.textContent = t('contact.copy', 'Copy'); btn.classList.remove('done'); }, 1800);
        };
        var fail = function () {
          var link = btn.parentNode.querySelector('a[href^="mailto:"]');
          if (link && window.getSelection) {
            var r = document.createRange(); r.selectNodeContents(link);
            var sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r);
          }
          flash('contact.copyfail', 'Press Ctrl+C');
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(email).then(function () { flash('contact.copied', 'Copied'); }, fail);
        } else { fail(); }
      });
    });

    // Enquiry emails open with a short, localised template
    var mailtos = document.querySelectorAll('a[data-mailto]');
    var setMail = function () {
      var q = '?subject=' + encodeURIComponent(t('mail.subject', 'Enquiry: [project name]')) +
              '&body=' + encodeURIComponent(t('mail.body', ''));
      each(mailtos, function (a) { a.setAttribute('href', 'mailto:info@chasegoldenglobe.com.au' + q); });
    };
    if (mailtos.length) { setMail(); document.addEventListener('cgg:lang', setMail); }

    var calm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Primary buttons: the lighter fill blooms from where the pointer enters
    each(document.querySelectorAll('.btn-brass'), function (b) {
      b.addEventListener('pointerenter', function (e) {
        var r = b.getBoundingClientRect();
        b.style.setProperty('--x', (e.clientX - r.left) + 'px');
        b.style.setProperty('--y', (e.clientY - r.top) + 'px');
      });
    });

    // Numbers count up to the figure already printed in the markup (never past it)
    var countUp = function (root) {
      each(root.querySelectorAll('[data-count]'), function (el) {
        if (el.getAttribute('data-done')) return;
        el.setAttribute('data-done', '1');
        var target = parseFloat(el.getAttribute('data-count'));
        var dp = parseInt(el.getAttribute('data-dp') || '0', 10);
        var pre = el.getAttribute('data-prefix') || '', suf = el.getAttribute('data-suffix') || '';
        var t0 = null, dur = 1900, wait = 320;
        var step = function (t) {
          if (t0 === null) t0 = t + wait;
          if (t < t0) { requestAnimationFrame(step); return; }
          var k = Math.min(1, (t - t0) / dur);
          var eased = 1 - Math.pow(1 - k, 3);
          el.textContent = pre + (target * eased).toFixed(dp) + suf;
          if (k < 1) requestAnimationFrame(step);
        };
        el.textContent = pre + (0).toFixed(dp) + suf;
        requestAnimationFrame(step);
      });
    };

    // The presence map fills in the order the house grew: Sydney, then where it began, then the regions
    var REGIONS = [
      ['Head office', ['Australia']],
      ['Southeast Asia', ['Indonesia']],
      ['The Gulf', ['Saudi Arabia', 'Qatar', 'United Arab Emirates']],
      ['North Africa', ['Algeria', 'Egypt']],
      ['Europe', ['United Kingdom', 'Switzerland', 'Luxembourg']]
    ];
    var playMap = function (svg, withRoute) {
      if (svg.getAttribute('data-played')) return;
      svg.setAttribute('data-played', '1');
      var box = svg.closest('.map-anim') || svg;
      var order = [], i;
      for (i = 0; i < REGIONS.length; i++) order = order.concat(REGIONS[i][1]);
      each(order, function (name, n) {
        setTimeout(function () {
          each(svg.querySelectorAll('.country.hi'), function (p) {
            if (p.getAttribute('data-name') === name) p.classList.add('lit');
          });
        }, 260 + n * 170);
      });
      if (!withRoute) return;
      var find = function (name) {
        var hit = null;
        each(svg.querySelectorAll('.country.hi'), function (p) { if (p.getAttribute('data-name') === name) hit = p; });
        return hit;
      };
      var from = find('Indonesia'), to = find('Australia');
      if (from && to) {
        var a = from.getBBox(), c = to.getBBox();
        // eastern Java out, Sydney in; the arc bows east so it stays off the land
        var x1 = a.x + a.width * 0.66, y1 = a.y + a.height * 0.78;
        var x2 = c.x + c.width * 0.9, y2 = c.y + c.height * 0.52;
        var ns = 'http://www.w3.org/2000/svg';
        var path = document.createElementNS(ns, 'path');
        path.setAttribute('class', 'trade-route');
        var span = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
        path.setAttribute('d', 'M' + x1 + ' ' + y1 + ' Q ' + (Math.max(x1, x2) + span * 0.42) + ' ' + ((y1 + y2) / 2 - span * 0.1) + ' ' + x2 + ' ' + y2);
        svg.appendChild(path);
        each([[x1, y1, ''], [x2, y2, 'b']], function (pt) {
          var dot = document.createElementNS(ns, 'circle');
          dot.setAttribute('class', 'trade-port ' + pt[2]);
          dot.setAttribute('cx', pt[0]); dot.setAttribute('cy', pt[1]); dot.setAttribute('r', '2.4');
          svg.appendChild(dot);
        });
        try { path.style.setProperty('--len', Math.ceil(path.getTotalLength()) + ''); } catch (e) {}
        setTimeout(function () { box.classList.add('routed'); }, 500);
      }
    };

    // Quiet scroll reveal, only for blocks that start below the fold; content stays visible without JS
    if (calm) {
      each(document.querySelectorAll('.map-anim'), function (m) { m.classList.add('routed'); });
      each(document.querySelectorAll('#worldMap .country.hi, #worldMapMini .country.hi'), function (p) { p.classList.add('lit'); });
    }
    if (!calm && 'IntersectionObserver' in window) {
      each(document.querySelectorAll('.map-block, .map-mini'), function (m) { m.classList.add('map-anim'); });
      var mapIo = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (!e.isIntersecting) return;
          mapIo.unobserve(e.target);
          playMap(e.target, e.target.id === 'worldMap');
        });
      }, { threshold: .25 });
      each(document.querySelectorAll('#worldMap, #worldMapMini'), function (svg) { mapIo.observe(svg); });

      each(document.querySelectorAll('.sector-list, .strip, .entries, .clist, .steps'), function (l) { l.classList.add('stagger'); });

      var targets = document.querySelectorAll('main section .wrap > *:not(.sr-only), main .hero-stats .stats, main .sector-list, main .strip, main .entries, main .clist');
      var io = new IntersectionObserver(function (entries) {
        each(entries, function (en) {
          if (!en.isIntersecting) return;
          en.target.classList.add('in');
          io.unobserve(en.target);
          countUp(en.target);
        });
      }, { rootMargin: '0px 0px -8% 0px' });
      each(targets, function (el) {
        if (el.getBoundingClientRect().top > window.innerHeight) {
          el.classList.add(el.matches('figure, .office3, .geo-photo, .plate, img') ? 'rv-wipe' : 'rv');
          io.observe(el);
        } else {
          // already on screen at load: show it straight away, so a staggered
          // list above the fold is never left hidden
          el.classList.add('in');
        }
      });
      each(document.querySelectorAll('.stagger'), function (el) {
        if (el.getBoundingClientRect().top <= window.innerHeight) el.classList.add('in');
      });
      // figures already on screen still get their numbers animated
      var statsIo = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { statsIo.unobserve(e.target); countUp(e.target); } });
      }, { threshold: .4 });
      each(document.querySelectorAll('.hero-stats, .map-stats'), function (el) { statsIo.observe(el); });
      window.addEventListener('beforeprint', function () { each(targets, function (el) { el.classList.add('in'); }); });
    }
  });
})();
