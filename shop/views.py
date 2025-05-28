import json
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Product, Category
from django.contrib import messages

# Настройка логирования
logger = logging.getLogger(__name__)

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
        logger.debug("Received cart_add request: %s", request.body or request.POST)
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))
        else:
            product_id = request.POST.get('product_id')
            quantity = int(request.POST.get('quantity', 1))
        logger.debug("Product ID: %s, Quantity: %s", product_id, quantity)
        product = get_object_or_404(Product, id=product_id)
        if product.stock < quantity:
            logger.warning("Insufficient stock for product %s", product_id)
            if request.content_type == 'application/json':
                return JsonResponse({'success': False, 'error': 'Недостаточно товара на складе'})
            else:
                messages.error(request, 'Недостаточно товара на складе')
                return redirect('product_list')
        cart = request.session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + quantity
        request.session['cart'] = cart
        request.session.modified = True
        logger.info("Product %s added to cart", product_id)
        if request.content_type == 'application/json':
            return JsonResponse({'success': True})
        else:
            messages.success(request, 'Товар добавлен в корзину!')
            return redirect('cart_detail')
    except Exception as e:
        logger.error("Error in cart_add: %s", str(e))
        if request.content_type == 'application/json':
            return JsonResponse({'success': False, 'error': str(e)})
        else:
            messages.error(request, f'Ошибка при добавлении товара: {str(e)}')
            return redirect('product_list')

@require_POST
def cart_remove(request):
    try:
        data = request.POST if request.POST else request.body
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
        messages.success(request, 'Заказ успешно оформлен!')
        request.session['cart'] = {}
        return redirect('home')
    return render(request, 'shop/checkout.html')