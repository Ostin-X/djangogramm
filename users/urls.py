from django.contrib.auth import login
from django.urls import path

from .views import UserListView, UserDetailView, UserUpdateView, ProfileUpdateView, UserRegisterView, UserDeleteView, \
    PasswordChangeCustomView, PasswordChangeSuccess

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('login/', login, name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/update_user/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/password/', PasswordChangeCustomView.as_view(), name='user_password'),
    path('<int:pk>/password_success/', PasswordChangeSuccess.as_view(), name='password_success'),
    path('<int:pk>/update_profile/', ProfileUpdateView.as_view(), name='profile_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
]
