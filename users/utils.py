import os
import glob

from djangogramm.settings import BASE_DIR

menu = [{"name": "Posts", "url": "/"},
        {"name": "Users", "url": "/users"},
        {"name": "Tags", "url": "/tags"},
        # {"name": "Create User", "url": "/users/create_user"},
        {"name": "Reset DB", "url": "/create_db"},
        {"name": "Admin", "url": "/admin"},
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
    file_list = glob.glob(os.path.join(BASE_DIR, f'media/avatars/{inst_pk}.*')) + glob.glob(
        os.path.join(BASE_DIR, f'media/avatars/{inst_pk}_*'))
    for file_path in file_list:
        try:
            os.remove(file_path)
        except OSError:
            print("Error while deleting file")
    filename = f'{inst_pk}.{ext}'

    return os.path.join(upload_to, filename)
