from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from djangogramm.utils import DataMixin

from .models import Post, Image, Tag
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
