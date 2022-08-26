from django.shortcuts import render
from django.http import HttpResponse

from .models import Post

posts = Post.objects.all()

def index(request, post_id=None):
    return render(request, 'posts.html', {'title': 'Posts', 'posts': posts})
    # if post_id:
    #     return HttpResponse(f'Post {post_id} here')
    # else:
    #     return HttpResponse('All posts here')
