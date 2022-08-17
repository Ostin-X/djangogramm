from django.urls import path
from .views import *

urlpatterns = [
    path('<int:user_id>/', users_here, name = 'user_id_name'),
    path('<str:user_name>/', users_here, name = 'user_name_name'),
    path('', users_here),
]
