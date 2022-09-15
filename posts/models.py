from django.db import models
from django.utils import timezone
from django.urls import reverse
import os

from django.contrib.auth.models import User
from djangogramm.settings import MEDIA_ROOT


def path_and_rename(instance, filename):
    if 'Profile' in str(instance):
        upload_to = 'avatars/'
        inst_pk = instance.pk
    else:
        upload_to = 'images/'
        inst_pk = instance.post_id
    ext = filename.split('.')[-1]
    filename = f'{upload_to[:-1]}_{inst_pk}.{ext}'
    if upload_to == 'avatars/' and os.path.exists(os.path.join(MEDIA_ROOT, upload_to, filename)):
        os.remove(os.path.join(MEDIA_ROOT, upload_to, filename))
    return os.path.join(upload_to, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True, verbose_name='Про себе')

    avatar = models.ImageField(upload_to=path_and_rename, null=True, blank=True, verbose_name='Аватарка')
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


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['id']


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)  # auto_now_add=True

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # , related_name = 'posts'

    tags = models.ManyToManyField(Tag)

    # first_image = models.PositiveIntegerField(null=True, blank=True, verbose_name='pk першого зображення')

    def __str__(self):
        return f'{self.title} | {str(self.user)}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def make_first(self, new_img_object):
        print('make_first(self, new_img_object)')
        if new_img_object in self.image_set.all():
            if hasattr(self, 'first_image'):
                old_img_obj = self.first_image
                old_img_obj.is_first = None
                old_img_obj.save()
            self.first_image = new_img_object
            new_img_object.save()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'
        ordering = ['id']


class Image(models.Model):
    date = models.DateTimeField(default=timezone.now)

    image = models.FileField(upload_to=path_and_rename, verbose_name='Зображення')
    image_thumbnail = models.ImageField(null=True, blank=True, verbose_name='Тамбнейл')

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    is_first = models.OneToOneField(Post, null=True, blank=True, related_name='first_image', on_delete=models.CASCADE)

    def __str__(self):
        return f'Image {self.pk} of Post {self.post}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.post.pk})

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'
        ordering = ['id']


class Like(models.Model):
    date = models.DateTimeField(default=timezone.now)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Like {self.id} for Post {self.post}'

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        ordering = ['id']
