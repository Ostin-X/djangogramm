from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
# from .models import Profile


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 60, 'rows': 3}),
    #                       label='Біографія')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


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
