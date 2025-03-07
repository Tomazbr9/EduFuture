// Função para fazer a renovação de tokens 
function refreshToken() {
  const refreshToken = localStorage.getItem('refresh_token')
  return fetch('/courses/refresh_token/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ refresh_token: refreshToken })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Erro ao renovar o token.')
    }
    return response.json()
  })
  .then(data => {
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('refresh_token', data.refresh_token)
    return data.access_token
  })
  .catch(error => {
    console.error("Erro ao renovar o token:", error)
    // Redireciona para a página de login se o refresh_token também expirar
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    window.location.href = '/courses/login_user'
    throw error
  })
}

async function fetchWithTokenRefresh(url, options = {}) {
  let accessToken = localStorage.getItem('access_token')

  // Tenta fazer a requisição com o token atual
  let response = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${accessToken}`
    }
  })

  // Se o token expirou (status 401), tenta renovar o token
  if (response.status === 401) {
    try {
      const newAccessToken = await refreshToken()
      // Repete a requisição com o novo token
      response = await fetch(url, {
        ...options,
        headers: {
          ...options.headers,
          'Authorization': `Bearer ${newAccessToken}`
        }
      })
    } catch (error) {
      console.error("Erro ao renovar o token:", error)
      throw error
    }
  }

  return response
}

let currentSlide = 0
function moveCarousel(carousel_id, direction) {
  const carouselWrapper = document.querySelector(`.carousel-wrapper-${carousel_id}`);
  const totalSlides = document.querySelectorAll(`.carousel-wrapper-${carousel_id} .carousel-slide`).length;
  
  // Atualiza o índice do slide
  currentSlide += direction

  // Verifica os limites
  if (currentSlide < 0) {
    currentSlide = totalSlides - 1;
  } else if (currentSlide >= totalSlides) {
    currentSlide = 0
  }

  // Move o carrossel
  const slideWidth = carouselWrapper.offsetWidth
  carouselWrapper.style.transform = `translateX(-${currentSlide * slideWidth}px)`
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

    if (data.access_token){
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
    }
  })
  .catch(error => {
    console.error("Erro:", error)
    messageError.textContent = "Erro ao tentar fazer login. Tente novamente."
  })
}

const categoryInput = document.getElementById('floatingCategory')
const listCategories = document.getElementById('listCategories')
if(categoryInput && listCategories){
  categoryInput.addEventListener('click', ()=>{
      listCategories.style.display = 'block'
  })
}

function assignCategory(element, IdCategory){
    let categoryInput = document.getElementById('floatingCategory')
    const hiddenCategory = document.getElementById('hiddenCategory') 
    categoryInput.value = element.textContent
    listCategories.style.display = 'none'
    hiddenCategory.value = IdCategory
}


document.addEventListener("DOMContentLoaded", () => {
  const floatingDate = document.getElementById("floatingDate")
  const hiddenDate = document.getElementById("hiddenDate")

  if (floatingDate && hiddenDate) { // Verifica se os elementos existem
      floatingDate.addEventListener("input", function (e) {
          let value = e.target.value.replace(/\D/g, "") // Remove tudo que não for número
          let formattedValue = ""

          if (value.length > 2) {
              formattedValue += value.substring(0, 2) + "/"
          } else {
              formattedValue += value
          }
          if (value.length > 4) {
              formattedValue += value.substring(2, 4) + "/"
          } else if (value.length > 2) {
              formattedValue += value.substring(2)
          }
          if (value.length > 8) {
              formattedValue += value.substring(4, 8)
          } else if (value.length > 4) {
              formattedValue += value.substring(4)
          }

          e.target.value = formattedValue

          if (value.length === 8) {
              let day = value.substring(0, 2)
              let month = value.substring(2, 4)
              let year = value.substring(4)

              hiddenDate.value = `${year}-${month}-${day}`
          } else {
              hiddenDate.value = ""
          }
      })
  }
})

const imageUser = document.getElementById('imageUser')
if(imageUser){
  imageUser.addEventListener('change', (event) => {
    const file = event.target.files[0]
    if (file) {
        const reader = new FileReader()
        reader.onload = function (e) {
            const img = document.getElementById('imageUserPreview')
            img.src = e.target.result
        }
        reader.readAsDataURL(file) 
    }
  })
}

function buyCourses() {
  let courses = []

  document.querySelectorAll('.content-course-cart').forEach(item => {
    let courseId = item.getAttribute('course-id');
    if (courseId) {
      courses.push(parseInt(courseId))
    }
  })

  if (courses.length === 0) {
    alert("Seu carrinho está vazio!")
    return
  }
  
  fetchWithTokenRefresh('/courses/buy/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ courses: courses })
  })
  .then(response => response.json())
  .then(data => {
    window.location.reload()
  })
  .catch(error => {
    console.error("Erro ao comprar cursos:", error)
    alert("Ocorreu um erro ao processar sua compra. Por favor, tente novamente.");
  })
}

function displayClassVideo(video, element){
  let sourceElement = document.getElementById('urlVideo')
  let videoElement = document.getElementById('videoLesson')
  let classId = element.getAttribute('classId')
  let courseId = element.getAttribute('courseId')

  try {
    let classeActivated = JSON.parse(localStorage.getItem(courseId) ?? '{}') || {} 
    classeActivated[courseId] = {[classId]: video} 
    localStorage.setItem(courseId, JSON.stringify(classeActivated))
  } 
  catch (error) {
    console.error("Erro ao acessar localStorage:", error)
    localStorage.setItem(courseId, JSON.stringify({})) 
  }

  sourceElement.src = video
  videoElement.load()
  videoElement.play()

  localStorage.setItem(`lastVideo-${classId}`, video)

  document.querySelectorAll('.class-item').forEach(item => {
    item.classList.remove('active-class')
  })

  element.classList.add('active-class')
  
}

// Evento para exibição do ultima aula assistida
window.addEventListener('DOMContentLoaded', () => {
  let sourceElement = document.getElementById('urlVideo')
  let videoElement = document.getElementById('videoLesson')
  
  document.querySelectorAll('.class-item').forEach(item => {
      let courseId = item.getAttribute('courseId')
      let classId = item.getAttribute('classId')
      
      let classeActivated = JSON.parse(localStorage.getItem(courseId))
      
      for(let [course, lesson] of Object.entries(classeActivated)){
        for(let info in lesson){
          if(info === classId){
            item.classList.add('active-class')

            sourceElement.src = lesson[info]
            videoElement.load()
          }
        }
      }
   })
})

function finishClass(element, classId){
  fetchWithTokenRefresh(`/courses/students_classes/${classId}/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ "completed": element.checked }) 
  })
}

