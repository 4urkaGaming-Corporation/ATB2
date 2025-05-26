# shop/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, Category
from django.views.decorators.http import require_POST
from django.contrib import messages

def home(request):
    return render(request, 'shop/home.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    cart_total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_price = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price,
        })
        cart_total += total_price
    return render(request, 'shop/cart.html', {'cart': cart_items, 'cart_total': cart_total})

@require_POST
def cart_add(request):
    try:
        data = request.POST if request.POST else request.body
        import json
        data = json.loads(data) if isinstance(data, bytes) else data
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        if product.stock < quantity:
            return JsonResponse({'success': False, 'error': 'Недостаточно товара на складе'})
        cart = request.session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + quantity
        request.session['cart'] = cart
        request.session.modified = True
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_POST
def cart_remove(request):
    try:
        data = request.POST if request.POST else request.body
        import json
        data = json.loads(data) if isinstance(data, bytes) else data
        product_id = data.get('product_id')
        cart = request.session.get('cart', {})
        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart
            request.session.modified = True
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_detail')
    if request.method == 'POST':
        # Заглушка для обработки заказа
        messages.success(request, 'Заказ успешно оформлен!')
        request.session['cart'] = {}
        return redirect('home')
    return render(request, 'shop/checkout.html')