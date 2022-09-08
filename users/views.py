from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login

# from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

from .forms import CustomUserCreationForm, ProfileForm
# from django.contrib.auth.models import User
from .models import User
from djangogramm.utils import DataMixin


class UserListView(DataMixin, ListView):
    paginate_by = 10
    model = User
    allow_empty = True

    # ordering = ['-pk']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='Користувачі')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return User.objects.filter(profile__is_invisible=False).order_by('-pk')


class UserDetailView(LoginRequiredMixin, DataMixin, DetailView):
    model = User

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['user'])
        return dict(list(context.items()) + list(c_def.items()))


class UserUpdateView(LoginRequiredMixin, DataMixin, UpdateView):
    model = User
    form_class = ProfileForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title=f"Редагування профілю {context['user']}")
        return dict(list(context.items()) + list(c_def.items()))


class UserDeleteView(LoginRequiredMixin, DataMixin, DeleteView):
    model = User
    success_url = reverse_lazy('user_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserDeleteView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title=f"Видалення профілю {context['user']}")
        return dict(list(context.items()) + list(c_def.items()))


class UserRegisterView(DataMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='Створити користувача')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(form.instance.profile.get_absolute_url())

# class LoginUserView(DataMixin, CreateView):
#     form_class = UserCreationForm
#     # success_url = reverse_lazy('users')
#     template_name = 'registration/register.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(LoginUserView, self).get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Створити користувача')
#         return dict(list(context.items()) + list(c_def.items()))

# class UserCreate(DataMixin, CreateView):
#     # form_class = CreateUserForm
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'users/user_register.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(UserCreate, self).get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Створити користувача')
#         return dict(list(context.items()) + list(c_def.items()))
