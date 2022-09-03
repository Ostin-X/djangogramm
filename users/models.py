# from django.db import models
# from django.urls import reverse
# from django.template.defaultfilters import slugify
# from django.contrib.auth.models import User
# import random
#
#
# from .utils import path_and_rename
#
#
# class Profile(models.Model):
#     user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
#
#     # name = models.CharField(max_length=100, verbose_name="Ім'я")
#     # slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')
#     # email = models.EmailField(max_length=100)
#     # password = models.CharField(max_length=100, verbose_name='Пароль')
#     bio = models.TextField(null=True, blank=True, verbose_name='Про себе')
#     is_invisible = models.BooleanField(default=False, verbose_name="Сором'змива дупа")
#     avatar = models.ImageField(upload_to=path_and_rename, null=True, blank=True, verbose_name='Аватар')
#
#     def __str__(self):
#         return str(self.user)
#
#     def get_absolute_url(self):
#         return reverse('user', kwargs={'slug': self.slug})
#
#     # def save(self, *args, **kwargs):
#     #     self.slug = slugify(self.name)
#     #     while (self.slug,) in User.objects.values_list('slug'):
#     #         self.slug += str(random.randint(11111, 99999))
#     #     super(User, self).save(*args, **kwargs)
#
#     class Meta:
#         verbose_name = 'Профіль'
#         verbose_name_plural = 'Профілі'
#         ordering = ['id']
#
#
#
