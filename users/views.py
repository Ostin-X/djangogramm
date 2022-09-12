from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordChangeView, TemplateView

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

from .forms import CustomUserCreationForm, UserForm, ProfileForm, PasswordChangeCustomForm
from .models import User, Profile
from djangogramm.utils import DataMixin, NotLoggedAllow


class UserListView(DataMixin, ListView):
    paginate_by = 10
    model = User
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='Користувачі')
        return {**context, **c_def}

    def get_queryset(self):
        return User.objects.filter(profile__is_invisible=False).order_by('-pk')


class UserDetailView(LoginRequiredMixin, DataMixin, DetailView):
    model = User

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['user'])
        return {**context, **c_def}


class UserRegisterView(NotLoggedAllow, DataMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='Створити користувача')
        return {**context, **c_def}

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(form.instance.profile.get_absolute_url())


class UserUpdateView(LoginRequiredMixin, DataMixin, UpdateView):
    model = User
    form_class = UserForm
    second_form_class = ProfileForm

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(pk=self.request.user.pk)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        form2 = ProfileForm(self.request.POST or None, instance=self.request.user.profile)
        c_def = self.get_user_context(title=f"Редагування юзера {context['user']}", form2=form2)
        return {**context, **c_def}

    def get_success_url(self):
        return self.object.profile.get_absolute_url()

    def post(self, request, *args, **kwargs):
        form2 = self.second_form_class(request.POST, request.FILES, instance=request.user.profile)
        if form2.is_valid():
            form2.save()
        return super().post(request, *args, **kwargs)


class ProfileUpdateView(LoginRequiredMixin, DataMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'auth/profile_form.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title=f'Редагування профілю {self.request.user}')
        return {**context, **c_def}

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(pk=self.request.user.pk)


class UserDeleteView(LoginRequiredMixin, DataMixin, DeleteView):
    model = User
    success_url = reverse_lazy('user_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserDeleteView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title=f"Видалення профілю {context['user']}")
        return {**context, **c_def}

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(pk=self.request.user.pk)


class PasswordChangeCustomView(DataMixin, PasswordChangeView):
    form_class = PasswordChangeCustomForm
    template_name = 'registration/change_password.html'

    def get_success_url(self):
        return reverse_lazy('password_success', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PasswordChangeCustomView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title=f"Зміна пароля {self.request.user}")
        return {**context, **c_def}


class PasswordChangeSuccess(LoginRequiredMixin, UserPassesTestMixin, DataMixin, TemplateView):
    template_name = 'registration/password_success.html'

    def test_func(self):
        return self.request.user.pk == self.kwargs['pk']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PasswordChangeSuccess, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title=f"Пароль оновлено {self.request.user}")
        return {**context, **c_def}
