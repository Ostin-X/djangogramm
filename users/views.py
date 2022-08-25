from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse

from templates.menu import menu
from .models import User

def index(request):
    users_list = User.objects.all()
    return render(request, 'users.html', {'menu': menu, 'users': users_list})


def user_view(request, user_id: int = None, user_name: str = None):
    if user_id:
        try:
            user = User.objects.get(id=user_id)
        except Exception:
            return HttpResponseNotFound('User not found')
    else:
        try:
            user = User.objects.get(name=user_name)
        except Exception:
            return HttpResponseNotFound('User not found')
    return render(request, 'user.html', {'menu': menu, 'user': user})

# def pageNotFound(request, exception):
#     return HttpResponseNotFound('<h1>Сторінка не знайдена</h1>')
