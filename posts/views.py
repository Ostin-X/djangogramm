from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from djangogramm.utils import DataMixin

from .models import Post, Image
from .forms import PostForm, ImageForm


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


class PostDetailView(LoginRequiredMixin, DataMixin, DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
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


class PostUpdateView(LoginRequiredMixin, DataMixin, UpdateView):
    model = Post
    form_class = PostForm
    second_form_class = ImageForm

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
