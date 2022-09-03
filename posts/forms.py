from django import forms
from .models import Post, Image


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть заголовок'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            "title": "Заголовок",
            "text": "Текст",
            'user': 'Користувач',
        }


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']

        widgets = {
            # 'image': forms.ImageField,
            # 'post': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'image': 'Картинка'
        }