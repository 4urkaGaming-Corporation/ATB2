// Логування для відлагодження, щоб перевірити завантаження скрипта
console.log('cart.js завантажено');

// Функція для додавання товару до кошика
function addToCart(productId) {
    console.log('addToCart викликано з productId:', productId);
    fetch('/cart/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ product_id: parseInt(productId) }), // Перетворюємо productId у число
    })
    .then(response => {
        console.log('Статус відповіді:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Дані відповіді:', data);
        if (data.success) {
            alert('Товар додано до кошика!');
            location.reload();
        } else {
            alert('Помилка при додаванні товару: ' + (data.error || 'Невідома помилка'));
        }
    })
    .catch(error => {
        console.error('Помилка:', error);
        alert('Виникла помилка при додаванні товару.');
    });
}

// Функція для видалення товару з кошика
function removeFromCart(productId) {
    console.log('removeFromCart викликано з productId:', productId);
    fetch('/cart/remove/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ product_id: parseInt(productId) }), // Перетворюємо productId у число
    })
    .then(response => {
        console.log('Статус відповіді:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Дані відповіді:', data);
        if (data.success) {
            location.reload();
        } else {
            alert('Помилка при видаленні товару: ' + (data.error || 'Невідома помилка'));
        }
    })
    .catch(error => {
        console.error('Помилка:', error);
        alert('Виникла помилка при видаленні товару.');
    });
}

// Функція для отримання CSRF-токена з кукі
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    console.log('CSRF Token:', cookieValue); // Логування для відлагодження
    return cookieValue;
}

// Клієнтська валідація форми оформлення замовлення
document.addEventListener('DOMContentLoaded', function() {
    const checkoutForm = document.querySelector('form');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', function(e) {
            const cardNumber = document.getElementById('card_number');
            const cardExpiry = document.getElementById('card_expiry');
            const cardCvv = document.getElementById('card_cvv');
            const phone = document.getElementById('phone');

            if (cardNumber && cardNumber.value.length !== 16) {
                e.preventDefault();
                alert('Номер картки має містити 16 цифр');
                return;
            }

            if (cardExpiry && !/^(0[1-9]|1[0-2])\/\d{2}$/.test(cardExpiry.value)) {
                e.preventDefault();
                alert('Невірний формат терміну дії (ММ/РР)');
                return;
            }

            if (cardCvv && !/^\d{3,4}$/.test(cardCvv.value)) {
                e.preventDefault();
                alert('CVV має містити 3 або 4 цифри');
                return;
            }

            if (phone && !/^\+?\d{10,}$/.test(phone.value)) {
                e.preventDefault();
                alert('Невірний формат номера телефону');
                return;
            }
        });
    }
});