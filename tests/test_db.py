from django.db.models import Q
from django.test import TestCase
import pytest

from posts.views_create_db import create_users_table, create_posts_table, create_likes_table, create_tags_table
from posts.models import Post, Profile, Like, Tag, User


class UsersTestCase(TestCase):
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
        # create_images_table(self.images_number)

    def test_create_objects(self):
        self.assertEqual(User.objects.count(), self.users_number)
        self.assertEqual(User.objects.count(), 5)

        self.assertNotEqual(User.objects.count(), self.users_number + 1)
        self.assertEqual(Profile.objects.count(), self.users_number)
        self.assertEqual(Post.objects.count(), self.posts_number)
        self.assertEqual(Like.objects.count(), self.likes_number)
        self.assertEqual(Tag.objects.count(), self.tags_number)

    def test_delete_user_object(self):
        user_object = User.objects.first()
        posts = user_object.post_set.all()
        post_object = posts.first()
        posts_count = posts.count()
        likes_count = Like.objects.filter(Q(user=user_object) | Q(post__user=user_object)).count()

        Tag.objects.create(name='test tag').post_set.add(post_object)
        tags_count = Tag.objects.count()

        user_object.delete()

        self.assertEqual(User.objects.count(), self.users_number - 1)
        self.assertNotEqual(User.objects.count(), self.users_number)
        self.assertEqual(Profile.objects.count(), self.users_number - 1)
        self.assertNotEqual(Profile.objects.count(), self.users_number)
        self.assertEqual(Post.objects.count(), self.posts_number - posts_count)
        self.assertEqual(Like.objects.count(), self.likes_number - likes_count)
        self.assertLess(Tag.objects.count(), tags_count)
