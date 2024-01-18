from django.db import models
from django.utils.text import slugify
from datetime import date


class BlogPost(models.Model):

    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.SlugField(max_length=150, unique=True, verbose_name='Slug')
    content = models.TextField(verbose_name='Содержимое')
    preview_image = models.ImageField(
        upload_to='blog/',
        default='blog/default_image.jpeg',
        max_length=150,
        verbose_name='Превью',
        blank=True,
        null=True
    )
    creation_date = models.DateField(
        verbose_name='Дата создания', default=date.today)
    is_published = models.BooleanField(
        default=False, verbose_name='Признак публикации')
    views_count = models.PositiveIntegerField(
        default=0, verbose_name='Количество просмотров')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} ({self.creation_date:%Y-%m-%d})'
