from django.shortcuts import render
from django.http import HttpResponse


def index(request, post_id=None):
    if post_id:
        return HttpResponse(f'Post {post_id} here')
    else:
        return HttpResponse('All posts here')
