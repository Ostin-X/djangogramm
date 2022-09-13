from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
    verbose_name = 'Пост'
    verbose_name_plural = 'Пости'

    def ready(self):
        from . import signals
