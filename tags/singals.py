import os
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from imagekit.utils import get_cache

from create_db.views import fake
from djangogramm.settings import MEDIA_ROOT
from django.contrib.auth.models import User
from users.models import Profile
from .models import Tag
from posts.models import Post, Image


@receiver(post_save, sender=User)
def auto_create_profile(sender, instance, **kwargs):
    if not Profile.objects.filter(user=instance).exists():
        Profile.objects.create(user=instance, bio=fake.text())


@receiver(post_delete, sender=Post)
def auto_delete_empty_tags(sender, **kwargs):
    Tag.objects.filter(post=None).delete()


@receiver(post_delete, sender=Image)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    get_cache().clear()
    root = MEDIA_ROOT
    folders = list(os.walk(root))[1:]

    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    try:
        if instance.image:

            # if os.path.isfile(instance.image.path):
            if os.path.exists(instance.image.path):
                os.remove(instance.image.path)
    except:
        pass
    try:
        if instance.image_thumbnail:
            # if os.path.isfile(instance.image_thumbnail.path):
            if os.path.exists(instance.image_thumbnail.path):
                os.remove(instance.image_thumbnail.path)
    except:
        pass

    for folder in folders:
        # folder example: ('FOLDER/3', [], ['file'])
        if not folder[2] and not folder[1]:
            try:
                os.rmdir(folder[0])
            except:
                print(f'ERROR IN {folder}')
                pass


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
