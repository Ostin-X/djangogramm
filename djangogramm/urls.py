"""djangogramm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('posts.urls')),
                  path('users/', include('users.urls')),
                  path('tags/', include('tags.urls')),
                  path('create_db/', include('create_db.urls')),
              ] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

# def pageNotFound(request, exception):
#     return HttpResponseNotFound('<h1>Сторінка не знайдена</h1>')

# handler404 = pageNotFound
