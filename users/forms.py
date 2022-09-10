from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm

from .models import User, Profile


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
