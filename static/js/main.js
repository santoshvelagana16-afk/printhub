// PrintHub – Main JS

document.addEventListener('DOMContentLoaded', function () {
  // Auto-dismiss alerts after 5s
  setTimeout(() => {
    document.querySelectorAll('.ph-alert').forEach(el => {
      try { new bootstrap.Alert(el).close(); } catch(e){}
    });
  }, 5000);

  // Password toggle
  window.togglePwd = function(id, btn) {
    const inp = document.getElementById(id);
    if (!inp) return;
    const show = inp.type === 'password';
    inp.type = show ? 'text' : 'password';
    btn.innerHTML = show ? '<i class="bi bi-eye-slash"></i>' : '<i class="bi bi-eye"></i>';
  };

  // Active nav link
  const path = window.location.pathname;
  document.querySelectorAll('.ph-navbar .nav-link').forEach(a => {
    if (a.getAttribute('href') === path) a.classList.add('active');
  });

  // Scroll reveal
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.style.opacity = '1';
        e.target.style.transform = 'translateY(0)';
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.08 });

  document.querySelectorAll('.step-card, .svc-card, .why-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(18px)';
    el.style.transition = 'opacity .45s ease, transform .45s ease';
    io.observe(el);
  });
});
