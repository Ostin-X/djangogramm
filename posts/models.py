from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.urls import reverse
import os

from django.contrib.auth.models import User
from django.conf import settings


def path_and_rename(instance, filename):
    if isinstance(instance, Profile):
        upload_to = 'avatars/'
        inst_pk = instance.pk
    else:
        upload_to = 'images/'
        inst_pk = instance.post_id
    ext = filename.split('.')[-1]
    filename = f'{upload_to[:-1]}_{inst_pk}.{ext}'
    if upload_to == 'avatars/' and os.path.exists(os.path.join(settings.MEDIA_ROOT, upload_to, filename)):
        os.remove(os.path.join(settings.MEDIA_ROOT, upload_to, filename))
    print(os.path.join(upload_to, filename))
    print(os.path.join(settings.MEDIA_ROOT, upload_to, filename))
    return os.path.join(upload_to, filename)
    # return os.path.join(settings.MEDIA_ROOT, upload_to, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True, verbose_name='Про себе')

    avatar = models.ImageField(upload_to=path_and_rename, null=True, blank=True, verbose_name='Аватарка')
    # avatar = models.ImageField(upload_to='avatars', null=True, blank=True, verbose_name='Аватарка')
    avatar_thumbnail = models.ImageField(null=True, blank=True, verbose_name='Тамбнейл')

    following = models.ManyToManyField('Profile', symmetrical=False, null=True, blank=True, related_name='followers')

    is_invisible = models.BooleanField(default=False, verbose_name="Сором'язлива дупа")

    def __str__(self):
        return f'Profile of {str(self.user)} {self.user.pk}'

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.user.pk})

    def sub_exists(self, user_object):
        return self.following.contains(user_object)

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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_image = models.ForeignKey('Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    tags = models.ManyToManyField(Tag, null=True, blank=True)

    def __str__(self):
        return f'{self.title} | {str(self.user)}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.like_set.count()

    def make_first(self, new_img_object):
        if new_img_object in self.image_set.all():
            if hasattr(self, 'first_image') and new_img_object != self.first_image:
                self.first_image = new_img_object
                self.save()

    def like_exists(self, user_object):
        return Like.objects.filter(post=self, user=user_object).exists()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'
        ordering = ['id']


class Image(models.Model):
    date = models.DateTimeField(default=timezone.now)

    image = models.ImageField(upload_to=path_and_rename, verbose_name='Зображення')
    image_thumbnail = models.ImageField(null=True, blank=True, verbose_name='Тамбнейл')

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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
