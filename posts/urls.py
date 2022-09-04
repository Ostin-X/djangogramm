from django.urls import path

# from .views import index
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, ImageCreateView

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/create_post/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('posts/<int:pk>/create_image/', ImageCreateView.as_view(), name='image_create'),

]
