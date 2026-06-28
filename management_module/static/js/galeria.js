document.addEventListener('DOMContentLoaded', function () {
  /* ===== Header: Hamburguer ===== */
  var hamburger = document.getElementById('hamburger');
  var mainNav = document.getElementById('mainNav');

  if (hamburger && mainNav) {
    hamburger.addEventListener('click', function () {
      hamburger.classList.toggle('active');
      mainNav.classList.toggle('open');
    });
  }

  /* ===== Hero Slider ===== */
  var slider = document.getElementById('heroSlider');
  if (slider) {
    var slides = slider.querySelectorAll('.hero-slide');
    var dots = slider.querySelectorAll('.hero-dot');
    var current = 0;
    var interval;

    function goToSlide(index) {
      slides.forEach(function (s) { s.classList.remove('active'); });
      dots.forEach(function (d) { d.classList.remove('active'); });
      slides[index].classList.add('active');
      dots[index].classList.add('active');
      current = index;
    }

    function nextSlide() {
      goToSlide((current + 1) % slides.length);
    }

    dots.forEach(function (dot) {
      dot.addEventListener('click', function () {
        goToSlide(parseInt(this.dataset.slide));
        clearInterval(interval);
        interval = setInterval(nextSlide, 5000);
      });
    });

    interval = setInterval(nextSlide, 5000);
  }

  /* ===== Gallery: Lightbox ===== */
  var lightbox = document.getElementById('lightbox');
  var lightboxImg = document.getElementById('lightboxImg');
  var lightboxTitulo = document.getElementById('lightboxTitulo');
  var lightboxSignatura = document.getElementById('lightboxSignatura');
  var lightboxAutor = document.getElementById('lightboxAutor');
  var lightboxFondo = document.getElementById('lightboxFondo');
  var lightboxAnio = document.getElementById('lightboxAnio');
  var lightboxColeccion = document.getElementById('lightboxColeccion');
  var lightboxLugar = document.getElementById('lightboxLugar');
  var lightboxDescripcion = document.getElementById('lightboxDescripcion');
  var lightboxClose = document.getElementById('lightboxClose');
  var lightboxPrev = document.getElementById('lightboxPrev');
  var lightboxNext = document.getElementById('lightboxNext');

  if (lightbox) {
    var cards = document.querySelectorAll('.gallery-card');
    var currentIndex = 0;

    function openLightbox(index) {
      var card = cards[index];
      if (!card) return;
      currentIndex = index;
      lightboxImg.src = card.dataset.fotoUrl;
      lightboxImg.alt = card.dataset.titulo;
      lightboxTitulo.textContent = card.dataset.titulo;
      lightboxSignatura.textContent = card.dataset.signatura;
      lightboxAutor.textContent = card.dataset.autor || '—';
      lightboxFondo.textContent = card.dataset.autorFondo || '—';
      lightboxAnio.textContent = card.dataset.anio || '—';
      lightboxColeccion.textContent = card.dataset.coleccion || '—';
      lightboxLugar.textContent = card.dataset.lugar || '—';
      lightboxDescripcion.textContent = card.dataset.descripcion || '';
      lightbox.classList.add('open');
      document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
      lightbox.classList.remove('open');
      document.body.style.overflow = '';
    }

    function prevImage() {
      var idx = (currentIndex - 1 + cards.length) % cards.length;
      openLightbox(idx);
    }

    function nextImage() {
      var idx = (currentIndex + 1) % cards.length;
      openLightbox(idx);
    }

    cards.forEach(function (card, i) {
      card.addEventListener('click', function () {
        openLightbox(i);
      });
    });

    lightboxClose.addEventListener('click', closeLightbox);
    lightboxPrev.addEventListener('click', prevImage);
    lightboxNext.addEventListener('click', nextImage);

    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox) closeLightbox();
    });

    document.addEventListener('keydown', function (e) {
      if (!lightbox.classList.contains('open')) return;
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowLeft') prevImage();
      if (e.key === 'ArrowRight') nextImage();
    });
  }

  /* ===== Gallery: Filter Toggle (mobile) ===== */
  var filterToggle = document.getElementById('filterToggle');
  var filtersSidebar = document.getElementById('filtersSidebar');

  if (filterToggle && filtersSidebar) {
    filterToggle.addEventListener('click', function () {
      filtersSidebar.classList.toggle('open');
    });
  }
});
