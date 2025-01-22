let currentSlide = 0;

function moveCarousel(direction) {
  const carouselWrapper = document.querySelector('.carousel-wrapper');
  const totalSlides = document.querySelectorAll('.carousel-slide').length;

  // Atualiza o índice do slide
  currentSlide += direction;

  // Verifica os limites
  if (currentSlide < 0) {
    currentSlide = totalSlides - 1;
  } else if (currentSlide >= totalSlides) {
    currentSlide = 0;
  }

  // Move o carrossel
  const slideWidth = carouselWrapper.offsetWidth;
  carouselWrapper.style.transform = `translateX(-${currentSlide * slideWidth}px)`;
}
