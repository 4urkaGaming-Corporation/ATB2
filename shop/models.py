from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL-имя')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL-имя')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    description = models.TextField(blank=True, verbose_name='Описание')
    stock = models.PositiveIntegerField(default=0, verbose_name='На складе')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='Изображение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'