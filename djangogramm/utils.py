from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect, request
from django.views import View

menu = [
    {"name": "Пости", "url": "post_list"},
    {"name": "Новий пост", "url": "post_create"},
    {"name": "Користувачі", "url": "user_list"},
    {"name": "Таги", "url": "tag_list"},
    # {"name": "Reset DB", "url": "create_db"},
    {"name": "Admin", "url": "admin:index"},
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu = menu[:1] + menu[2:-1]
        context['menu'] = user_menu
        return context


class NotLoggedAllow(UserPassesTestMixin):
    # login_url = '/profile/'

    def test_func(self):
        return not self.request.user.is_authenticated
