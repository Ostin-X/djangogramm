from django.contrib import admin

from .models import Post, Like, Image, Tag

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Image)
admin.site.register(Tag)
