import os
import shutil

from django.db.models.signals import post_delete
from django.dispatch import receiver
from imagekit.utils import get_cache

from djangogramm.settings import MEDIA_ROOT
from users.models import Profile
from .models import Tag
from posts.models import Post, Image


@receiver(post_delete, sender=Post)
def auto_delete_empty_tags(sender, **kwargs):
    Tag.objects.filter(post=None).delete()


@receiver(post_delete, sender=Image)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    get_cache().clear()
    root = MEDIA_ROOT
    print(root+'\CACHE')
    os.rmdir(root+'\CACHE')
    print(root+'\CACHE')
    folders = list(os.walk(root))[1:]
    for folder in folders:
        print(folder)
        # folder example: ('FOLDER/3', [], ['file'])
        if not folder[2] and not folder[1]:
            shutil.rmtree(folder[0])
            # os.rmdir(folder[0])
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(post_delete, sender=Profile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    get_cache().clear()
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)
