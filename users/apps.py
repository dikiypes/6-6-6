from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from catalog.models import Product
        moderator_group, created = Group.objects.get_or_create(
            name='Модераторы')
        content_type = ContentType.objects.get_for_model(Product)
        change_is_published_permission, created = Permission.objects.get_or_create(
            codename='can_change_is_published',
            name='Может менять статус публикации',
            content_type=content_type
        )
        change_description_permission, created = Permission.objects.get_or_create(
            codename='can_change_description',
            name='Может менять описание',
            content_type=content_type
        )
        change_category_permission, created = Permission.objects.get_or_create(
            codename='can_change_category',
            name='Может менять категорию',
            content_type=content_type
        )
        moderator_group.permissions.add(
            change_is_published_permission, change_description_permission, change_category_permission)
        moderator_group.save()
