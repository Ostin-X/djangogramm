from django.db import models
from django.utils import timezone
from users.models import User
from .tags.models import Tag


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # , related_name = 'posts'

    tags = models.ManyToManyField(Tag)

    def __repr__(self):
        return f'<Post {self.id}>'


class ImageFile(models.Model):
    image = models.FileField()
    image_data = models.BinaryField(null=True)
    date = models.DateTimeField(default=timezone.now)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __repr__(self):
        return f'<Image {self.id}>'


class Like(models.Model):
    date = models.DateTimeField(default=timezone.now)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __repr__(self):
        return f'<Like {self.id}>'
