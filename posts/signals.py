import random
import re

from PIL import Image as ImagePIL
from django.db import IntegrityError
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from faker import Faker

from .models import Image, Post, Tag, User, Profile

fake = Faker()


@receiver(post_delete, sender=Post)
def auto_delete_empty_tags(sender, **kwargs):
    Tag.objects.filter(post=None).delete()


@receiver(post_save, sender=Post)
def auto_fill_tags(sender, instance, **kwargs):
    regex = "#(\w+)"
    instance.tags.clear()
    for tag in re.findall(regex, instance.text):
        instance.tags.add(Tag.objects.get_or_create(name=tag.lower())[0])
    auto_delete_empty_tags(Post)


@receiver(post_save, sender=User)
def auto_create_profile(sender, instance, created, **kwargs):
    '''
    Create Profile object
    when User is created
    '''
    # try:
    if created:
        Profile.objects.create(user=instance)  # , bio=fake.text()
    # except IntegrityError:
    #     pass


# @receiver(post_save, sender=Profile)
# def auto_create_thumbnail(sender, instance, **kwargs):
#     '''
#     Create or delete thumbnail
#     when Profile is saved
#     '''
#     avatar = instance.avatar
#     thumbnail = instance.avatar_thumbnail
#
#     if avatar:
#         thumbnail_path = add_thumbnail_to_name(avatar.path)
#         img = ImagePIL.open(avatar.path)
#         # if img.height > 300 or img.width > 300:
#         output_size = (300, 300)
#         img.thumbnail(output_size)
#         img.save(thumbnail_path)
#         Profile.objects.filter(pk=instance.pk).update(avatar_thumbnail=add_thumbnail_to_name(avatar.name))
#     elif thumbnail:
#         instance.avatar_thumbnail = ''
#         instance.save()
#
#
# def add_thumbnail_to_name(path):
#     path_splited = path.split('.')
#     path_splited[-2] += '_thumbnail'
#     return '.'.join(path_splited)
#
#
# @receiver(post_save, sender=Image)
# def auto_create_thumbnail(sender, instance, **kwargs):
#     '''
#     Create or delete thumbnail
#     when Profile is saved
#     '''
#     avatar = instance.image
#     thumbnail = instance.image_thumbnail
#
#     if avatar:
#         thumbnail_path = add_thumbnail_to_name(avatar.path)
#         img = ImagePIL.open(avatar.path)
#         # if img.height > 300 or img.width > 300:
#         output_size = (100, 100)
#         img.thumbnail(output_size)
#         img.save(thumbnail_path)
#         Image.objects.filter(pk=instance.pk).update(image_thumbnail=add_thumbnail_to_name(avatar.name))
#     elif thumbnail:
#         instance.image_thumbnail = ''
#         instance.save()
#
#
# def add_thumbnail_to_name(path):
#     path_splited = path.split('.')
#     path_splited[-2] += '_thumbnail'
#     return '.'.join(path_splited)
