# from django.db import models
# from django.urls import reverse
# import os
#
# from django.contrib.auth.models import User
#
# from djangogramm.settings import MEDIA_ROOT
#
#
# def path_and_rename(instance, filename):
#     if 'Profile' in str(instance):
#         upload_to = 'avatars/'
#         inst_pk = instance.pk
#     else:
#         upload_to = 'images/'
#         inst_pk = instance.post_id
#     ext = filename.split('.')[-1]
#     filename = f'{upload_to[:-1]}_{inst_pk}.{ext}'
#     if upload_to == 'avatars/' and os.path.exists(os.path.join(MEDIA_ROOT, upload_to, filename)):
#         os.remove(os.path.join(MEDIA_ROOT, upload_to, filename))
#     return os.path.join(upload_to, filename)
#
#
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(null=True, blank=True, verbose_name='Про себе')
#
#     avatar = models.ImageField(upload_to=path_and_rename, null=True, blank=True, verbose_name='Аватарка')
#     avatar_thumbnail = models.ImageField(null=True, blank=True, verbose_name='Тамбнейл')
#
#     is_invisible = models.BooleanField(default=False, verbose_name="Сором'язлива дупа")
#
#     def __str__(self):
#         return f'Profile of {str(self.user)} {self.user.pk}'
#
#     def get_absolute_url(self):
#         return reverse('user_detail', kwargs={'pk': self.user.pk})
#
#     class Meta:
#         verbose_name = 'Профіль'
#         verbose_name_plural = 'Профілі'
#         ordering = ['user']
