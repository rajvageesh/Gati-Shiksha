// =========================================
// GATI SHIKSHA — GLOBAL JAVASCRIPT
// =========================================


// ---------- NAVBAR ----------

const navbar = document.getElementById("mainNavbar");
const menuButton = document.getElementById("menuButton");
const mobileMenu = document.getElementById("mobileMenu");


// Navbar background on scroll

window.addEventListener("scroll", () => {

    if (window.scrollY > 20) {
        navbar.classList.add("scrolled");
    } else {
        navbar.classList.remove("scrolled");
    }

});


// Mobile menu

if (menuButton && mobileMenu) {

    menuButton.addEventListener("click", () => {

        const expanded = menuButton.getAttribute("aria-expanded") === "true";
        mobileMenu.classList.toggle("active");
        menuButton.setAttribute("aria-expanded", String(!expanded));

    });


    // Close menu after clicking a link

    const mobileLinks =
        mobileMenu.querySelectorAll("a");

    mobileLinks.forEach(link => {

        link.addEventListener("click", () => {

            mobileMenu.classList.remove("active");
            menuButton.setAttribute("aria-expanded", "false");

        });

    });

}

// ---------- ABOUT SECTION TABS ----------

const tabButtons = document.querySelectorAll('.mv-tab-btn');
const tabPanels = document.querySelectorAll('.mv-panel');

if (tabButtons.length > 0 && tabPanels.length > 0) {
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons and panels
            tabButtons.forEach(btn => {
                btn.classList.remove('active');
                btn.setAttribute('aria-selected', 'false');
            });
            tabPanels.forEach(panel => panel.classList.remove('active'));

            // Add active class to clicked button
            button.classList.add('active');
            button.setAttribute('aria-selected', 'true');

            // Add active class to corresponding panel
            const tabId = button.getAttribute('data-tab');
            const targetPanel = document.getElementById(`panel-${tabId}`);
            if (targetPanel) {
                targetPanel.classList.add('active');
            }
        });
    });
}


// ---------- CONTACT FORM INLINE VALIDATION ----------

(function () {
    const form = document.getElementById('inquiryForm');
    if (!form) return;

    const rules = {
        name: {
            validate: v => v.trim().length >= 2,
            msg: 'Please enter your full name (at least 2 characters).'
        },
        email: {
            validate: v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()),
            msg: 'Please enter a valid email address (e.g. you@school.in).'
        },
        mobile: {
            validate: v => {
                let cleaned = v.replace(/[\s\-\(\)\+]/g, '');
                if (cleaned.startsWith('91') && cleaned.length === 12) cleaned = cleaned.slice(2);
                if (cleaned.startsWith('0') && cleaned.length === 11) cleaned = cleaned.slice(1);
                return /^[6-9]\d{9}$/.test(cleaned);
            },
            msg: 'Please enter a valid 10-digit mobile number starting with 6, 7, 8, or 9.'
        },
        role: {
            validate: v => v !== '',
            msg: 'Please select your role so we can respond appropriately.'
        },
        message: {
            validate: v => v.trim().length >= 10,
            msg: 'Please write a short message (at least 10 characters).'
        }
    };

    function validateField(fieldId) {
        const field = form.querySelector('#' + fieldId);
        const errorEl = form.querySelector('#' + fieldId + '-error');
        if (!field || !rules[fieldId]) return true;

        const valid = rules[fieldId].validate(field.value);
        field.classList.toggle('is-invalid', !valid);
        if (errorEl) errorEl.textContent = valid ? '' : rules[fieldId].msg;
        return valid;
    }

    // Real-time validation on blur
    Object.keys(rules).forEach(id => {
        const el = form.querySelector('#' + id);
        if (!el) return;
        el.addEventListener('blur', () => validateField(id));
        el.addEventListener('input', () => {
            if (el.classList.contains('is-invalid')) validateField(id);
        });
    });

    // Full validation on submit
    form.addEventListener('submit', e => {
        let allValid = true;
        Object.keys(rules).forEach(id => {
            if (!validateField(id)) allValid = false;
        });
        if (!allValid) {
            e.preventDefault();
            // Focus first invalid field
            const first = form.querySelector('.is-invalid');
            if (first) first.focus();
        }
    });
})();


