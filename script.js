// Chase Golden Globe — shared site behaviour

document.addEventListener('DOMContentLoaded', () => {

  // Mobile menu
  const toggle = document.getElementById('navToggle');
  const links = document.getElementById('navLinks');
  const backdrop = document.getElementById('navBackdrop');
  if (toggle && links && backdrop) {
    const closeMenu = () => {
      links.classList.remove('open');
      backdrop.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    };
    toggle.addEventListener('click', () => {
      const isOpen = links.classList.toggle('open');
      backdrop.classList.toggle('open', isOpen);
      toggle.setAttribute('aria-expanded', String(isOpen));
    });
    backdrop.addEventListener('click', closeMenu);
    links.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
  }

  // Chapter axis (Origin / The Shift / Today)
  const chapterNav = document.querySelector('.chapter-nav');
  if (chapterNav) {
    const buttons = chapterNav.querySelectorAll('button');
    const panels = document.querySelectorAll('.chapter-panel');
    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        const target = btn.getAttribute('data-chapter');
        buttons.forEach(b => b.classList.toggle('active', b === btn));
        panels.forEach(p => p.classList.toggle('active', p.getAttribute('data-chapter') === target));
      });
    });
  }

  // Capability tiles (expand in place)
  document.querySelectorAll('.tile').forEach(tile => {
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
    const countries = mapVisual.querySelectorAll('.country.hi');
    countries.forEach(path => {
      path.addEventListener('mousemove', (e) => {
        tooltip.textContent = path.getAttribute('data-name');
        tooltip.style.left = (e.clientX + 14) + 'px';
        tooltip.style.top = (e.clientY + 14) + 'px';
        tooltip.classList.add('show');
      });
      path.addEventListener('mouseleave', () => {
        tooltip.classList.remove('show');
      });
    });
  }
});
