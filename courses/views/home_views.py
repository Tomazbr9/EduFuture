from django.shortcuts import render, get_object_or_404, redirect
from utils.other_functions import slice_courses
from courses.models import Course, Student, StudentCourse
from decimal import Decimal


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

    # desired_category = Student.objects.get(user=request.user).category
    # courses_interest = Course.objects.filter(category=3)
    # courses_interest_slice = slice_courses(courses_interest)

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
    
    # Lista de Objetivos de aprendizado
    learning_list = course.objective.split('\n')

    # Quantidade de alunos matriculados
    number_of_students = StudentCourse.objects.filter(course=course).count()

    context = {
        'course': course,
        'learning_list': learning_list,
        'number_of_students': number_of_students
    }

    return render(request, 'course.html', context)
