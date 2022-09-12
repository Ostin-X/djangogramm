from django.contrib import admin
from django.contrib.admin import display
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from .models import User, Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'avatar', 'is_invisible')
    list_display_links = ('id', 'user')
    search_fields = ('user', 'bio')
    list_editable = ('is_invisible',)
    readonly_fields = ('user', 'get_email')

    # ordering = ('id',)
    # list_filter = ('is_invisible',)
    # prepopulated_fields = {'slug': ('name',)}

    @display(description='Email')
    def get_email(self, obj):
        return obj.user.email


class ProfileAdminInline(admin.StackedInline):
    model = Profile
    max_num = 1
    can_delete = False


class UserAdmin(AuthUserAdmin):
    inlines = [ProfileAdminInline]


admin.site.register(Profile, ProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
