# from PIL import Image
# from django.db.models.signals import post_delete, post_save, pre_save
# from django.dispatch import receiver
#
# from posts.views_create_db import fake
# from .models import User, Profile
#
#
# @receiver(post_save, sender=User)
# def auto_create_profile(sender, instance, **kwargs):
#     '''
#     Create Profile object
#     when User is created
#     '''
#     if not Profile.objects.filter(user=instance).exists():
#         Profile.objects.create(user=instance, bio=fake.text())
#
#
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
#         img = Image.open(avatar.path)
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
# # @receiver(pre_save, sender=Profile)
# # def auto_delete_file_on_delete(sender, instance, **kwargs):
# #     # get_cache().clear()
# #     print(get_cache())
# #     """
# #     Deletes file from filesystem
# #     when corresponding `MediaFile` object is deleted.
# #     """
# #     if instance.avatar:
# #         if os.path.isfile(instance.avatar.path):
# #             os.remove(instance.avatar.path)
# #
# #         if instance.avatar_thumbnail and os.path.isfile(instance.avatar_thumbnail.path):
# #             os.remove(instance.avatar_thumbnail.path)
#
#
# # @receiver(post_delete, sender=Profile)
# # def auto_delete_file_on_delete(sender, instance, **kwargs):
# #     get_cache().clear()
# #     """
# #     Deletes file from filesystem
# #     when corresponding `MediaFile` object is deleted.
# #     """
# #     # if instance.avatar:
# #     #     if os.path.isfile(instance.avatar.path):
# #     #         os.remove(instance.avatar.path)
# #
# #     if instance.avatar_thumbnail:
# #         if os.path.isfile(instance.avatar_thumbnail.path):
# #             os.remove(instance.avatar_thumbnail.path)
