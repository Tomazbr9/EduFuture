from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from courses.models import Course, Cart, Student

def add_to_cart(request, course_id):
    # Obtém o curso pelo ID
    course = get_object_or_404(Course, pk=course_id)

    # Obtém o carrinho da sessão (ou cria um novo dicionário vazio)
    cart = request.session.get('cart', {})

    # Obtém o nome do instrutor
    first_name = course.instructor.user.first_name  # type: ignore
    last_name = course.instructor.user.last_name  # type: ignore
    name_instructor = f'{first_name} {last_name}'

    # Adiciona o curso ao carrinho na sessão, se ainda não estiver presente
    if str(course.pk) not in cart:
        cart[str(course.pk)] = {
            'name': course.name,
            'price': float(course.price),
            'instructor': name_instructor,
            'image': course.image.url if course.image else ''
        }

    # Atualiza o carrinho na sessão
    request.session['cart'] = cart

    return redirect('cart')


def remove_item_cart(request, item_id):
    # Obtém o carrinho da sessão
    cart = request.session.get('cart', {})

    # Remove o item do carrinho da sessão, se ele existir
    if str(item_id) in cart:
        del cart[str(item_id)]
        request.session['cart'] = cart  # Atualiza a sessão
    
    return redirect('cart')

@login_required(login_url='login-user')
def cart_view(request):
    
    cart = request.session.get('cart', {})

    # obter total do carrinho
    total = 0
    for value in cart.values():
        total += value['price']

    # obter numero de cursos no carrinho
    number_course_cart = len(cart)

    context = {
        'cart': cart,
        'total': total,
        'number_course_cart': number_course_cart
    }

    return render(request, 'cart.html', context)