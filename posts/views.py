from django.shortcuts import render
from django.http import HttpResponse

from templates.settings import menu
from .models import Post

posts = Post.objects.all()

def index(request, post_id=None):
    return render(request, 'posts.html', {'menu': menu, 'posts': posts})
    # if post_id:
    #     return HttpResponse(f'Post {post_id} here')
    # else:
    #     return HttpResponse('All posts here')
