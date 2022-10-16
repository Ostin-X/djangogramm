import json

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import PasswordChangeView, TemplateView, LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Count

from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
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
    context_object_name = 'profile'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['profile'],
                                      sub_exists=self.request.user.profile.sub_exists(self.object.profile))
        return {**context, **c_def}

    def post(self, request, *args, **kwargs):
        profile_followed_object = self.get_object().profile
        profile_follower_object = request.user.profile
        if profile_follower_object.sub_exists(profile_followed_object):
            profile_follower_object.following.remove(profile_followed_object)
        else:
            profile_follower_object.following.add(profile_followed_object)
        return self.get(request, *args, **kwargs)


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        import six
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


class UserRegisterView(NotLoggedAllow, DataMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='Створити користувача')
        return {**context, **c_def}

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        mail_subject = 'Activation link has been sent to your email id'
        message = render_to_string('registration/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('Please confirm your email address to complete the registration')


class UserActivationView(DataMixin, TemplateView):
    template_name = 'registration/auth_token.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserActivationView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title=f"Email confirmation")
        return {**context, **c_def}

    def get(self, request, uidb64, token, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            context['message'] = 'Thank you for your email confirmation. Now you can login your account.'
            return self.render_to_response(context)
        else:
            context['message'] = 'Activation link is invalid!'
            return self.render_to_response(context)


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


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class PostDetailView(LoginRequiredMixin, DataMixin, DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'].title,
                                      like_exists=self.object.like_exists(self.request.user))
        return {**context, **c_def}

    def post(self, request, *args, **kwargs):
        post_object = self.get_object()
        user_object = request.user
        if request.POST.get("operation") == "like_submit" and is_ajax(request):
            post_id = request.POST.get("post_id", None)
            post = get_object_or_404(Post, pk=post_id)
            print(post)
            try:
                Like.objects.get(user=user_object, post=post).delete()
                liked = False
            except Like.DoesNotExist:
                Like.objects.create(user=user_object, post=post_object)
                liked = True
            ctx = {"liked": liked, "post_id": post_id}
            return HttpResponse(json.dumps(ctx), content_type='application/json')

        # if 'post_pk' in request.POST:
        #     try:
        #         Like.objects.get(user=user_object, post=post_object).delete()
        #     except Like.DoesNotExist:
        #         Like.objects.create(user=user_object, post=post_object)
        return self.get(request, *args, **kwargs)


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
        c_def = self.get_user_context(
            title=f"Редагувати зображення поста {Post.objects.get(pk=self.kwargs['pk']).title}", object=post_object)
        return {**context, **c_def}

    def post(self, request, *args, **kwargs):
        post_object = get_object_or_404(Post, id=kwargs['pk'])
        image_object = get_object_or_404(Image, id=request.POST['image_pk'])
        post_object.make_first(image_object)
        return self.get(request, *args, **kwargs)


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


class SubListView(DataMixin, DetailView):
    model = Profile
    paginate_by = 10
    context_object_name = 'subs'
    template_name = 'posts/sub_list.html'

    def get_context_data(self, **kwargs):
        context = super(SubListView, self).get_context_data(**kwargs)
        context['subs'] = self.object.followers.annotate(post_count=Count('user__post')).order_by('-post_count')
        c_def = self.get_user_context(title='Підписки')
        return {**context, **c_def}

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(user=self.request.user)
