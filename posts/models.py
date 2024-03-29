# from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.urls import reverse
import os

from django.contrib.auth.models import User


def path_and_rename(instance, filename):
    if isinstance(instance, Profile):
        upload_to = 'avatars/'
        inst_pk = instance.pk
    else:
        upload_to = 'images/'
        inst_pk = instance.post_id
    ext = filename.split('.')[-1]
    filename = f'{upload_to[:-1]}_{inst_pk}.{ext}'
    return os.path.join(upload_to, filename)


def path_and_rename_thumbnail(instance, filename):
    filepath_list = path_and_rename(instance, filename).split('.')
    filepath_list[0] += '_thumbnail'
    return '.'.join(filepath_list)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True, verbose_name='Про себе')

    avatar = models.ImageField(upload_to=path_and_rename, null=True, blank=True, verbose_name='Аватарка')
    avatar_thumbnail = models.ImageField(upload_to=path_and_rename_thumbnail, null=True, blank=True,
                                         verbose_name='Тамбнейл')

    following = models.ManyToManyField('Profile', symmetrical=False, blank=True, related_name='followers')

    is_invisible = models.BooleanField(default=False, verbose_name="Сором'язлива дупа")

    def __str__(self):
        return f'Profile of {str(self.user)} {self.user.pk}'

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.user.pk})

    def sub_exists(self, user_object):
        if self.following.contains(user_object):
            return 'active'
        else:
            return 'inactive'

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
    date = models.DateTimeField(auto_now_add=True)  # auto_now_add=True

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_image = models.ForeignKey('Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'{self.title} | {str(self.user)}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    @property
    def total_likes(self):
        return self.like_set.count()

    def make_first(self, new_img_object):
        if new_img_object in self.image_set.all():
            if hasattr(self, 'first_image') and new_img_object != self.first_image:
                self.first_image = new_img_object
                self.save()

    def like_exists(self, user_object):
        if Like.objects.filter(post=self, user=user_object).exists():
            return 'active'
        else:
            return 'inactive'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'
        ordering = ['id']


class Image(models.Model):
    date = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to=path_and_rename, verbose_name='Зображення')
    image_thumbnail = models.ImageField(upload_to=path_and_rename_thumbnail, null=True, blank=True,
                                        verbose_name='Тамбнейл')

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
    date = models.DateTimeField(auto_now_add=True)  # default=timezone.now

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Like {self.id} for Post {self.post}'

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        ordering = ['id']
        # unique_together = [['post', 'user']]
        constraints = [
            models.UniqueConstraint(
                fields=['post', 'user'],
                name='like_exists',
            )
        ]
