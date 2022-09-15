# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import ListView, DetailView, CreateView

from .models import Post


# posts = Post.objects.all()
#
#
# def index(request, post_id=None):
#     post_image_list = []
#     posts_query = Post.objects.all()
#     for post in posts_query:
#         post_image_list.append((post, post.image_set.all()))
#     # image_query = image_query[1].image_thumbnail.url
#     # print(post_image_list[0][1][1].image_thumbnail)
#     return render(request, 'post_list.html', {'title': 'Posts', 'posts': post_image_list})
#     # if post_id:
#     #     return HttpResponse(f'Post {post_id} here')
#     # else:
#     #     return HttpResponse('All posts here')


# def users(request):
#     users_list = User.objects.all()
#     return render(request, 'login.html', {'users': users_list, 'title': 'Users'})





# def user_view(request, user_id: int = None, slug: str = None):
#     # if user_id:
#     #     user = get_object_or_404(User, pk=user_id)
#     # else:
#     user = get_object_or_404(User, slug=slug)
#
#     return render(request, 'user.html', {'user': user, 'title': user.name})



# def create_user(request):
#     if request.method == 'POST':
#         form = CreateUserForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('users')
#     else:
#         form = CreateUserForm()
#     return render(request, 'users/user_register.html', {'form': form, 'title': 'Create User'})
