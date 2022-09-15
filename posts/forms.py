from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm

from .models import Post, Image, User, Profile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        # self.fields['username'].widget.attrs['class'] = 'form-control'
        # self.fields['password1'].widget.attrs['class'] = 'form-control'
        # self.fields['password2'].widget.attrs['class'] = 'form-control'


class UserForm(UserChangeForm):
    class Meta:
        model = User
        password = None
        fields = ('username', 'email')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'avatar', 'is_invisible')

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'cols': 60, 'rows': 3}),
            # 'avatar': forms.FileInput(),
            'is_invisible': forms.CheckboxInput(attrs={'class': 'form-check'}),
        }


class PasswordChangeCustomForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PasswordChangeCustomForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['type'] = 'password'
            field.help_text = None


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

        # widgets = {
        #     'image': forms.ImageField,
        #     'post': forms.Select(attrs={'class': 'form-control'}),
        # }
        labels = {
            'image': 'Картинка'
        }
