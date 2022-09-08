from django.contrib.auth import login
from django.urls import path
from .views import UserListView, UserDetailView, UserUpdateView, UserRegisterView, UserDeleteView

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('login/', login, name='login'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
]