function saveId(element, id){
    id.value = element.value
}

// Função para fazer requisição para a criação de cursos
const formCreateCourse = document.getElementById('formCreateCourse')
if(formCreateCourse){
  formCreateCourse.addEventListener('submit', (event) => {
    event.preventDefault()

      let name = document.getElementById('nameCourseCreate').value
      let description = document.getElementById('descriptionCourseCreate').value
      let price = document.getElementById('priceCourseCreate').value
      let image = document.getElementById('imageCourseCreate').files[0]
      let category = document.getElementById('categoryId').value

      const formData = new FormData()
      formData.append('name', name)
      formData.append('description', description)
      formData.append('price', price)
      formData.append('image', image)
      formData.append('category', category)

      fetchWithTokenRefresh('/courses/courses/', {
        method: 'POST',
        body: formData 
      }).catch(error => console.error("Error:", error))
  })
}
  
// Função para fazer requisição para a criação de modulos
const formCreateModule = document.getElementById('formCreateModule')
if(formCreateModule){
  formCreateModule.addEventListener('submit', (event)=>{
    event.preventDefault()

    let nameModule = document.getElementById('nameModuleCreate').value
    let idCourse = document.getElementById('courseIdModuleCreate').value

    const formData = new FormData()
    formData.append('title', nameModule)
    formData.append('course', idCourse)

    fetchWithTokenRefresh('/courses/modules/', {
        method: 'POST',
        body: formData
    }).then(response => {
      if(response.ok){
        location.reload()
      }
    })
    .catch(error => console.error("Error:", error))
  })
}

// Função para fazer requisição para a criação de aulas
const formLessonCreate = document.getElementById('formLessonCreate')
if(formLessonCreate){
    formLessonCreate.addEventListener('submit', (event)=>{
      event.preventDefault()

      let nameLesson = document.getElementById('nameLessonCreate').value
      let materials = document.getElementById('materialsLessonCreate').files[0]
      let video = document.getElementById('videoLessonCreate').files[0]
      let _module = document.getElementById('lessonIdModuleCreate').value

      const formData = new FormData()
      formData.append('title', nameLesson)
      formData.append('materials', materials)
      formData.append('video', video)
      formData.append('module', _module)

      fetchWithTokenRefresh('/courses/classes/', {
        method: 'POST',
        body: formData
      }).then(response => {
        if(response.ok){
          location.reload()
        }
      }).catch(error => console.error('Error:', error))
      })
}

// Função para fazer uma requisição de registro de novo úsuario
const formRegister = document.getElementById('formRegister')
if(formRegister){
  formRegister.addEventListener('submit', (event)=>{
    event.preventDefault()

    let messageErrorRegister = document.getElementById('messageErrorRegister')

    let userName = document.getElementById('floatingUserName').value
    let email = document.getElementById('floatingEmail').value
    let firstName = document.getElementById('floatingName').value
    let lastName = document.getElementById('floatingLastName').value
    let date = document.getElementById('hiddenDate').value
    let password = document.getElementById('floatingPassword').value
    let category = document.getElementById('hiddenCategory').value
    let isInstructor = document.getElementById('flexCheckDefault').checked

    const formData = new FormData()
    formData.append('username', userName)
    formData.append('email', email)
    formData.append('first_name', firstName)
    formData.append('last_name', lastName)
    formData.append('age', date)
    formData.append('password', password)
    formData.append('category', category)
    formData.append('username', userName)
    formData.append('is_instructor', isInstructor)

    fetch('/courses/register/', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json().then(data => ({ status: response.status, body: data })))
    .then(result => {
        if (result.status === 400) {
            for(field in result.body){
              messageErrorRegister.innerHTML += `${result.body[field]}<br>`
            }
        } 
        else {
            window.location.href = '/courses/login_user/'
        }
    })
    .catch(error => console.error('Erro na requisição:', error))
  })
}