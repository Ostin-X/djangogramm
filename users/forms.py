from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth.models import User


# from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class ProfileForm(UserChangeForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 60, 'rows': 3}),
                          label='Про себе')
    avatar = forms.ImageField(label='Аватарка')
    is_invisible = forms.BooleanField(required=False, label="Сором'змива дупа")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть заголовок'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),

        }

# class CreateUserForm(forms.Form):
#     email = forms.EmailField(max_length=100)
#     password = forms.CharField(widget=forms.PasswordInput(), max_length=100, label='Пароль')
#     name = forms.CharField(max_length=100, label="Ім'я")
#     # slug = forms.SlugField(max_length=100)
#     bio = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Біографія')
#     # avatar = forms.ImageField(label='Аватарка')
#     # is_invisible = forms.BooleanField(label="Сором'язливість", required=False)
#     # cat = forms.ModelChoiceField(queryset=['cool', 'not cool'], empty_label='ijnjn')


# class CreateUserForm(forms.ModelForm):
#     # def __init__(self, *args, **kwargs):
#     #     super().__init__(*args, **kwargs)
#     # self.fields['cat'].empty_label = 'Категорія не вибрана'
#     class Meta:
#         model = Profile
#         # fields = '__all__'
#         fields = ['name', 'email', 'password', 'bio', 'avatar', 'is_invisible']
#         # widgets = {}
