from django.urls import path
from .views import UserList, UserDetail, UserCreate, RegisterUser

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('<slug:slug>/', UserDetail.as_view(), name='user'),
    path('', UserList.as_view(), name='users'),
]
