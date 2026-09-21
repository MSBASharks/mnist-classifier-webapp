document.addEventListener('DOMContentLoaded', function () {
    var toggle = document.getElementById('navToggle');
    var sidebar = document.getElementById('sidebar');
    var backdrop = document.getElementById('navBackdrop');

    // These only exist for logged-in users (see base.html) -- bail quietly
    // on pages where there's nothing to toggle, e.g. the login page.
    if (!toggle || !sidebar || !backdrop) {
        return;
    }

    function openMenu() {
        sidebar.classList.add('open');
        backdrop.classList.add('open');
        toggle.setAttribute('aria-expanded', 'true');
    }

    function closeMenu() {
        sidebar.classList.remove('open');
        backdrop.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
    }

    function toggleMenu() {
        if (sidebar.classList.contains('open')) {
            closeMenu();
        } else {
            openMenu();
        }
    }

    toggle.addEventListener('click', toggleMenu);
    backdrop.addEventListener('click', closeMenu);

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            closeMenu();
        }
    });
});
