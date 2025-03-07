from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from utils.other_functions import slice_courses
from courses.models import Course, Student, StudentCourse, StudentClass, Category
from utils.instructor import InstructorUtil

def home(request):

    query = request.GET.get('q')

    if not query:

        # Todos os Cursos da plataforma
        courses = Course.objects.all()
        all_courses_slice = slice_courses(courses)
        
        # Cursos de Tecnologia
        technology_courses = Course.objects.filter(category=1)
        technology_courses_slice = slice_courses(technology_courses)

        # Cursos de Saúde
        health_courses = Course.objects.filter(category=2)
        health_courses_slice = slice_courses(health_courses)

        # Cursos de Finanças
        finance_courses = Course.objects.filter(category=3)
        finance_courses_slice = slice_courses(finance_courses)

        context = {
            'all_courses': all_courses_slice,
            'technology_courses': technology_courses_slice,
            'health_courses': health_courses_slice,
            'finance_courses': finance_courses_slice,
            # 'courses_interest': courses_interest_slice
        }

        return render(request, 'home.html', context)
    
    result_courses = Course.objects.filter(
            Q(name__icontains=query)  # Filtra pelo nome
        )
    
    return render(request, 'home.html', {'result_courses': result_courses})

    


def course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    try: 
        user = Student.objects.get(user=request.user)
        course_purchased = StudentCourse.objects.filter(
        course=course, student=user).exists()
    except Exception:
        course_purchased = False

    if course_purchased:
        
        # Obtem os modulos e aulas do curso
        modules = course.modules.prefetch_related('classes') # type: ignore
        modules_dict = {}

        # obtem o certificado do aluno
        certificate = StudentCourse.objects.get(
            course=course, student=user
        ).certificate

        student_classes = StudentClass.objects.filter(
            student=user, cls__module__course=course
        ).select_related('cls')

        lessons_dict = {
            sc.cls.pk: {'id': sc.pk, 'completed': sc.completed}
            for sc in student_classes
        }
        
        for module in modules:
            module_classes = []
            for cls in module.classes.values('id', 'title', 'video'):
                classes_info = lessons_dict.get(
                    cls['id'], {'id': None, 'completed': None}
                )
            
                module_classes.append({
                    **cls,
                    'id_student_classes': classes_info['id'],
                    'completed': classes_info['completed']
                })
            
            modules_dict[module.title] = module_classes
        
        context = {
            'certificate': certificate,
            'course': course,
            'course_purchased': course_purchased,
            'modules_dict': modules_dict,
        }
        

        return render(request, 'course_purchased.html', context)
    else:

        # Lista de Objetivos de aprendizado
        learning_list = course.objective.split('\n')

        # Quantidade de alunos matriculados
        number_of_students = StudentCourse.objects.filter(course=course).count()

        context = {
            'course_purchased': course_purchased,
            'course': course,
            'learning_list': learning_list,
            'number_of_students': number_of_students,
        }

        return render(request, 'course.html', context)

def courses_from_user(request):
    
    # obter cursos comprados pelo usuario
    user = Student.objects.get(user=request.user)
    courses_from_user = StudentCourse.objects.filter(student=user)

    context = {
        'courses_from_user': courses_from_user
    }

    return render(request, 'courses_from_user.html', context)

def course_create(request):
    
    # obtendo todos os cursos criados pelo instructor
    instructor_courses = InstructorUtil(request).take_courses()

    # obtendo todos os modulos criado pelo instrutor
    instructor_modules = InstructorUtil(request).take_modules()

    # obtem todas categorias disponiveis
    categorys = Category.objects.all()


    context = {
        'courses': instructor_courses,
        'modules': instructor_modules,
        'categorys': categorys
    }

    return render(request, 'course_creation_area', context)


def search(request):
    search_value = request.GET.get('q', '').strip()

    if search_value == '':
        return redirect('home')
    
    courses = Course.objects.filter(
        show=True
    ).filter(
        Q(name__icontains=search_value)
    ).order_by('-id')

    context = {
        'courses': courses,
        'search_value' : search_value
    }

    return render(request, 'home.html', context)