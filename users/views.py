from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse


def users_here(request, user_id: int = None, user_name: str = None):
    if user_id:
        return HttpResponse(f'User id-{user_id} here')
    elif user_name:
        print(reverse('user_name_name', args=[user_name]))
        return HttpResponse(f'User name-{user_name} here')
    else:
        return HttpResponseNotFound('Users here')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Сторінка не знайдена</h1>')
