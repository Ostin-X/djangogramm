import json

from django.test import TestCase, Client

import pytest
from django.urls import reverse

from posts.views_create_db import create_users_table, create_posts_table, create_likes_table, create_tags_table

from posts.models import Post, Profile, Like, Tag, User


class PostViewsTestCase(TestCase):
    def setUp(self):
        self.users_number = 5
        self.posts_number = 8
        self.likes_number = 20
        self.tags_number = 20
        # self.images_number = 10

        create_users_table(self.users_number)
        create_posts_table(self.posts_number)
        create_likes_table(self.likes_number)
        create_tags_table(self.tags_number)
        self.user_ostin = User.objects.create(email='and@and.gmail.com', password='qwe', username='ostin')
        self.post_ostin = Post.objects.create(title='Мій тестовий тайтл',
                                              text='Дуже багато тексту ' + '1234567890' * 10,
                                              user=self.user_ostin)

        self.client = Client()

        # self.list_url = reverse('post_list')
        # self.detail_login_url = reverse('post_detail', kwargs={'pk': self.post_ostin.pk})
        # self.detail_url = reverse('post_detail', kwargs={'pk': self.post_ostin.pk})

    def test_post_list_GET(self):
        response = self.client.get(reverse('post_list'))

        # assert response.__dict__ == 'posts/post_list.html2'

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual((response.context_data['object_list']), (Post.objects.order_by('-date').all()))
        self.assertTemplateUsed(response, 'posts/post_list.html')
        self.assertTemplateNotUsed(response, 'posts/post_detail.html')
        self.assertContains(response, 'Мій тестовий тайтл')
        self.assertContains(response,
                            'Дуже багато тексту ' + '1234567890' * 8 + '1')

    def test_post_detail_GET_loggedin(self):
        # self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        self.client.force_login(self.user_ostin)
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post_ostin.pk}))

        # assert response.__dict__ == 'posts/post_list.html2'
        # assert response.context_data['object'] == self.post_ostin.__dict__

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.context_data['object'], self.post_ostin)
        self.assertTemplateUsed(response, 'posts/post_detail.html')
        self.assertContains(response, 'Додати зображення')

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
