from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, override_settings
import tempfile
from django.urls import reverse

import pytest

from posts.views_create_db import create_users_table, create_posts_table, create_likes_table, create_tags_table, \
    create_images_table
from posts.models import Post, Profile, Like, Tag, User, Image


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class PostViewsTestCase(TestCase):
    def setUp(self):
        self.users_number = 5
        self.posts_number = 8
        self.likes_number = 20
        self.tags_number = 20
        self.images_number = 10

        create_users_table(self.users_number)
        create_posts_table(self.posts_number)
        create_likes_table(self.likes_number)
        create_tags_table(self.tags_number)
        create_images_table(self.images_number)

        # self.user_ostin = User.objects.create(email='and@and.gmail.com', password='qwe', username='ostin')
        # self.user_ostin.set_password('qwe')
        self.user_ostin = User.objects.create_user(email='and@and.gmail.com', password='qwe', username='ostin')

        self.post_ostin = Post.objects.create(title='Мій тестовий тайтл',
                                              text='Дуже багато тексту ' + '1234567890' * 10,
                                              user=self.user_ostin)
        self.image_path = 'Lewis_Hamilton_2016_Malaysia_2.jpg'
        self.add_image = SimpleUploadedFile(name='test_image.jpg', content=open(self.image_path, 'rb').read(),
                                            content_type='image/jpeg')
        Image.objects.create(post=self.post_ostin, user=self.user_ostin, image=self.add_image)

        self.client = Client()

    def test_post_list_GET(self):
        response = self.client.get(reverse('post_list'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual((response.context_data['object_list']), (Post.objects.order_by('-date').all()))
        self.assertTemplateUsed(response, 'posts/post_list.html')
        self.assertTemplateNotUsed(response, 'posts/post_detail.html')
        self.assertContains(response, 'Мій тестовий тайтл')
        self.assertContains(response, 'Дуже багато тексту ' + '1234567890' * 8 + '1')

    def test_post_detail_GET_loggedin(self):
        # self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        self.client.force_login(self.user_ostin)
        # login = self.client.login(username='ostin', password='qwe')
        # assert login == True
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post_ostin.pk}))

        # assert response.__dict__ == 'posts/post_list.html2'
        # assert response.context_data['object'] == self.post_ostin.__dict__

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.context_data['object'], self.post_ostin)
        self.assertTemplateUsed(response, 'posts/post_detail.html')
        self.assertContains(response, 'Додати зображення')
        self.assertContains(response, 'Керувати зображеннями')

    def test_post_create_POST(self):
        self.client.force_login(self.user_ostin)
        post_query_count = Post.objects.count()
        response = self.client.post(reverse('post_create'), {'title': 'New title'})

        self.assertEqual(302, response.status_code)
        self.assertEqual(post_query_count + 1, Post.objects.count())
        self.assertEqual(Post.objects.get(title='New title'), Post.objects.last())
        self.assertEqual(Post.objects.get(title='New title').user, self.user_ostin)
        self.assertIn(Post.objects.get(title='New title'), Post.objects.all())

    def test_post_update_POST(self):
        self.client.force_login(self.user_ostin)
        post_query_count = Post.objects.count()
        self.assertIn(Post.objects.get(title='Мій тестовий тайтл'), Post.objects.all())
        self.assertEqual('Мій тестовий тайтл', Post.objects.get(pk=self.post_ostin.pk).title)
        self.assertFalse(Post.objects.filter(title='Новий змінений тайтл').exists())

        response = self.client.post(
            reverse('post_update', kwargs={'pk': self.post_ostin.pk}), {'title': 'Новий змінений тайтл'})

        self.assertEqual(302, response.status_code)
        self.assertIn(Post.objects.get(title='Новий змінений тайтл'), Post.objects.all())
        self.assertFalse(Post.objects.filter(title='Мій тестовий тайтл').exists())
        self.assertEqual('Новий змінений тайтл', Post.objects.get(pk=self.post_ostin.pk).title)
        self.assertEqual(post_query_count, Post.objects.count())

    def test_post_delete_DELETE(self):
        self.client.force_login(self.user_ostin)
        post_query_count = Post.objects.count()
        post_to_be_deleted = Post.objects.get(title='Мій тестовий тайтл')

        self.assertIn(post_to_be_deleted, Post.objects.all())

        response = self.client.delete(reverse('post_delete', kwargs={'pk': post_to_be_deleted.pk}))

        self.assertEqual(302, response.status_code)
        self.assertNotIn(post_to_be_deleted, Post.objects.all())
        self.assertEqual(post_query_count - 1, Post.objects.count())

    def test_post_detail_GET_other_loggedin(self):
        self.client.force_login(self.user_ostin)
        response = self.client.get(reverse('post_detail', kwargs={'pk': Post.objects.first().pk}))

        self.assertEqual(200, response.status_code)
        self.assertNotEqual(response.context_data['object'], self.post_ostin)
        self.assertTemplateUsed(response, 'posts/post_detail.html')
        self.assertNotContains(response, 'Додати зображення')

    def test_post_detail_GET_loggedout(self):
        post_object = Post.objects.first()
        response = self.client.get(reverse('post_detail', kwargs={'pk': post_object.pk}))

        self.assertEqual(302, response.status_code)
        self.assertEqual(response.headers['Location'], f'/users/login/?next=/posts/{post_object.pk}/')
        self.assertTemplateNotUsed(response, 'posts/post_detail.html')

    def test_image_create_POST(self):
        self.client.force_login(self.user_ostin)
        old_image_count = Image.objects.count()

        with open(self.image_path, 'rb') as fp:
            response = self.client.post(reverse('image_create', kwargs={'pk': self.post_ostin.pk}), {'image': fp})

        self.assertEqual(302, response.status_code)
        self.assertEqual(old_image_count + 1, Image.objects.count())
        self.assertEqual(2, self.post_ostin.image_set.count())
        self.assertEqual(2, self.user_ostin.image_set.count())
        self.assertEqual(f'images/images_{self.post_ostin.pk}.jpg', self.post_ostin.image_set.first().image)
        self.assertEqual(f'images/images_{self.post_ostin.pk}_thumbnail.jpg',
                         self.post_ostin.image_set.first().image_thumbnail)
        self.assertIn(f'images/images_{self.post_ostin.pk}', str(self.post_ostin.image_set.last().image))
        self.assertIn(f'images/images_{self.post_ostin.pk}', str(self.post_ostin.image_set.last().image_thumbnail))
        self.assertIn('_thumbnail.jpg', str(self.post_ostin.image_set.last().image_thumbnail))

    def test_image_delete_DELETE(self):
        self.client.force_login(self.user_ostin)
        old_image_count = Image.objects.count()

        response = self.client.delete(
            reverse('image_delete', kwargs={'post_pk': self.post_ostin.pk, 'pk': self.post_ostin.image_set.first().pk}))

        self.assertEqual(302, response.status_code)
        self.assertEqual(old_image_count - 1, Image.objects.count())
        self.assertEqual(0, self.post_ostin.image_set.count())
        self.assertEqual(0, self.user_ostin.image_set.count())

    def test_image_make_first_GET(self):
        self.client.force_login(self.user_ostin)

        self.assertIsNone(Post.objects.get(pk=self.post_ostin.pk).first_image)
        response = self.client.get(
            reverse('image_make_first',
                    kwargs={'post_pk': self.post_ostin.pk, 'pk': self.post_ostin.image_set.first().pk}))

        self.assertEqual(302, response.status_code)
        self.assertIsNotNone(Post.objects.get(pk=self.post_ostin.pk).first_image)
        self.assertEqual(self.post_ostin.image_set.first(), Post.objects.get(pk=self.post_ostin.pk).first_image)

        response2 = self.client.get(reverse('post_list'))

        self.assertContains(response2, Post.objects.get(pk=self.post_ostin.pk).first_image.image_thumbnail)

    def test_like_POST(self):
        self.client.force_login(self.user_ostin)

        post_likes_count = self.post_ostin.like_set.count()
        other_post_likes_count = Post.objects.first().like_set.count()
        user_likes_count = self.user_ostin.like_set.count()
        likes_count = Like.objects.count()

        response = self.client.get(reverse('post_like', kwargs={'pk': self.post_ostin.pk}))
        response2 = self.client.get(reverse('post_like', kwargs={'pk': Post.objects.first().pk}))

        self.assertEqual(302, response.status_code)
        self.assertEqual(302, response2.status_code)
        self.assertEqual(post_likes_count + 1, Post.objects.get(pk=self.post_ostin.pk).like_set.count())
        self.assertEqual(other_post_likes_count + 1, Post.objects.first().like_set.count())
        self.assertEqual(user_likes_count + 2, User.objects.get(pk=self.user_ostin.pk).like_set.count())
        self.assertEqual(likes_count + 2, Like.objects.count())

        # response3 = self.client.get(reverse('post_like', kwargs={'pk': self.post_ostin.pk}))
        response4 = self.client.get(reverse('post_like', kwargs={'pk': Post.objects.first().pk}))

        # self.assertEqual(302, response3.status_code)
        self.assertEqual(302, response4.status_code)
        self.assertEqual(post_likes_count + 1, Post.objects.get(pk=self.post_ostin.pk).like_set.count())
        self.assertEqual(other_post_likes_count, Post.objects.first().like_set.count())
        self.assertEqual(user_likes_count + 1, User.objects.get(pk=self.user_ostin.pk).like_set.count())
        self.assertEqual(likes_count + 1, Like.objects.count())
