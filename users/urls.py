from django.contrib.auth import login
from django.urls import path
from django.contrib.auth import views

from .views import UserListView, UserDetailView, UserUpdateView, ProfileUpdateView, UserRegisterView, UserDeleteView, \
    PasswordChangeCustomView, password_success

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('login/', login, name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/update_user/', UserUpdateView.as_view(), name='user_update'),
    # path('<int:pk>/password/', views.PasswordChangeView.as_view(template_name='registration/change_password.html'),
    #      name='user_password'),
    path('<int:pk>/password/', PasswordChangeCustomView.as_view(), name='user_password'),
    path('<int:pk>/password_success/', password_success, name='password_success'),
    path('<int:pk>/update_profile/', ProfileUpdateView.as_view(), name='profile_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
]
