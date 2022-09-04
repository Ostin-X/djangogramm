import os

from django.db import models
from django.utils import timezone
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# from users.models import Profile
from django.contrib.auth.models import User
from tags.models import Tag


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)  # auto_now_add=True

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # , related_name = 'posts'

    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f'{self.title} | {str(self.user)}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})


def image_dir(instance, filename):
    upload_to = 'images/'
    inst_pk = instance.post.pk
    upload_to += str(inst_pk)
    return os.path.join(upload_to, filename)


class Image(models.Model):
    date = models.DateTimeField(default=timezone.now)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    image = models.FileField(upload_to=image_dir)
    image_thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(70, 100)], format='JPEG',
                                     options={'quality': 60}, )

    # post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Image, self).delete(*args, **kwargs)

    def __repr__(self):
        return f'<Image {self.id}>'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.post.pk})


class Like(models.Model):
    date = models.DateTimeField(default=timezone.now)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __repr__(self):
        return f'<Like {self.id}>'
