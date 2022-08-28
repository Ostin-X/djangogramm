from django.urls import path
from .views import index, user_view, create_user

urlpatterns = [
    path('create_user', create_user, name='create_user'),
    path('<int:user_id>/', user_view, name='user'),
    path('<str:user_name>/', user_view, name='user_name_name'),
    path('', index),
]
