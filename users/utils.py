import os
import glob

from django.conf import settings

menu = [
    {"name": "Posts", "url": "post_list"},
    {"name": "Create Post", "url": "post_create"},
    {"name": "Users", "url": "users"},
    {"name": "Tags", "url": "tag_list"},
    {"name": "Reset DB", "url": "create_db"},
    {"name": "Admin", "url": "admin:index"},
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu = menu[:-2]
        context['menu'] = user_menu
        # if 'menu_selected' not in context:
        #     context['menu_selected'] = 0
        return context


def path_and_rename(instance, filename):
    upload_to = 'avatars/'
    ext = filename.split('.')[-1]
    inst_pk = instance.pk
    file_list = glob.glob(os.path.join(settings.BASE_DIR, f'media/avatars/{inst_pk}.*')) + glob.glob(
        os.path.join(settings.BASE_DIR, f'media/avatars/{inst_pk}_*'))
    for file_path in file_list:
        try:
            os.remove(file_path)
        except OSError:
            print("Error while deleting file")
    filename = f'{inst_pk}.{ext}'

    return os.path.join(upload_to, filename)
