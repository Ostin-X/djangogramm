from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordChangeView, TemplateView, LoginView

from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .utils import DataMixin, NotLoggedAllow

from .models import Post, Image, Tag, User, Profile, Like
from .forms import PostForm, ImageForm, CustomUserCreationForm, UserForm, ProfileForm, PasswordChangeCustomForm


class LoginCustomView(DataMixin, LoginView):
    extra_context = {'title': 'Posts'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LoginCustomView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='Логін')
        return {**context, **c_def}


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
        self.object = self.get_object()
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


class PostListView(DataMixin, ListView):
    model = Post
    paginate_by = 10
    context_object_name = 'posts'

    # extra_context = {'title': 'Posts'}

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='Пости')
        return {**context, **c_def}

    def get_queryset(self):
        return Post.objects.filter().order_by('-date')  # post__is_invisible=False


def like_post(request, pk):
    post_object = get_object_or_404(Post, id=request.POST.get('post_pk'))
    like_object = Like.objects.filter(user=request.user, post=post_object)
    if like_object.exists():
        like_object.delete()
    else:
        Like.objects.create(user=request.user, post=post_object)
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))


def image_make_first(request, post_pk, pk):
    post_object = get_object_or_404(Post, id=post_pk)
    image_object = get_object_or_404(Image, id=pk)
    post_object.make_first(image_object)
    return HttpResponseRedirect(reverse('image_update', args=[str(post_pk)]))


class PostDetailView(LoginRequiredMixin, DataMixin, DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'].title)
        return {**context, **c_def}


class PostCreateView(LoginRequiredMixin, DataMixin, CreateView):
    model = Post
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='Новий пост')
        return {**context, **c_def}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PostCreateView, self).form_valid(form)


# class PostUpdateView(LoginRequiredMixin, DataMixin, UpdateView):
#     model = Post
#     form_class = PostForm
#     second_form_class = ImageForm
#
#     def get_queryset(self, *args, **kwargs):
#         return super().get_queryset().filter(user=self.request.user)
#
#     def get_context_data(self, **kwargs):
#         context = super(PostUpdateView, self).get_context_data(**kwargs)
#         obj = get_object_or_404(Post, id=self.request.resolver_match.kwargs['pk'])
#         # print(obj.image_set)
#         # print(self.request.resolver_match.kwargs['pk'])
#         image_set = obj.image_set.all()
#         if image_set:
#             for image in image_set:
#                 form2 = ImageForm(self.request.FILES or None,
#                                   instance=image)  # , instance=self.request.image_set self.request.Post or None,
#         else:
#             form2 = ImageForm(self.request.FILES or None)
#         c_def = self.get_user_context(title='Редагувати пост', form2=form2)
#         return {**context, **c_def}
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form2 = self.second_form_class(request.FILES)
#         print(request.FILES.__dict__)
#         if 'image' in request.FILES:
#             print(request.FILES['image'])
#             form2.instance.user = self.request.user
#             form2.instance.post = Post.objects.get(pk=self.object.pk)
#             form2.instance.image = request.FILES['image'].get()
#             # form2.instance.image =
#             print(form2.instance.__dict__)
#             print(form2.instance.image)
#             if form2.is_valid():
#                 print('--------------VALID_--------')
#                 form2.save()
#         return super().post(request, *args, **kwargs)


class PostUpdateView(LoginRequiredMixin, DataMixin, UpdateView):
    model = Post
    form_class = PostForm

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='Редагувати пост')
        return {**context, **c_def}


class PostDeleteView(LoginRequiredMixin, DataMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(PostDeleteView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title=f'Видалити пост "{self.object.title}"')
        return {**context, **c_def}


class ImageCreateView(LoginRequiredMixin, UserPassesTestMixin, DataMixin, CreateView):
    model = Image
    form_class = ImageForm

    def test_func(self):
        return self.request.user.pk == Post.objects.get(pk=self.kwargs['pk']).user_id

    def get_context_data(self, **kwargs):
        context = super(ImageCreateView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(
            title=f"Додати зображення до поста {Post.objects.get(pk=self.kwargs['pk']).title}")
        return {**context, **c_def}

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        return super(ImageCreateView, self).form_valid(form)


class ImageUpdateView(LoginRequiredMixin, UserPassesTestMixin, DataMixin, TemplateView):
    template_name = 'posts/image_update.html'

    def test_func(self):
        return self.request.user.pk == Post.objects.get(pk=self.kwargs['pk']).user_id

    def get_context_data(self, **kwargs):
        context = super(ImageUpdateView, self).get_context_data(**kwargs)
        post_object = Post.objects.get(pk=self.kwargs['pk'])
        # post_object.make_first(Post.objects.get(pk=self.kwargs['pk']).image_set.get(pk=1))
        c_def = self.get_user_context(
            title=f"Редагувати зображення поста {Post.objects.get(pk=self.kwargs['pk']).title}", object=post_object)
        return {**context, **c_def}

    # def post(self, request, *args, **kwargs):
    #     print(request.POST)
    #     return self.get(request, *args, **kwargs)

    # def from_valid(self, form):
    #     print(self.request.POST)


class ImageDeleteView(LoginRequiredMixin, DataMixin, DeleteView):
    model = Image
    template_name = 'posts/image_delete.html'

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ImageDeleteView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title=f'Видалити зображення до поста "{self.object.post.title}"')
        return {**context, **c_def}

    def get_success_url(self):
        print(self.object.post.image_set.count())
        if self.object.post.image_set.count() > 1:
            return reverse_lazy('image_update', kwargs={'pk': self.object.post.pk})
        else:
            return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})


class TagListView(DataMixin, ListView):
    model = Tag
    paginate_by = 10
    context_object_name = 'tags'
    ordering = ['name']

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='Теги')
        return {**context, **c_def}


class TagDetailView(LoginRequiredMixin, DataMixin, DetailView):
    model = Tag

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='#' + str(context['tag']))
        return {**context, **c_def}
