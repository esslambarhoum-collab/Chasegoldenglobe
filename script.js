// Chase Golden Globe — shared site behaviour

function cggEach(list, fn) {
  for (var i = 0; i < list.length; i++) fn(list[i], i);
}

document.addEventListener('DOMContentLoaded', () => {

  // Sticky nav elevation after scroll
  const nav = document.getElementById('siteNav');
  if (nav) {
    const onScroll = () => {
      if (window.scrollY > 20) nav.classList.add('scrolled');
      else nav.classList.remove('scrolled');
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // Mobile menu — expands in place below the nav (no slide-in panel, no
  // full-screen overlay). Toggle is a text label ("Menu"/"Close"), translated
  // via the same dictionary the language switcher uses.
  const toggle = document.getElementById('navToggle');
  const links = document.getElementById('navLinks');
  if (toggle && links) {
    const currentDict = () => {
      const lang = document.documentElement.getAttribute('lang') || 'en';
      return (typeof CGG_TRANSLATIONS !== 'undefined' && CGG_TRANSLATIONS[lang]) || {};
    };
    const setToggleLabel = (isOpen) => {
      const key = isOpen ? 'nav.close' : 'nav.menu';
      const dict = currentDict();
      toggle.setAttribute('data-i18n', key);
      toggle.textContent = dict[key] || (isOpen ? 'Close' : 'Menu');
    };
    const closeMenu = () => {
      links.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      setToggleLabel(false);
    };
    toggle.addEventListener('click', () => {
      const isOpen = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(isOpen));
      setToggleLabel(isOpen);
    });
    cggEach(links.querySelectorAll('a'), (a) => a.addEventListener('click', closeMenu));
  }

  // Capability tiles (expand in place)
  cggEach(document.querySelectorAll('.tile'), (tile) => {
    const trigger = tile.querySelector('.tile-trigger');
    trigger.addEventListener('click', () => {
      const isOpen = tile.classList.toggle('open');
      trigger.setAttribute('aria-expanded', String(isOpen));
    });
  });

  // World map hover tooltip
  const mapVisual = document.querySelector('.map-visual');
  if (mapVisual) {
    let tooltip = document.querySelector('.map-tooltip');
    if (!tooltip) {
      tooltip = document.createElement('div');
      tooltip.className = 'map-tooltip';
      document.body.appendChild(tooltip);
    }
    const svg = document.getElementById('worldMap');
    const resetBtn = document.getElementById('mapReset');
    const defaultViewBox = svg ? svg.getAttribute('data-default-viewbox') : null;

    const zoomToBbox = (bbox) => {
      if (!svg || !bbox) return;
      svg.setAttribute('viewBox', bbox.split(',').join(' '));
      if (resetBtn) resetBtn.classList.add('show');
    };
    const resetZoom = () => {
      if (!svg || !defaultViewBox) return;
      svg.setAttribute('viewBox', defaultViewBox);
      if (resetBtn) resetBtn.classList.remove('show');
    };

    const countries = mapVisual.querySelectorAll('.country.hi');
    cggEach(countries, (path) => {
      path.addEventListener('mousemove', (e) => {
        const rawName = path.getAttribute('data-name');
        let label = rawName;
        try {
          const lang = document.documentElement.getAttribute('lang') || 'en';
          const dict = (typeof CGG_TRANSLATIONS !== 'undefined' && CGG_TRANSLATIONS[lang]) || {};
          if (dict['country.' + rawName]) label = dict['country.' + rawName];
        } catch (e) {}
        tooltip.textContent = label;
        tooltip.style.left = (e.clientX + 14) + 'px';
        tooltip.style.top = (e.clientY + 14) + 'px';
        tooltip.classList.add('show');
      });
      path.addEventListener('mouseleave', () => {
        tooltip.classList.remove('show');
      });
      path.addEventListener('click', () => {
        zoomToBbox(path.getAttribute('data-bbox'));
      });
    });

    if (resetBtn) resetBtn.addEventListener('click', resetZoom);

    cggEach(document.querySelectorAll('.country-list button'), (btn) => {
      btn.addEventListener('click', () => {
        const name = btn.getAttribute('data-country');
        const path = mapVisual.querySelector('.country.hi[data-name="' + name + '"]');
        if (path) zoomToBbox(path.getAttribute('data-bbox'));
      });
    });
  }
});
