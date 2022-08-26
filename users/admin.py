from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'password', 'avatar')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'bio')
    list_editable = ('password',)
    list_filter = ('name',)


admin.site.register(User, UserAdmin)
