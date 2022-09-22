from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Q
from django.test import TestCase, override_settings
import tempfile

from posts.views_create_db import create_users_table, create_posts_table, create_likes_table, create_tags_table, \
    create_images_table
from posts.models import Post, Profile, Like, Tag, User, Image


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
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
        create_images_table(self.images_number)

    def test_create_objects(self):
        self.assertEqual(Profile.objects.count(), self.users_number)

        self.assertFalse(Image.objects.filter(Q(image_thumbnail='') | Q(image_thumbnail=None)).all())
        self.assertIn(f'images_{Image.objects.first().post.pk}', str(Image.objects.first().image))
        self.assertIn(f'images_{Image.objects.first().post.pk}_thumbnail', str(Image.objects.first().image_thumbnail))

    def test_delete_user_object(self):
        user_object = User.objects.first()
        post_object = Post.objects.create(title='Test post title', user=user_object)

        self.assertEqual(0, post_object.image_set.count())

        image_path = 'Lewis_Hamilton_2016_Malaysia_2.jpg'
        add_image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(),
                                       content_type='image/jpeg')
        Image.objects.create(post=post_object, user=user_object, image=add_image)

        self.assertEqual(1, post_object.image_set.count())

        images_count = user_object.image_set.count()
        posts_count = user_object.post_set.count()
        likes_count = Like.objects.filter(Q(user=user_object) | Q(post__user=user_object)).count()

        Tag.objects.create(name='test tag').post_set.add(post_object)
        tags_count = Tag.objects.count()

        user_object.delete()

        self.assertEqual(User.objects.count(), self.users_number - 1)
        self.assertNotEqual(User.objects.count(), self.users_number)
        self.assertEqual(Profile.objects.count(), self.users_number - 1)
        self.assertNotEqual(Profile.objects.count(), self.users_number)
        self.assertEqual(Post.objects.count(), self.posts_number + 1 - posts_count)
        self.assertEqual(Like.objects.count(), self.likes_number - likes_count)
        self.assertLess(Tag.objects.count(), tags_count)
        self.assertEqual(Image.objects.count(), self.images_number + 1 - images_count)

    def test_delete_post_object(self):
        post_object = Post.objects.first()
        posts_count = Post.objects.count()
        post_user_object = post_object.user
        user_posts_count = post_object.user.post_set.count()
        post_likes_count = post_object.like_set.count()
        likes_count = Like.objects.count()

        Tag.objects.create(name='test tag').post_set.add(post_object)
        tags_count = Tag.objects.count()

        post_object.delete()

        self.assertNotIn(post_object, Post.objects.all())
        self.assertEqual(posts_count - 1, Post.objects.count())
        self.assertNotEqual(Post.objects.count(), posts_count)
        self.assertFalse(Post.objects.filter(pk=post_object.pk).exists())
        self.assertEqual(user_posts_count - 1, post_user_object.post_set.count())
        self.assertEqual(likes_count - post_likes_count, Like.objects.count())
        self.assertLess(Tag.objects.count(), tags_count)
