from django.urls import path
from .views import create_all_db

urlpatterns = [
    path('', create_all_db),
]
