from django.shortcuts import render

from templates.settings import menu
from .models import Tag

tags = Tag.objects.all()

def index(request, post_id=None):
    return render(request, 'tags.html', {'menu': menu, 'tags': tags})
