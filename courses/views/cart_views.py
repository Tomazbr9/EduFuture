from django.shortcuts import render, redirect, get_object_or_404
from courses.models import Course

def add_to_cart(request, course_id):

    course = get_object_or_404(Course, pk=course_id)

    cart = request.session.get('cart', {})
    
    first_name = course.instructor.user.first_name # type: ignore
    last_name = course.instructor.user.last_name # type: ignore
    name_instructor = f'{first_name} {last_name}'

    if not str(course.pk) in cart:
        cart[str(course.pk)] = {
            'name': str(course.name),
            'price': float(course.price),
            'instructor': name_instructor,
            'image': course.image.url
        }

    request.session['cart'] = cart
    
    return redirect('cart')

def remove_item_cart(request, item_id):

    cart = request.session.get('cart')

    # Deleta o item do carrinho
    del cart[str(item_id)]
    request.session['cart'] = cart

    return redirect('cart')

def cart_view(request):
    
    cart = request.session.get('cart', {})

    # obter numero de cursos no carrinho
    number_course_cart = len(cart)

    context = {
        'cart': cart,
        'number_course_cart': number_course_cart
    }

    return render(request, 'cart.html', context)