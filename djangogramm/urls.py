from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('posts.urls')),
                  path('users/', include('django.contrib.auth.urls')),
                  path('users/', include('users.urls')),
                  path('tags/', include('tags.urls')),
                  path('create_db/', include('create_db.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# def pageNotFound(request, exception):
#     return HttpResponseNotFound('<h1>Сторінка не знайдена</h1>')

# handler404 = pageNotFound
