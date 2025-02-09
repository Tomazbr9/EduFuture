from django.shortcuts import render, redirect
from courses.models import Category
from django.contrib.auth import login, authenticate, logout

def login_view(request):
    
    return render(request, 'login.html')

def logout_view(request):

    logout(request)
    return redirect('home')

def register_view(request):
    
    all_categories = Category.objects.all()

    context = {
        'all_categories': all_categories
    }

    return render(request, 'register.html', context)