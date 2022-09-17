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
        self.assertTemplateUsed(response, 'posts/post_list.html')
        self.assertTemplateNotUsed(response, 'posts/post_list.html2')
        self.assertContains(response, 'Мій тестовий тайтл')
        self.assertContains(response,
                            'Дуже багато тексту 123456789012345678901234567890123456789012345678901234567890123456789012345678901')

    def test_post_detail_GET_loggedin(self):
        # self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        self.client.force_login(self.user_ostin)
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post_ostin.pk}))

        # assert response.__dict__ == 'posts/post_list.html2'

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'posts/post_detail.html')
        self.assertContains(response, 'Додати зображення')

        self.client.logout()

    def test_post_detail_GET_other_loggedin(self):
        self.client.force_login(self.user_ostin)
        response = self.client.get(reverse('post_detail', kwargs={'pk': Post.objects.first().pk}))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'posts/post_detail.html')
        self.assertNotContains(response, 'Додати зображення')

        self.client.logout()

    def test_post_detail_GET_loggedout(self):
        self.client.logout()
        response = self.client.get(reverse('post_detail', kwargs={'pk': Post.objects.first().pk}))

        self.assertEqual(302, response.status_code)
        self.assertTemplateNotUsed(response, 'posts/post_detail.html')

