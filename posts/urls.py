from django.urls import path
from .views import index

urlpatterns = [
    path('<int:post_id>/', index),
    path('', index),
]
