// Chase Golden Globe — shared site behaviour

document.addEventListener('DOMContentLoaded', () => {

  // Sticky nav background after scroll
  const nav = document.getElementById('siteNav');
  const onScroll = () => {
    if (window.scrollY > 40) nav.classList.add('scrolled');
    else nav.classList.remove('scrolled');
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

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

  // Accordion (capabilities)
  document.querySelectorAll('.accordion-item').forEach(item => {
    const trigger = item.querySelector('.accordion-trigger');
    trigger.addEventListener('click', () => {
      const isOpen = item.classList.toggle('open');
      trigger.setAttribute('aria-expanded', String(isOpen));
    });
  });
});
