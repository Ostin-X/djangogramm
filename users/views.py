from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse

from templates.settings import menu
from .models import User

users_list = User.objects.all()


def index(request):
    return render(request, 'users.html', {'menu': menu, 'users': users_list})


def user_view(request, user_id: int = None, user_name: str = None):
    if user_id:
        print(user_id)
        user = User.objects.get(id=5219)
        print(user)
    # elif user_name:
    #     print(reverse('user_name_name', args=[user_name]))
    #     return HttpResponse(f'User name-{user_name} here')
    # else:
    #     return HttpResponseNotFound('Users here')
    return render(request, 'user.html', {'menu': menu, 'user': user})

# def pageNotFound(request, exception):
#     return HttpResponseNotFound('<h1>Сторінка не знайдена</h1>')
