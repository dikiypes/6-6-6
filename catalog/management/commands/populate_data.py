from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from django.db import connection


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        Category.objects.all().delete()

        Category.objects.create(category_name='Новая категория 1')
        Category.objects.create(category_name='Новая категория 2')

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO catalog_category (category_name, category_description) VALUES ('Новая категория 3', 'Описание 3')")
            cursor.execute(
                "INSERT INTO catalog_category (category_name, category_description) VALUES ('Новая категория 4', 'Описание 4')")
