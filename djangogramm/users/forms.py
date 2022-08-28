from django import forms
from .models import User


class CreateUserForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=100, label='Пароль')
    name = forms.CharField(max_length=100, label="Ім'я")
    # slug = forms.SlugField(max_length=100)
    bio = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Біографія')
    avatar = forms.ImageField(label='Аватарка')
    is_invisible = forms.BooleanField(label="Сором'язливість", required=False)
    # cat = forms.ModelChoiceField(queryset=['cool', 'not cool'], empty_label='ijnjn')