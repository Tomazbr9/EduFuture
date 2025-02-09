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


function showModal(event, idCourse){
    event.preventDefault()
    
    fetch(`/courses/add_to_cart/${idCourse}/`, {
      method: 'GET'
    }).then(()=>{
      let modal = new bootstrap.Modal(document.getElementById('modalBuy'))
      modal.show()
    })
    .catch(error => console.error('Erro na requisição: ', error))
}

function loginUser(event) {
  event.preventDefault();

  const username = document.getElementById('floatingInputLogin').value
  const password = document.getElementById('floatingPasswordLogin').value
  const messageError = document.getElementById('messageError')

  fetch(`/courses/login/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password })
  })
  .then(response => {
    if(response.ok){
      window.location.href = '/courses/home/'
    }

    return response.json()
  })
  .then(data => {
    messageError.textContent = data.message
  })
  .catch(error => {
    console.error("Erro:", error)
    messageError.textContent = "Erro ao tentar fazer login. Tente novamente."
  })
}

const categoryInput = document.getElementById('floatingCategory')
const listCategories = document.getElementById('listCategories')
categoryInput.addEventListener('click', ()=>{
    listCategories.style.display = 'block'
})

function assignCategory(element, IdCategory){
    let categoryInput = document.getElementById('floatingCategory')
    const hiddenCategory = document.getElementById('hiddenCategory') 
    categoryInput.value = element.textContent
    listCategories.style.display = 'none'
    hiddenCategory.value = IdCategory
}


document.getElementById("floatingDate").addEventListener("input", function (e) {
    let value = e.target.value.replace(/\D/g, "") // Remove tudo que não for número
    let formattedValue = ""

    if (value.length > 2) {
        formattedValue += value.substring(0, 2) + "/";
    } else {
        formattedValue += value
    }
    if (value.length > 4) {
        formattedValue += value.substring(2, 4) + "/"
    } else if (value.length > 2) {
        formattedValue += value.substring(2);
    }
    if (value.length > 8) {
        formattedValue += value.substring(4, 8)
    } else if (value.length > 4) {
        formattedValue += value.substring(4)
    }

    e.target.value = formattedValue

    if(value.length === 8){
      let day = value.substring(0, 2)
      let month = value.substring(2, 4)
      let year = value.substring(4)
    
      document.getElementById('hiddenDate').value = `${year}-${month}-${day}`

    } else {
      document.getElementById('hiddenDate').value = ''
    }
})
