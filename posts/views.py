from django.shortcuts import render
from django.http import HttpResponse

from .models import Post

posts = Post.objects.all()


def index(request, post_id=None):
    post_image_list = []
    posts_query = Post.objects.all()
    for post in posts_query:
        post_image_list.append((post, post.image_set.all()))
    # image_query = image_query[1].image_thumbnail.url
    # print(post_image_list[0][1][1].image_thumbnail)
    return render(request, 'posts.html', {'title': 'Posts', 'posts': post_image_list})
    # if post_id:
    #     return HttpResponse(f'Post {post_id} here')
    # else:
    #     return HttpResponse('All posts here')
