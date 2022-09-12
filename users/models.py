from django.db import models
from django.urls import reverse
import os

from django.contrib.auth.models import User


def path_and_rename_avatars(instance, filename):
    upload_to = 'avatars/'
    inst_pk = instance.pk
    ext = filename.split('.')[-1]
    filename = f'{inst_pk}.{ext}'
    return os.path.join(upload_to, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True, verbose_name='Про себе')

    avatar = models.ImageField(upload_to=path_and_rename_avatars, null=True, blank=True, verbose_name='Аватарка')
    avatar_thumbnail = models.ImageField(null=True, blank=True, verbose_name='Тамбнейл')

    is_invisible = models.BooleanField(default=False, verbose_name="Сором'язлива дупа")

    def __str__(self):
        return f'Profile of {str(self.user)} {self.user.pk}'

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.user.pk})

    class Meta:
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профілі'
        ordering = ['user']
