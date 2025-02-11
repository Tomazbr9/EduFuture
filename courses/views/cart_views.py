from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
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

    # Obtém ou cria o Student vinculado ao usuário logado
    student, created = Student.objects.get_or_create(user=request.user)

    # Obtém ou cria o carrinho do estudante
    cart_obj, created = Cart.objects.get_or_create(user=student)

    # Se items for um JSONField, apenas salvar os itens no banco
    if hasattr(cart_obj, 'items'):
        cart_obj.items = cart  # Armazena o carrinho no banco
        cart_obj.save()

    return redirect('cart')


def remove_item_cart(request, item_id):
    # Obtém o carrinho da sessão
    cart = request.session.get('cart', {})

    # Remove o item do carrinho da sessão, se ele existir
    if str(item_id) in cart:
        del cart[str(item_id)]
        request.session['cart'] = cart  # Atualiza a sessão

    # Obtém ou cria o estudante vinculado ao usuário
    student, _ = Student.objects.get_or_create(user=request.user)

    # Obtém ou cria o carrinho do estudante
    cart_obj, _ = Cart.objects.get_or_create(user=student)

    # Se `cart_obj.items` for um JSONField, remove a chave de forma segura
    if isinstance(cart_obj.items, dict) and str(item_id) in cart_obj.items:
        cart_obj.items.pop(str(item_id))  # Remove o item do JSONField
        cart_obj.save()  # Salva a alteração no banco de dados

    # Atualiza o carrinho na sessão
    request.session['cart'] = cart_obj.items if isinstance(cart_obj.items, dict) else {}

    return redirect('cart')

@login_required(login_url='login-user')
def cart_view(request):
    
    student = get_object_or_404(Student, user=request.user)
    cart, _ = Cart.objects.get_or_create(user=student)

    items = cart.items if cart.items else {}

    # obter numero de cursos no carrinho
    number_course_cart = len(items)

    context = {
        'items': items,
        'number_course_cart': number_course_cart
    }

    return render(request, 'cart.html', context)