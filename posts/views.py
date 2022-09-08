from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from extra_views import CreateWithInlinesView, InlineFormSetFactory

from djangogramm.utils import DataMixin

from .models import Post, Image
from .forms import PostForm, ImageForm


class PostListView(ListView):
    model = Post
    paginate_by = 5
    context_object_name = 'posts'
    ordering = ['-date']
    extra_context = {'title': 'Posts'}


class PostDetailView(LoginRequiredMixin, DataMixin, DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    extra_context = {'title': 'Create Post'}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    extra_context = {'title': 'Update Post'}

    def get_queryset(self, *args, **kwargs):
        print(self.kwargs['pk'])
        return super().get_queryset().filter(
            user=self.request.user
        )


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    extra_context = {'title': 'Delete Post'}
    success_url = reverse_lazy('post_list')

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(
            user=self.request.user
        )


class ImageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Image
    form_class = ImageForm
    extra_context = {'title': 'Create Image'}

    def test_func(self):
        return self.request.user.pk == Post.objects.get(pk=self.kwargs['pk']).user_id

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        return super(ImageCreateView, self).form_valid(form)

# class ImageCreateView(InlineFormSetFactory):
#     model = Image
#     fields = '__all__'
#
# class PostCreateView(CreateWithInlinesView):
#     model = Post
#     inlines = [ImageCreateView, ]
#     form_class = PostForm
#     # fields = '__all__'
