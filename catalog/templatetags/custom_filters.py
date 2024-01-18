from django import template
from django.templatetags.static import PrefixNode
from django.conf import settings

register = template.Library()


@register.simple_tag
def mediapath(file_path):
    if file_path and not str(file_path).startswith(('http://', 'https://', '/')):
        return f"{settings.MEDIA_URL}{file_path}"
    return file_path
