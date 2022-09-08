menu = [
    {"name": "Пости", "url": "post_list"},
    {"name": "Новий пост", "url": "post_create"},
    {"name": "Користувачі", "url": "user_list"},
    {"name": "Таги", "url": "tag_list"},
    {"name": "Reset DB", "url": "create_db"},
    {"name": "Admin", "url": "admin:index"},
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu = menu[:1] + menu[2:-2]
        context['menu'] = user_menu
        return context
