from django.urls import path

from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, ImageCreateView, \
    TagListView, TagDetailView, ImageUpdateView, ImageDeleteView
from .views_create_db import create_all_db

urlpatterns = [
    # path('/admin_too/', admin.site.urls, name='admin_path'),
    path('create_db/', create_all_db, name='create_db'),
    path('', PostListView.as_view(), name='home'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/create_post/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('posts/<int:pk>/create_image/', ImageCreateView.as_view(), name='image_create'),
    path('posts/<int:pk>/images/', ImageUpdateView.as_view(), name='image_update'),
    path('posts/<int:post_pk>/images/<int:pk>', ImageDeleteView.as_view(), name='image_delete'),
    path('posts/tags/', TagListView.as_view(), name='tag_list'),
    path('posts/tags/<int:pk>/', TagDetailView.as_view(), name='tag_detail'),
]
