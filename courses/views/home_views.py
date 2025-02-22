from django.shortcuts import render, get_object_or_404, redirect
from utils.other_functions import slice_courses
from courses.models import Course, Student, StudentCourse, StudentClass, Class
from collections import defaultdict

def home(request):

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


def course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course_purchased = False
    try:
        user = Student.objects.get(user=request.user)
    except Exception:
        ...

    # Verificar se o usuario comprou o curso
    course_purchased = StudentCourse.objects.filter(
    course=course, student=user).exists()
    
    # Lista de Objetivos de aprendizado
    learning_list = course.objective.split('\n')

    # Quantidade de alunos matriculados
    number_of_students = StudentCourse.objects.filter(course=course).count()

    
    # Obtem os modulos e aulas do curso
    modules = course.modules.prefetch_related('classes') # type: ignore
    modules_dict = {}
    lessons_dict = {}

    student_classes = StudentClass.objects.filter(
        student=user, cls__module__course=course
    )

    for i in student_classes:
        lessons_dict[i.cls.pk] =  {'id': i.pk, 'completed': i.completed}
    for module in modules:
        for i in module.classes.all():
            for id, student_class in lessons_dict.items():
                if id == i.pk:
                    modules_dict[module.title] = [
                        {
                            **cls, 'id_student_class': student_class['id'], 
                            'completed': student_class['completed']
                        } 
                        for cls in module.classes.values('id', 'title', 'video')
                    ]

    print(modules_dict)

    context = {
        'course_purchased': course_purchased,
        'course': course,
        'learning_list': learning_list,
        'number_of_students': number_of_students,
        'modules_dict': modules_dict
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
