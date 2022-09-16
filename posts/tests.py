from django.test import TestCase
import pytest
from .views_create_db import create_users_table, create_posts_table, create_likes_table, create_tags_table, \
    create_images_table

from posts.models import Post, Profile, Like, Tag
from django.contrib.auth.models import User


class UsersTestCase(TestCase):
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
        # create_images_table(self.images_number)

    def test_create_user_objects(self):
        assert User.objects.count() == self.users_number

    def test_auto_create_profile_objects(self):
        assert Profile.objects.count() == self.users_number

    def test_create_post_objects(self):
        assert Post.objects.count() == self.posts_number

    def test_create_like_objects(self):
        assert Like.objects.count() == self.likes_number

    def test_create_tag_objects(self):
        assert Tag.objects.count() == self.tags_number

    def test_delete_user_object(self):
        user_object = User.objects.first()
        posts_count = user_object.post_set.count()
        likes_count = user_object.like_set.count()
        for p in Post.objects.filter(user=user_object).all():
            likes_count += p.like_set.exclude(user=user_object).count()
        user_object.delete()
        assert User.objects.count() == self.users_number - 1
        assert Profile.objects.count() == self.users_number - 1
        assert Post.objects.count() == self.posts_number - posts_count
        assert Like.objects.count() == self.likes_number - likes_count

# @pytest.fixture(scope='session')
# def fixture_1():
#     print('run_fixture_1')
#     return 1

# @pytest.mark.django_db
# def test_example_db1():
#     User.objects.create_user('ostin', 'ostin@ostin.gmal.com', 'ostin')
#     assert User.objects.count() == 1
#
#
# @pytest.mark.xfail
# def test_example2(fixture_1):
#     num = fixture_1
#     assert num == 2
#
#
# @pytest.mark.skip
# def test_post_example():
#     print('')
#     print('test1')
#     assert True
