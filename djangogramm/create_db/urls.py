from django.urls import path
from .views import create_all_db

urlpatterns = [
    # path('<int:user_id>/', users_here, name='user_id_name'),
    # path('<str:user_name>/', users_here, name='user_name_name'),
    path('', create_all_db),
]
