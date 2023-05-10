from django.urls import path

from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, ImageCreateView, \
    TagListView, TagDetailView, ImageUpdateView, ImageDeleteView, UserListView, UserDetailView, UserUpdateView, \
    ProfileUpdateView, UserRegisterView, UserDeleteView, PasswordChangeCustomView, PasswordChangeSuccess, \
    LoginCustomView, UserActivationView, SubListView

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/create_post/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    path('posts/<int:pk>/create_image/', ImageCreateView.as_view(), name='image_create'),
    path('posts/<int:pk>/images/', ImageUpdateView.as_view(), name='image_update'),
    path('posts/<int:post_pk>/images/<int:pk>/delete/', ImageDeleteView.as_view(), name='image_delete'),

    path('posts/tags/', TagListView.as_view(), name='tag_list'),
    path('posts/tags/<int:pk>/', TagDetailView.as_view(), name='tag_detail'),

    path('users/', UserListView.as_view(), name='user_list'),
    path('users/login/', LoginCustomView.as_view(), name='login'),
    path('users/register/', UserRegisterView.as_view(), name='register'),

    path('users/subs/<int:pk>/', SubListView.as_view(), name='sub_list'),

    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/update_user/', UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/password/', PasswordChangeCustomView.as_view(), name='user_password'),
    path('users/<int:pk>/password_success/', PasswordChangeSuccess.as_view(), name='password_success'),
    path('users/<int:pk>/update_profile/', ProfileUpdateView.as_view(), name='profile_update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),

    path('activate/<str:uidb64>/<str:token>/', UserActivationView.as_view(), name='activate'),

]
