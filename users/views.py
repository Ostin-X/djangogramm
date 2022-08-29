from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

from .forms import CreateUserForm
from .models import User


class UserList(ListView):
    model = User
    allow_empty = False

    # template_name = 'users.html'
    # extra_context = {'title': 'Users'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserList, self).get_context_data(**kwargs)
        context['title'] = 'Users'
        return context

    def get_queryset(self):
        return User.objects.filter(is_invisible=False)


# def users(request):
#     users_list = User.objects.all()
#     return render(request, 'user_list.html', {'users': users_list, 'title': 'Users'})


class UserDetail(DetailView):
    model = User
    allow_empty = False

    # slug_url_kwarg = 'user_slug'
    # pk_url_kwarg = 'user_pk'
    # context_object_name = 'one_user'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        context['title'] = context['user']
        return context


# def user_view(request, user_id: int = None, slug: str = None):
#     # if user_id:
#     #     user = get_object_or_404(User, pk=user_id)
#     # else:
#     user = get_object_or_404(User, slug=slug)
#
#     return render(request, 'user.html', {'user': user, 'title': user.name})


class UserCreate(CreateView):
    form_class = CreateUserForm
    template_name = 'users/user_create.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreate, self).get_context_data(**kwargs)
        context['title'] = 'Create User'
        return context


# def create_user(request):
#     if request.method == 'POST':
#         form = CreateUserForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('users')
#     else:
#         form = CreateUserForm()
#     return render(request, 'users/user_create.html', {'form': form, 'title': 'Create User'})
