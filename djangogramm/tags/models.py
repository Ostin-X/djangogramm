from django.db import models
from ..posts.models import Post


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=100)
