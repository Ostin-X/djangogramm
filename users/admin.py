from django.contrib import admin

from .models import Profile


# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'email', 'password', 'avatar', 'is_invisible')
#     list_display_links = ('id', 'name')
#     search_fields = ('name', 'bio')
#     list_editable = ('is_invisible',)
#     # prepopulated_fields = {'slug': ('name',)}
#     # list_filter = ('name',)


admin.site.register(Profile) #, UserAdmin
