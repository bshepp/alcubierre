/* Light/dark theme toggle. Persists choice in localStorage; respects
   prefers-color-scheme on first load. Auto-injects a button into
   .topbar-right so individual pages don't need new markup. */
(function () {
  var STORAGE_KEY = 'alcubierre-theme';
  var root = document.documentElement;

  function getInitial() {
    var saved = null;
    try { saved = localStorage.getItem(STORAGE_KEY); } catch (e) {}
    if (saved === 'light' || saved === 'dark') return saved;
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) return 'light';
    return 'dark';
  }

  function apply(theme) {
    root.setAttribute('data-theme', theme);
    var btn = document.querySelector('.theme-toggle');
    if (btn) btn.textContent = theme === 'light' ? '☾ Dark' : '☀ Light';
    try { localStorage.setItem(STORAGE_KEY, theme); } catch (e) {}
  }

  // Apply ASAP to avoid flash
  apply(getInitial());

  function inject() {
    var host = document.querySelector('.topbar-right');
    if (!host || host.querySelector('.theme-toggle')) return;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'theme-toggle';
    btn.setAttribute('aria-label', 'Toggle light/dark theme');
    btn.textContent = root.getAttribute('data-theme') === 'light' ? '☾ Dark' : '☀ Light';
    btn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      apply(next);
    });
    host.insertBefore(btn, host.firstChild);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject);
  } else {
    inject();
  }
})();
