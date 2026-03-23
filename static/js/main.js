/* ═══════════════════════════════════════════════════════════════
   EngiConnect — main.js
   Single JS file for the entire project
   ═══════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', function () {

  // ── 1. Sidebar collapse ──────────────────────────────────────
  const sidebar      = document.getElementById('sidebar');
  const toggleBtn    = document.getElementById('sidebarToggle');
  const mobileToggle = document.getElementById('mobileSidebarToggle');

  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('sidebar--collapsed');
      localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('sidebar--collapsed'));
    });
  }

  if (mobileToggle && sidebar) {
    mobileToggle.addEventListener('click', () => {
      sidebar.classList.toggle('sidebar--mobile-open');
    });
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
      if (
        sidebar.classList.contains('sidebar--mobile-open') &&
        !sidebar.contains(e.target) &&
        e.target !== mobileToggle
      ) {
        sidebar.classList.remove('sidebar--mobile-open');
      }
    });
  }

  // Restore sidebar collapsed state
  if (sidebar && localStorage.getItem('sidebarCollapsed') === 'true') {
    sidebar.classList.add('sidebar--collapsed');
  }

  // ── 2. Active sidebar link highlighting ─────────────────────
  document.querySelectorAll('.sidebar__link').forEach(link => {
    const href = link.getAttribute('href');
    if (href && (window.location.pathname === href || window.location.pathname.startsWith(href + '/'))) {
      link.classList.add('sidebar__link--active');
    }
  });

  // ── 3. Toast auto-dismiss ────────────────────────────────────
  document.querySelectorAll('.toast').forEach(toast => {
    setTimeout(() => { toast.style.opacity = '0'; }, 4500);
    setTimeout(() => { toast.remove(); }, 5000);
  });

  // ── 4. Form enhancements ─────────────────────────────────────

  // Mark invalid django fields with CSS class
  document.querySelectorAll('.errorlist').forEach(errList => {
    const field = errList.previousElementSibling;
    if (field && field.classList.contains('form-control')) {
      field.classList.add('form-control--error');
    }
  });

  // Password strength meter (used on register pages)
  const pwdInput = document.getElementById('id_password1');
  const pwdMeter = document.getElementById('passwordStrength');
  if (pwdInput && pwdMeter) {
    pwdInput.addEventListener('input', () => {
      const val = pwdInput.value;
      let strength = 0;
      if (val.length >= 8)           strength++;
      if (/[A-Z]/.test(val))         strength++;
      if (/[0-9]/.test(val))         strength++;
      if (/[^A-Za-z0-9]/.test(val))  strength++;
      const labels  = ['', 'Weak', 'Fair', 'Good', 'Strong'];
      const colors  = ['', '#dc2626', '#d97706', '#0ea271', '#1a56db'];
      pwdMeter.style.width  = (strength * 25) + '%';
      pwdMeter.style.background = colors[strength];
      const label = document.getElementById('passwordStrengthLabel');
      if (label) {
        label.textContent = labels[strength];
        label.style.color = colors[strength];
      }
    });
  }

  // Confirm password match indicator
  const pwd2 = document.getElementById('id_password2');
  if (pwd2 && pwdInput) {
    pwd2.addEventListener('input', () => {
      if (pwd2.value && pwd2.value === pwdInput.value) {
        pwd2.style.borderColor = 'var(--color-success)';
      } else if (pwd2.value) {
        pwd2.style.borderColor = 'var(--color-danger)';
      } else {
        pwd2.style.borderColor = '';
      }
    });
  }

  // ── 5. File input preview (for avatar uploads) ───────────────
  const avatarInput   = document.getElementById('id_avatar');
  const avatarPreview = document.getElementById('avatarPreview');
  if (avatarInput && avatarPreview) {
    avatarInput.addEventListener('change', () => {
      const file = avatarInput.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = e => { avatarPreview.src = e.target.result; };
        reader.readAsDataURL(file);
      }
    });
  }

  // ── 6. Confirm dialogs ───────────────────────────────────────
  document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', (e) => {
      const msg = el.getAttribute('data-confirm') || 'Are you sure?';
      if (!confirm(msg)) e.preventDefault();
    });
  });

  // ── 7. Multi-step form (used in job intake) ──────────────────
  // Steps are controlled by data-step on .form-step elements
  const steps     = document.querySelectorAll('.form-step');
  const nextBtns  = document.querySelectorAll('[data-next-step]');
  const prevBtns  = document.querySelectorAll('[data-prev-step]');
  let currentStep = 0;

  function showStep(idx) {
    steps.forEach((step, i) => {
      step.style.display = i === idx ? 'block' : 'none';
    });
    // Update step indicator dots
    document.querySelectorAll('.step').forEach((dot, i) => {
      dot.classList.toggle('step--active', i === idx);
      dot.classList.toggle('step--done',   i < idx);
    });
  }

  if (steps.length > 0) {
    showStep(0);
    nextBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        if (currentStep < steps.length - 1) {
          currentStep++;
          showStep(currentStep);
          window.scrollTo(0, 0);
        }
      });
    });
    prevBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        if (currentStep > 0) {
          currentStep--;
          showStep(currentStep);
        }
      });
    });
  }

  // ── 8. Simple dropdown menus ─────────────────────────────────
  document.querySelectorAll('[data-dropdown-toggle]').forEach(trigger => {
    const targetId = trigger.getAttribute('data-dropdown-toggle');
    const menu = document.getElementById(targetId);
    if (!menu) return;
    trigger.addEventListener('click', (e) => {
      e.stopPropagation();
      menu.classList.toggle('dropdown--open');
    });
    document.addEventListener('click', () => menu.classList.remove('dropdown--open'));
  });

  // ── 9. Search/filter tables ──────────────────────────────────
  const tableSearch = document.getElementById('tableSearch');
  if (tableSearch) {
    const tableBody = document.querySelector('[data-searchable]');
    if (tableBody) {
      tableSearch.addEventListener('input', () => {
        const q = tableSearch.value.toLowerCase();
        tableBody.querySelectorAll('tr').forEach(row => {
          row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
        });
      });
    }
  }

  // ── 10. Quote calculator (used in jobs intake) ───────────────
  // This gets activated by the jobs app templates.
  // The function is exposed globally for reuse.
  window.EngiConnect = window.EngiConnect || {};

  window.EngiConnect.calculateQuote = function (discipline, floors, area) {
    const baseRates = {
      structural: 15000,
      civil:      18000,
      plb:        12000,
      mep:        20000,
      environmental: 22000,
      other:      10000,
    };
    const base   = baseRates[discipline] || 10000;
    const floorMult  = 1 + ((parseInt(floors) || 1) - 1) * 0.3;
    const areaMult   = area > 200 ? 1.5 : area > 100 ? 1.2 : 1;
    const low  = Math.round(base * floorMult * areaMult);
    const high = Math.round(low * 1.4);
    return { low, high };
  };

});