from django.db import models
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import os
import glob

from django.conf import settings
from django.contrib.auth.models import User


def path_and_rename(instance, filename):
    upload_to = 'avatars/'
    ext = filename.split('.')[-1]
    inst_pk = instance.pk
    file_list = glob.glob(os.path.join(settings.BASE_DIR, f'media/avatars/{inst_pk}.*')) + glob.glob(
        os.path.join(settings.BASE_DIR, f'media/avatars/{inst_pk}_*'))
    for file_path in file_list:
        try:
            os.remove(file_path)
        except OSError:
            print("Error while deleting file")
    filename = f'{inst_pk}.{ext}'

    return os.path.join(upload_to, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True, verbose_name='Про себе')

    avatar = models.ImageField(upload_to=path_and_rename, null=True, blank=True, verbose_name='Аватарка')
    avatar_thumbnail = ImageSpecField(source='avatar', processors=[ResizeToFill(70, 100)], format='JPEG',
                                      options={'quality': 60}, )

    is_invisible = models.BooleanField(default=False, verbose_name="Сором'язлива дупа")

    def __str__(self):
        return f'Profile of {str(self.user)} {self.user.pk}'

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.user.pk})

    class Meta:
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профілі'
        ordering = ['user']
