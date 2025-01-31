let currentSlide = 0;

function moveCarousel(carousel_id, direction) {
  const carouselWrapper = document.querySelector(`.carousel-wrapper-${carousel_id}`);
  const totalSlides = document.querySelectorAll(`.carousel-wrapper-${carousel_id} .carousel-slide`).length;
  
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


function displayClasses(idModule){
    const classes = document.getElementById(`classes-${idModule}`)
    const arrow = document.getElementById(`arrow-${idModule}`)
    classes.style.display = classes.style.display === 'block' ? 'none' : 'block'
    
    if (arrow.classList.contains('bi-chevron-down')){
      arrow.classList.replace('bi-chevron-down', 'bi-chevron-up')
    } else {
      arrow.classList.replace('bi-chevron-up', 'bi-chevron-down') 
    }
}


function showModal(){
  const modal = new bootstrap.Modal(document.getElementById('modalBuy'))
  modal.show()
}


function freeze(){
  
}