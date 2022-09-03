from django.urls import path

# from .views import index
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, ImageCreateView

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('posts', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/create_post/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/create_image/', ImageCreateView.as_view(), name='image_create'),

]
