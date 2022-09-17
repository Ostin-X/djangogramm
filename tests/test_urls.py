from django.test import SimpleTestCase
from django.urls import reverse, resolve

from posts.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, ImageCreateView, \
    TagListView, TagDetailView, ImageUpdateView, ImageDeleteView, UserListView, UserDetailView, UserUpdateView, \
    ProfileUpdateView, UserRegisterView, UserDeleteView, PasswordChangeCustomView, PasswordChangeSuccess, \
    LoginCustomView, like_post, image_make_first


class TestUrls(SimpleTestCase):

    def test_post_list_url(self):
        url = reverse('post_list')
        self.assertEqual(resolve(url).func.__name__, PostListView.as_view().__name__)
        self.assertEqual(resolve(url).route, 'posts/')

    def test_post_detail_url(self):
        url = reverse('post_detail', args=['1'])
        self.assertEqual(resolve(url).func.view_class, PostDetailView)
        self.assertEqual('posts/<int:pk>/', resolve(url).route)

    def test_post_create_url(self):
        url = reverse('post_create')
        self.assertEqual(resolve(url).func.view_class, PostCreateView)
        self.assertEqual('posts/create_post/', resolve(url).route)

    def test_post_update_url(self):
        url = reverse('post_update', args=['1'])
        self.assertEqual(resolve(url).func.view_class, PostUpdateView)
        self.assertEqual('posts/<int:pk>/update/', resolve(url).route)

    def test_post_delete_url(self):
        url = reverse('post_delete', args=['1'])
        self.assertEqual(resolve(url).func.view_class, PostDeleteView)
        self.assertEqual('posts/<int:pk>/delete/', resolve(url).route)

    def test_post_like_url(self):
        url = reverse('post_like', args=['1'])
        self.assertEqual(resolve(url).func, like_post)
        self.assertEqual('posts/<int:pk>/like/', resolve(url).route)

    def test_image_create_url(self):
        url = reverse('image_create', args=['1'])
        self.assertEqual(resolve(url).func.view_class, ImageCreateView)
        self.assertEqual('posts/<int:pk>/create_image/', resolve(url).route)

    def test_image_update_url(self):
        url = reverse('image_update', args=['1'])
        self.assertEqual(resolve(url).func.view_class, ImageUpdateView)
        self.assertEqual('posts/<int:pk>/images/', resolve(url).route)

    def test_image_make_first_url(self):
        url = reverse('image_make_first', args=['1', '1'])
        self.assertEqual(resolve(url).func, image_make_first)
        self.assertEqual('posts/<int:post_pk>/images/<int:pk>/first/', resolve(url).route)

    def test_image_delete_url(self):
        url = reverse('image_delete', args=['1', '1'])
        self.assertEqual(resolve(url).func.view_class, ImageDeleteView)
        self.assertEqual('posts/<int:post_pk>/images/<int:pk>/delete/', resolve(url).route)

    def test_tag_list_url(self):
        url = reverse('tag_list')
        self.assertEqual(resolve(url).func.view_class, TagListView)
        self.assertEqual('posts/tags/', resolve(url).route)

    def test_tag_detail_url(self):
        url = reverse('tag_detail', args=['1'])
        self.assertEqual(resolve(url).func.view_class, TagDetailView)
        self.assertEqual('posts/tags/<int:pk>/', resolve(url).route)

    def test_user_list_url(self):
        url = reverse('user_list')
        self.assertEqual(resolve(url).func.__name__, UserListView.as_view().__name__)
        self.assertEqual(resolve(url).func.view_class, UserListView)
        self.assertEqual(resolve(url).route, 'users/')

    def test_user_detail_url(self):
        url = reverse('user_detail', args=['1'])
        self.assertEqual(resolve(url).func.view_class, UserDetailView)
        self.assertEqual('users/<int:pk>/', resolve(url).route)

    def test_user_update_url(self):
        url = reverse('user_update', args=['1'])
        self.assertEqual(resolve(url).func.view_class, UserUpdateView)
        self.assertEqual('users/<int:pk>/update_user/', resolve(url).route)

    def test_user_password_url(self):
        url = reverse('user_password', args=['1'])
        self.assertEqual(resolve(url).func.view_class, PasswordChangeCustomView)
        self.assertEqual('users/<int:pk>/password/', resolve(url).route)

    def test_passsword_success_url(self):
        url = reverse('password_success', args=['1'])
        self.assertEqual(resolve(url).func.view_class, PasswordChangeSuccess)
        self.assertEqual('users/<int:pk>/password_success/', resolve(url).route)

    def test_profile_update_url(self):
        url = reverse('profile_update', args=['1'])
        self.assertEqual(resolve(url).func.view_class, ProfileUpdateView)
        self.assertEqual('users/<int:pk>/update_profile/', resolve(url).route)

    def test_user_delete_url(self):
        url = reverse('user_delete', args=['1'])
        self.assertEqual(resolve(url).func.view_class, UserDeleteView)
        self.assertEqual('users/<int:pk>/delete/', resolve(url).route)

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginCustomView)
        self.assertEqual('users/login/', resolve(url).route)

    def test_register_url(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func.view_class, UserRegisterView)
        self.assertEqual('users/register/', resolve(url).route)
