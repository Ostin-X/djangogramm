from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from posts.views_create_db import create_all_db


urlpatterns = [
                  # path('create_db', create_all_db),
                  path('admin/', admin.site.urls),
                  path('', include('posts.urls')),
                  path('users/', include('django.contrib.auth.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# def pageNotFound(request, exception):
#     return HttpResponseNotFound('<h1>Сторінка не знайдена</h1>')

# handler404 = pageNotFound
