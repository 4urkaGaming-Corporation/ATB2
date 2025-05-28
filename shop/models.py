from django.db import models

# Модель категорії товарів
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Назва')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL-ім’я')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

# Модель товару
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL-ім’я')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='Категорія')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')
    description = models.TextField(blank=True, verbose_name='Опис')
    stock = models.PositiveIntegerField(default=0, verbose_name='На складі')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='Зображення')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'