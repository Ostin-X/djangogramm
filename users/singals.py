import os
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from imagekit.utils import get_cache

from create_db.views import fake
from users.models import User, Profile


@receiver(post_save, sender=User)
def auto_create_profile(sender, instance, **kwargs):
    '''
    Create Profile object
    when User is created
    '''
    if not Profile.objects.filter(user=instance).exists():
        Profile.objects.create(user=instance, bio=fake.text())


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

    if instance.avatar_thumbnail:
        if os.path.isfile(instance.avatar_thumbnail.path):
            os.remove(instance.avatar_thumbnail.path)
