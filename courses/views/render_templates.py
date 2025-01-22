from django.shortcuts import render
from courses.models import Course


def home(request):
    courses = Course.objects.all()

    chunk_size = 5
    grouped_courses = [courses[i:i + chunk_size] for i in range(0, len(courses), chunk_size)]

    context = {
        'grouped_courses': grouped_courses
    }

    for i in grouped_courses:
        print(i)
        for group in i:
            print(group)

    return render(request, 'home.html', context)