from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

# from .forms import CreateUserForm
# from .models import Profile
from .utils import DataMixin


class UserList(DataMixin, ListView):
    paginate_by = 10
    model = User
    allow_empty = False

    # template_name = 'users.html'
    # extra_context = {'title': 'Users'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserList, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='Користувачі')
        return dict(list(context.items()) + list(c_def.items()))

    # def get_queryset(self):
    #     return User.objects.filter(is_invisible=False)


class UserDetail(LoginRequiredMixin, DataMixin, DetailView):
    model = User
    allow_empty = False
    # login_url = '/admin/'
    login_url = reverse_lazy('users')
    raise_exception = True

    # slug_url_kwarg = 'user_slug'
    # pk_url_kwarg = 'user_pk'
    # context_object_name = 'one_user'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['user'])
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RegisterUser, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='Створити користувача')
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(DataMixin, CreateView):
    form_class = UserCreationForm
    # success_url = reverse_lazy('users')
    template_name = 'users/register.html'

    def get_success_url(self):
        return reverse('mainapp:profile')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LoginUser, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='Створити користувача')
        return dict(list(context.items()) + list(c_def.items()))


class UserCreate(DataMixin, CreateView):
    # form_class = CreateUserForm
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreate, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='Створити користувача')
        return dict(list(context.items()) + list(c_def.items()))
