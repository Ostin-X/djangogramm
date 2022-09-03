from django.urls import path
from .views import UserList, UserDetail, UserCreate, RegisterUser, LoginUser

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    # path('login/', LoginUser.as_view(), name='login'),
    path('<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('', UserList.as_view(), name='users'),
]
