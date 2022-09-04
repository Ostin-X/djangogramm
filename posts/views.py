from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from extra_views import CreateWithInlinesView, InlineFormSetFactory

from .models import Post, Image
from .forms import PostForm, ImageForm


class PostListView(ListView):
    model = Post
    paginate_by = 5
    context_object_name = 'posts'
    ordering = ['-date']
    extra_context = {'title': 'Posts'}


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        # print(self.request.user.get_absolute_url)
        context = super(PostDetailView, self).get_context_data(**kwargs)
        print(context['post'])
        print(context['post'].image_set.first())
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


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    extra_context = {'title': 'Delete Post'}
    success_url = reverse_lazy('post_list')


class ImageCreateView(LoginRequiredMixin, CreateView):
    model = Image
    form_class = ImageForm
    extra_context = {'title': 'Create Image'}

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(pk=self.request.path.split('/')[-3])
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
