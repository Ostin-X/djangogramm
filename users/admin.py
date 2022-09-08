from django.contrib import admin
from django.contrib.admin import display

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'avatar', 'is_invisible')  # , 'user.name', 'email', 'password'
    list_display_links = ('id', 'get_user')
    search_fields = ('get_user', 'bio')
    list_editable = ('is_invisible',)

    # ordering = ('id',)
    # list_filter = ('is_invisible',)
    # prepopulated_fields = {'slug': ('name',)}

    @display(ordering='book__author', description='Користувач')
    def get_user(self, obj):
        return obj.user

    get_user.admin_order_field = 'user'


admin.site.register(Profile, ProfileAdmin)
