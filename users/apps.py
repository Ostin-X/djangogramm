from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Профільq'
    verbose_name_plural = 'Профілі'

    def ready(self):
        from . import signals