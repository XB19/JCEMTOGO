document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('admin-menu-toggle');
  const sidebar = document.getElementById('admin-sb');
  const overlay = document.getElementById('admin-overlay');

  if (!toggle || !sidebar || !overlay) return;

  function closeMenu() {
    sidebar.classList.remove('open');
    overlay.classList.remove('show');
    toggle.setAttribute('aria-expanded', 'false');
  }

  function toggleMenu() {
    const isOpen = sidebar.classList.toggle('open');
    overlay.classList.toggle('show', isOpen);
    toggle.setAttribute('aria-expanded', String(isOpen));
  }

  toggle.addEventListener('click', toggleMenu);
  overlay.addEventListener('click', closeMenu);
  sidebar.querySelectorAll('.anav-item').forEach((link) => {
    link.addEventListener('click', closeMenu);
  });
});
