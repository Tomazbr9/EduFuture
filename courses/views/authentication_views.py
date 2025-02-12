from django.shortcuts import render, redirect, get_object_or_404
from courses.models import Category, Cart, Student
from django.contrib.auth import login, authenticate, logout

def login_view(request):
    
    return render(request, 'login.html')

def logout_view(request):

    cart = request.session.get('cart', {})

    user = get_object_or_404(Student, user=request.user)
    cart_obj, _ = Cart.objects.get_or_create(user=user)
    cart_obj.items = cart
    cart_obj.save()

    logout(request)
    return redirect('home')

def register_view(request):
    
    all_categories = Category.objects.all()

    context = {
        'all_categories': all_categories
    }

    return render(request, 'register.html', context)