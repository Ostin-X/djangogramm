from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from extra_views import CreateWithInlinesView, InlineFormSetFactory

from .models import Post, Image
from .forms import PostForm, ImageForm


class PostListView(ListView):
    model = Post
    paginate_by = 5
    context_object_name = 'posts'
    extra_context = {'title': 'Posts'}


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['title'] = context['post']
        return context


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


class ImageCreateView(LoginRequiredMixin, CreateView):
    model = Image
    form_class = ImageForm
    # fields = '__all__'
    extra_context = {'title': 'Create Image'}

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(pk=self.request.path.split('/')[2])
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
