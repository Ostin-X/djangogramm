from django.db import models
from django.utils import timezone
from django.urls import reverse

from users.models import User
from tags.models import Tag


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)  # auto_now_add=True

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # , related_name = 'posts'

    tags = models.ManyToManyField(Tag)

    def __repr__(self):
        return f'<Post {self.title}>'

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.id})


class Image(models.Model):
    image = models.FileField(upload_to='images/')
    date = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __repr__(self):
        return f'<Image {self.id}>'

    def get_absolute_url(self):
        return reverse('image', kwargs={'image_id': self.id})


class Like(models.Model):
    date = models.DateTimeField(default=timezone.now)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __repr__(self):
        return f'<Like {self.id}>'
