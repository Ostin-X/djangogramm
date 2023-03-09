import os
from django import forms
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from six import BytesIO
from PIL import Image as PilImage

from .models import Post, Image, User, Profile


def resize_uploaded_image(image, max_width=100, max_height=50):
    size = (max_width, max_height)

    # Uploaded file is in memory
    if isinstance(image, InMemoryUploadedFile):
        # memory_image = BytesIO(image.read())
        pil_image = PilImage.open(image)
        img_format = os.path.splitext(image.name)[1][1:].upper()
        img_format = 'JPEG' if img_format == 'JPG' else img_format

        if pil_image.width > max_width or pil_image.height > max_height:
            pil_image.thumbnail(size)

        new_image = BytesIO()
        pil_image.save(new_image, format=img_format)

        new_image = ContentFile(new_image.getvalue())
        return InMemoryUploadedFile(new_image, None, image.name, image.content_type, None, None)


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

    def save(self, commit=True):
        obj = super().save()
        from django.utils.datastructures import MultiValueDictKeyError
        try:
            obj.avatar_thumbnail = resize_uploaded_image(self.files['avatar'])
            obj.save(update_fields=["avatar_thumbnail"])
        except MultiValueDictKeyError as e:
            if e.args[0] == 'avatar':
                if not obj.avatar:
                    obj.avatar_thumbnail = ''
                    obj.save(update_fields=["avatar_thumbnail"])
            else:
                raise e

        # if 'avatar' in self.files:
        #     image_uploaded = self.files['avatar']
        #     obj.avatar_thumbnail = resize_uploaded_image(image_uploaded)
        #     obj.save(update_fields=["avatar_thumbnail"])
        # elif not obj.avatar:
        #     obj.avatar_thumbnail = ''
        #     obj.save(update_fields=["avatar_thumbnail"])
        return obj


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

        labels = {
            'image': 'Картинка'
        }

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.save()
        if 'image' in self.files:
            image_uploaded = self.files['image']
            obj.image_thumbnail = resize_uploaded_image(image_uploaded)
            obj.save(update_fields=["image_thumbnail"])
        elif not obj.image and obj.image_thumbnail:
            obj.image_thumbnail = ''
            obj.save(update_fields=["image_thumbnail"])
        return obj


ImageFormSet = inlineformset_factory(Post, Image, form=ImageForm, extra=2)
