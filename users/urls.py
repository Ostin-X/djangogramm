from django.urls import path
from .views import index, user_view

urlpatterns = [
    path('<int:user_id>/', user_view, name='user_id_name'),
    path('<str:user_name>/', user_view, name='user_name_name'),
    path('', index),
]
