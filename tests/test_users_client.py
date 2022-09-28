from django.contrib import auth
from django.contrib.auth.models import AnonymousUser
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
        self.user_ostin.profile.bio = 'Тестова БІО'
        self.user_ostin.profile.save()
        self.post_ostin = Post.objects.create(title='Мій тестовий тайтл', user=self.user_ostin,
                                              text='Дуже багато тексту ' + '1234567890' * 10)
        self.image_path = 'Lewis_Hamilton_2016_Malaysia_2.jpg'
        self.add_image = SimpleUploadedFile(name='test_image.jpg', content=open(self.image_path, 'rb').read(),
                                            content_type='image/jpeg')
        Image.objects.create(post=self.post_ostin, user=self.user_ostin, image=self.add_image)

        self.client = Client()

    def test_user_list_GET(self):
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual((response.context_data['object_list']), (User.objects.order_by('-pk').all()))
        self.assertTemplateUsed(response, 'auth/user_list.html')
        self.assertTemplateNotUsed(response, 'posts/user_detail.html')
        self.assertContains(response, 'ostin')
        self.assertContains(response, 'Тестова БІО')

    def test_user_detail_GET_loggedin(self):
        self.client.force_login(self.user_ostin)

        response = self.client.get(reverse('user_detail', kwargs={'pk': self.user_ostin.pk}))

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.context_data['object'], self.user_ostin)
        self.assertTemplateUsed(response, 'auth/user_detail.html')
        self.assertContains(response, 'Edit User')
        self.assertContains(response, 'Delete')

    def test_user_login_POST(self):
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

        response = self.client.post(reverse('login'), data={'username': 'ostin', 'password': 'qwe'})

        self.assertEqual(302, response.status_code)

        user2 = auth.get_user(self.client)

        self.assertTrue(user2.is_authenticated)
        self.assertEqual(user2, self.user_ostin)
        self.assertEqual(response.url, reverse('user_list'))

    def test_user_register_POST(self):
        user_query_count = User.objects.count()
        profile_query_count = Profile.objects.count()
        response = self.client.post(reverse('register'), {'username': 'NewUser', 'email': 'test@test.gmail.com',
                                                          'password1': 'poiqwe123908123',
                                                          'password2': 'poiqwe123908123'})

        self.assertEqual(302, response.status_code)
        self.assertEqual(user_query_count + 1, User.objects.count())
        self.assertEqual(profile_query_count + 1, Profile.objects.count())
        self.assertEqual(User.objects.get(username='NewUser'), User.objects.last())
        self.assertEqual(Profile.objects.last().user, User.objects.get(username='NewUser'))
        self.assertTrue(User.objects.get(username='NewUser').profile)
        self.assertIn(User.objects.get(username='NewUser'), User.objects.all())

        user = auth.get_user(self.client)

        self.assertTrue(user.is_authenticated)
        self.assertEqual(user, User.objects.get(username='NewUser'))
        self.assertEqual(response.url, reverse('user_detail', kwargs={'pk': User.objects.get(username="NewUser").pk}))

    def test_user_update_POST(self):
        self.client.force_login(self.user_ostin)
        user_query_count = User.objects.count()
        profile_query_count = Profile.objects.count()

        self.assertIn('ostin', str(User.objects.values_list('username')))
        self.assertEqual('ostin', User.objects.get(pk=self.user_ostin.pk).username)
        self.assertFalse(User.objects.filter(username='ostinNEW').exists())

        response = self.client.post(
            reverse('user_update', kwargs={'pk': self.user_ostin.pk}), {'username': 'ostinNEW'})

        self.user_ostin.refresh_from_db()

        self.assertEqual(302, response.status_code)
        self.assertIn(User.objects.get(username='ostinNEW'), User.objects.all())
        self.assertFalse(User.objects.filter(username='ostin').exists())
        self.assertEqual('ostinNEW', self.user_ostin.username)
        self.assertEqual(user_query_count, User.objects.count())
        self.assertEqual(profile_query_count, Profile.objects.count())
        self.assertEqual(response.url, reverse('user_detail', kwargs={'pk': self.user_ostin.pk}))

    def test_user_password_update_POST(self):
        old_password = 'qwe'
        old_password_encrypted = self.user_ostin.password
        new_password = 'bjkndfsbkndfbklj09468234jnbdkf'
        login = self.client.login(username='ostin', password=old_password)

        self.assertTrue(login)
        self.assertTrue(self.user_ostin.password)

        user = auth.get_user(self.client)
        self.assertTrue(old_password_encrypted, user.password)

        user_query_count = User.objects.count()
        profile_query_count = Profile.objects.count()

        self.assertNotEqual(old_password, self.user_ostin.password)
        self.assertNotEqual(new_password, self.user_ostin.password)

        response = self.client.post(
            reverse('user_password', kwargs={'pk': self.user_ostin.pk}),
            {'old_password': old_password, 'new_password1': new_password, 'new_password2': new_password})

        self.user_ostin.refresh_from_db()

        self.assertEqual(302, response.status_code)
        self.assertNotEqual(old_password, self.user_ostin.password)
        self.assertNotEqual(new_password, self.user_ostin.password)
        self.assertNotEqual(old_password_encrypted, self.user_ostin.password)
        self.assertEqual(user_query_count, User.objects.count())
        self.assertEqual(profile_query_count, Profile.objects.count())
        self.assertEqual(response.url, reverse('password_success', kwargs={'pk': self.user_ostin.pk}))

        self.client.logout()
        user2 = auth.get_user(self.client)
        self.assertFalse(user2.is_authenticated)

        login2 = self.client.login(username='ostin', password=new_password)
        self.assertTrue(login2)
        user3 = auth.get_user(self.client)
        self.assertTrue(user3.is_authenticated)
        self.assertEqual(user3, self.user_ostin)

    def test_profile_update_POST(self):
        self.client.force_login(self.user_ostin)
        user_query_count = User.objects.count()
        profile_query_count = Profile.objects.count()

        self.assertIn(self.user_ostin, User.objects.all())
        self.assertEqual('Тестова БІО', self.user_ostin.profile.bio)
        self.assertTrue(self.user_ostin.profile.bio)
        self.assertFalse(Profile.objects.filter(bio='Нова БбІо').exists())
        self.assertFalse(self.user_ostin.profile.avatar)
        self.assertFalse(self.user_ostin.profile.avatar_thumbnail)

        with open(self.image_path, 'rb') as fp:
            response = self.client.post(reverse('profile_update', kwargs={'pk': self.user_ostin.pk}),
                                        {'bio': 'Нова БбІо', 'avatar': fp})

        self.user_ostin.refresh_from_db()

        self.assertEqual(302, response.status_code)
        self.assertEqual('Нова БбІо', User.objects.get(pk=self.user_ostin.pk).profile.bio)
        self.assertEqual('Нова БбІо', self.user_ostin.profile.bio)
        self.assertEqual(Profile.objects.get(bio='Нова БбІо').user, self.user_ostin)
        self.assertFalse(Profile.objects.filter(bio='Тестова БІО').exists())
        self.assertEqual(user_query_count, User.objects.count())
        self.assertEqual(profile_query_count, Profile.objects.count())
        self.assertEqual(response.url, reverse('user_detail', kwargs={'pk': self.user_ostin.pk}))

        self.assertTrue(self.user_ostin.profile.avatar)
        self.assertEqual('avatars/avatars_6.jpg', self.user_ostin.profile.avatar)
        self.assertTrue(self.user_ostin.profile.avatar_thumbnail)
        self.assertEqual('avatars/avatars_6_thumbnail.jpg', self.user_ostin.profile.avatar_thumbnail)

        response2 = self.client.post(reverse('profile_update', kwargs={'pk': self.user_ostin.pk}),
                                     {'avatar-clear': True})

        self.user_ostin.refresh_from_db()

        self.assertEqual(302, response2.status_code)
        self.assertEqual(user_query_count, User.objects.count())
        self.assertEqual(profile_query_count, Profile.objects.count())
        self.assertFalse(self.user_ostin.profile.avatar)
        self.assertFalse(self.user_ostin.profile.avatar_thumbnail)

    def test_user_delete_DELETE(self):
        self.client.force_login(self.user_ostin)
        user_query_count = User.objects.count()
        profile_query_count = Profile.objects.count()
        user_to_be_deleted = self.user_ostin
        profile_to_be_deleted = self.user_ostin.profile

        self.assertIn(user_to_be_deleted, User.objects.all())
        self.assertIn(profile_to_be_deleted, Profile.objects.all())

        response = self.client.delete(reverse('user_delete', kwargs={'pk': user_to_be_deleted.pk}))

        self.assertEqual(302, response.status_code)
        self.assertNotIn(user_to_be_deleted, User.objects.all())
        self.assertNotIn(profile_to_be_deleted, Profile.objects.all())
        self.assertEqual(user_query_count - 1, User.objects.count())
        self.assertEqual(profile_query_count - 1, Profile.objects.count())

        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated)
        self.assertEqual(response.url, reverse('user_list'))

    def test_user_detail_GET_other_loggedin(self):
        self.client.force_login(self.user_ostin)
        response = self.client.get(reverse('user_detail', kwargs={'pk': User.objects.first().pk}))

        self.assertEqual(200, response.status_code)
        self.assertNotEqual(response.context_data['object'], self.post_ostin)
        self.assertTemplateUsed(response, 'auth/user_detail.html')
        self.assertNotContains(response, 'Edit User')

    def test_user_detail_GET_loggedout(self):
        user_object = User.objects.first()
        response = self.client.get(reverse('user_detail', kwargs={'pk': user_object.pk}))

        self.assertEqual(302, response.status_code)
        self.assertEqual(response.headers['Location'], f'/users/login/?next=/users/{user_object.pk}/')
        self.assertTemplateNotUsed(response, 'auth/user_detail.html')
