from django.db import models
from django.urls import reverse


class User(models.Model):
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100, verbose_name='Пароль')
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Ім'я")
    bio = models.TextField(null=True, blank=True, verbose_name='Про себе')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватар')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('user', kwargs={'user_name': self.name})

    class Meta:
        verbose_name = 'Користувачі'
        verbose_name_plural = 'Користувачі'
        ordering = ['id']
