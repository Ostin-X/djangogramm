from django.urls import path
from .views import *

urlpatterns = [
    path('<int:post_id>/', posts_here),
    path('', posts_here),
]
