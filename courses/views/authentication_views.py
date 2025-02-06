from django.shortcuts import render
from courses.models import Category

def login_view(request):

    return render(request, 'login.html')


def register_view(request):
    
    all_categories = Category.objects.all()

    context = {
        'all_categories': all_categories
    }

    return render(request, 'register.html', context)