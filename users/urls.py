from django.urls import path
from .views import UserList, UserDetail, UserCreate

urlpatterns = [
    path('create_user/', UserCreate.as_view(), name='create_user'),
    path('<slug:slug>/', UserDetail.as_view(), name='user'),
    path('', UserList.as_view(), name='users'),
]
