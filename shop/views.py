import json
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Product, Category
from django.contrib import messages

# Налаштування логування
logger = logging.getLogger(__name__)

# Відображення головної сторінки
def home(request):
    return render(request, 'shop/home.html')

# Список усіх товарів
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

# Деталі конкретного товару
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})

# Відображення кошика
def cart_detail(request):
    cart = request.session.get('cart', {})
    logger.debug("Вміст кошика: %s", cart)  # Логування вмісту кошика
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
    logger.debug("Елементи кошика: %s, Загалом: %s", cart_items, cart_total)
    return render(request, 'shop/cart.html', {'cart': cart_items, 'cart_total': cart_total})

# Додавання товару до кошика
@require_POST
def cart_add(request):
    try:
        logger.debug("Отримано запит cart_add: %s", request.body or request.POST)
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))
        else:
            product_id = request.POST.get('product_id')
            quantity = int(request.POST.get('quantity', 1))
        logger.debug("ID товару: %s, Кількість: %s", product_id, quantity)
        product = get_object_or_404(Product, id=product_id)
        if product.stock < quantity:
            logger.warning("Недостатньо товару на складі для товару %s", product_id)
            if request.content_type == 'application/json':
                return JsonResponse({'success': False, 'error': 'Недостатньо товару на складі'})
            else:
                messages.error(request, 'Недостатньо товару на складі')
                return redirect('product_list')
        cart = request.session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + quantity
        request.session['cart'] = cart
        request.session.modified = True
        logger.info("Товар %s додано до кошика", product_id)
        if request.content_type == 'application/json':
            return JsonResponse({'success': True})
        else:
            messages.success(request, 'Товар додано до кошика!')
            return redirect('cart_detail')
    except Exception as e:
        logger.error("Помилка в cart_add: %s", str(e))
        if request.content_type == 'application/json':
            return JsonResponse({'success': False, 'error': str(e)})
        else:
            messages.error(request, f'Помилка при додаванні товару: {str(e)}')
            return redirect('product_list')

# Видалення товару з кошика
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
        logger.error("Помилка в cart_remove: %s", str(e))
        return JsonResponse({'success': False, 'error': str(e)})

# Оформлення замовлення
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Ваш кошик порожній.')
        return redirect('cart_detail')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        card_number = request.POST.get('card_number')
        card_expiry = request.POST.get('card_expiry')
        card_cvv = request.POST.get('card_cvv')

        # Базова валідація
        if not all([name, email, address, phone, card_number, card_expiry, card_cvv]):
            messages.error(request, 'Будь ласка, заповніть усі поля.')
            return render(request, 'shop/checkout.html', {'cart': cart})

        try:
            # Формування даних кошика для сторінки подяки
            cart_items = []
            cart_total = 0
            for product_id, quantity in cart.items():
                product = get_object_or_404(Product, id=product_id)
                if product.stock < quantity:
                    messages.error(request, f'Недостатньо товару {product.name} на складі.')
                    return render(request, 'shop/checkout.html', {'cart': cart})
                total_price = product.price * quantity
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total_price': total_price,
                })
                cart_total += total_price
                # Оновлення складських запасів
                product.stock -= quantity
                product.save()

            # Очищення кошика
            request.session['cart'] = {}
            request.session.modified = True

            logger.info("Замовлення оброблено для користувача: %s", name)
            messages.success(request, 'Замовлення успішно оформлено!')
            return render(request, 'shop/thank_you.html', {
                'name': name,
                'email': email,
                'address': address,
                'phone': phone,
                'cart_total': cart_total,
                'cart_items': cart_items
            })
        except Exception as e:
            logger.error("Помилка при оформленні замовлення: %s", str(e))
            messages.error(request, 'Виникла помилка при оформленні замовлення.')
            return render(request, 'shop/checkout.html', {'cart': cart})

    # Відображення вмісту кошика на сторінці оформлення
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

    return render(request, 'shop/checkout.html', {
        'cart': cart_items,
        'cart_total': cart_total
    })

# Захист від прямого доступу до сторінки подяки
def thank_you(request):
    return redirect('home')