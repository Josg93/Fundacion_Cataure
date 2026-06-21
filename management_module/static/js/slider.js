document.addEventListener('DOMContentLoaded', function() {
  // Elementos del slider
  const slider = document.querySelector('.slider');
  const slides = document.querySelector('.slides');
  const slideItems = document.querySelectorAll('.slide');
  const prevBtn = document.querySelector('.slider-prev');
  const nextBtn = document.querySelector('.slider-next');
  const dots = document.querySelectorAll('.dot');
  
  // Configuración
  let currentIndex = 0;
  const slideCount = slideItems.length;
  // const slideWidth = slideItems[0].clientWidth; // This line is not needed
  const autoSlideInterval = 5000; // 5 segundos
  let autoSlideTimer;
  
  // Inicializar slider
  function initSlider() {
    // Establecer el ancho del contenedor de slides
    slides.style.width = `${slideCount * 100}%`;
    
    // Iniciar auto-desplazamiento
    startAutoSlide();
    
    // Event listeners
    prevBtn.addEventListener('click', prevSlide);
    nextBtn.addEventListener('click', nextSlide);
    
    dots.forEach(dot => {
      dot.addEventListener('click', function() {
        goToSlide(parseInt(this.getAttribute('data-index')));
      });
    });
    
    // Pausar auto-desplazamiento al interactuar
    slider.addEventListener('mouseenter', pauseAutoSlide);
    slider.addEventListener('mouseleave', startAutoSlide);
    
    // Actualizar para pantallas redimensionadas
    window.addEventListener('resize', function() {
      // updateSlidePosition(); // This might not be strictly necessary if CSS handles responsiveness well for percentages
    });
  }
  
  // Ir a slide específico
  function goToSlide(index) {
    if (index < 0) {
      index = slideCount - 1;
    } else if (index >= slideCount) {
      index = 0;
    }
    
    currentIndex = index;
    updateSlidePosition();
    updateDots();
  }
  
  // Slide anterior
  function prevSlide() {
    goToSlide(currentIndex - 1);
    resetAutoSlide();
  }
  
  // Siguiente slide
  function nextSlide() {
    goToSlide(currentIndex + 1);
    resetAutoSlide();
  }
  
  // Actualizar posición del slide
  function updateSlidePosition() {
    const offset = -currentIndex * 100;
    slides.style.transform = `translateX(${offset}%)`;
  }
  
  // Actualizar indicadores de puntos
  function updateDots() {
    dots.forEach((dot, index) => {
      if (index === currentIndex) {
        dot.classList.add('active');
      } else {
        dot.classList.remove('active');
      }
    });
  }
  
  // Auto-desplazamiento
  function startAutoSlide() {
    autoSlideTimer = setInterval(nextSlide, autoSlideInterval);
  }
  
  function pauseAutoSlide() {
    clearInterval(autoSlideTimer);
  }
  
  function resetAutoSlide() {
    pauseAutoSlide();
    startAutoSlide();
  }
  
  // Inicializar
  initSlider();
});