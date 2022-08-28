from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

from .forms import CreateUserForm
from .models import User


def index(request):
    users_list = User.objects.all()
    return render(request, 'users.html', {'users': users_list, 'title': 'Users'})


def user_view(request, user_id: int = None, user_name: str = None):
    if user_id:
        user = get_object_or_404(User, id=user_id)
    else:
        user = get_object_or_404(User, name=user_name)

    return render(request, 'user.html', {'user': user, 'title': user.name})


def create_user(request):
    if request.method == 'Post':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            try:
                User.objects.create(**form.cleaned_data)
                return redirect ('home')
            except:
                form.add_error(None, 'Помилка створення користувача')
    else:
        form = CreateUserForm()
    return render(request, 'create_user.html', {'form': form, 'title': 'Create User'})
