from django.contrib import admin
from django.contrib.admin import display
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from .models import Post, Like, Image, Tag, User, Profile


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
    list_display = ('id', 'username', 'is_active',)
    list_display_links = ('id', 'username')
    list_editable = ('is_active',)


class ImageAdminInline(admin.StackedInline):
    model = Image
    can_delete = True
    fk_name = 'post'
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [ImageAdminInline]
    list_display = ('id', 'title', 'user')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'user')
    readonly_fields = ('user', 'get_likes_count')

    @display(description='Likes')
    def get_likes_count(self, obj):
        return obj.like_set.count()


class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user')
    search_fields = ('post', 'user')


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user')
    search_fields = ('post', 'user')


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Tag, TagAdmin)
