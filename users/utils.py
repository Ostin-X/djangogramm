import os
import glob

from djangogramm.settings import BASE_DIR


# class DataMixin:
#     def get_user_context(self, **kwargs):
#         context = kwargs
#         context['title'] = 'Users'
#         return context


def path_and_rename(instance, filename):
    upload_to = 'avatars/'
    ext = filename.split('.')[-1]
    inst_pk = instance.pk
    file_list = glob.glob(os.path.join(BASE_DIR, f'media/avatars/{inst_pk}.*')) + glob.glob(
        os.path.join(BASE_DIR, f'media/avatars/{inst_pk}_*'))
    for file_path in file_list:
        try:
            os.remove(file_path)
        except OSError:
            print("Error while deleting file")
    filename = f'{inst_pk}.{ext}'

    return os.path.join(upload_to, filename)
