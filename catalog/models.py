from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    category_name = models.CharField(
        max_length=100, verbose_name='Наименование')
    category_description = models.CharField(
        max_length=250, verbose_name='Описание')

    def __str__(self):
        return f'{self.category_name}'


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products', default=0)

    product_name = models.CharField(
        max_length=150, verbose_name='Наименование')
    product_description = models.CharField(
        max_length=250, verbose_name='Описание')
    product_image = models.ImageField(upload_to='catalog/', default='catalog/default_image.jpeg',
                                      max_length=150, verbose_name='Изображение(превью)', **NULLABLE)
    product_category_name = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Категория')
    product_sale_price = models.FloatField(verbose_name='Цена за штуку')
    create_date = models.DateField(
        verbose_name='Дата создания', default=timezone.now)
    update_date = models.DateField(
        verbose_name='Дата последнего изменения', default=timezone.now)
    is_published = models.BooleanField(
        default=False, verbose_name='Опубликован')

    def __str__(self):
        return f'{self.id} {self.product_name} {self.product_sale_price} {self.product_category_name}'


class Version(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Продукт')
    version_number = models.CharField(
        max_length=50, verbose_name='Номер версии')
    version_name = models.CharField(
        max_length=100, verbose_name='Название версии')
    is_current = models.BooleanField(
        default=False, verbose_name='Текущая версия')

    def __str__(self):
        return f'{self.product} - {self.version_number} ({self.version_name})'
