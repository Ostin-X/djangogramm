from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Tag
from posts.models import Post

@receiver(post_delete, sender=Post)
def delete_empty_tags(sender, **kwargs):
    Tag.objects.filter(post=None).delete()
