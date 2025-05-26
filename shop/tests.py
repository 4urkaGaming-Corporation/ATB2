from django.test import TestCase
from .models import Product
from django.urls import reverse

class ProductModelTests(TestCase):
    def setUp(self):
        Product.objects.create(name="Test Product", price=10.00, stock=100)

    def test_product_creation(self):
        product = Product.objects.get(name="Test Product")
        self.assertEqual(product.price, 10.00)
        self.assertEqual(product.stock, 100)

class ProductViewTests(TestCase):
    def test_product_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Products")