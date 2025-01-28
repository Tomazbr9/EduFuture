let currentSlide = 0;

function moveCarousel(carousel_id, direction) {
  const carouselWrapper = document.querySelector(`.carousel-wrapper-${carousel_id}`);
  const totalSlides = document.querySelectorAll(`.carousel-wrapper-${carousel_id} .carousel-slide`).length;
  
  console.log(totalSlides)
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
