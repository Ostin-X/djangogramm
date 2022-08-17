from django.db import models


class User(models.Model):
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    bio = models.CharField(max_length=1000)
    avatar = models.ImageField()

    def __repr__(self):
        return f'<User {self.id}>'
