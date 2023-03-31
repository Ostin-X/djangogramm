# import urllib.request
import urllib
from django.core.files.uploadedfile import SimpleUploadedFile
# from django.http import HttpResponse
import random
import pytz as pytz
from django.core.management.color import no_style
from django.db import connection

from posts.models import Post, Image, Like, Tag, User, Profile
from posts.signals import fake


def create_all_db():
    User.objects.all().delete()

    sequence_sql = connection.ops.sequence_reset_sql(no_style(), [User, Profile, Post, Image, Like, Tag])
    with connection.cursor() as cursor:
        for sql in sequence_sql:
            cursor.execute(sql)

    created_users = create_users_table(3)
    created_posts = create_posts_table(10)
    created_likes = create_likes_table(20)
    created_images = create_images_table(5)
    # created_tags = create_tags_table(100)

    if created_users:
        users_return_text = f' {created_users} users,'
    else:
        users_return_text = ''

    if created_posts:
        posts_return_text = f' {created_posts} posts,'
    else:
        posts_return_text = ''

    if created_likes:
        likes_return_text = f' {created_likes} likes,'
    else:
        likes_return_text = ''

    if created_images:
        images_return_text = f' {created_images} images,'
    else:
        images_return_text = ''

    return f'DB created{users_return_text}{posts_return_text}{likes_return_text}{images_return_text}'[:-1]


def create_users_table(number_of_users):
    # User.objects.all().delete()

    count = User.objects.count()
    decreasing_number = number_of_users

    while decreasing_number > count:
        add_name = fake.name()
        add_email = fake.email()
        add_pass = fake.password()
        user_object = User.objects.create_user(email=add_email, password=add_pass, username=add_name)
        Profile.objects.get(user=user_object).bio = fake.text()
        decreasing_number -= 1

    return number_of_users - count


def create_posts_table(number_of_posts):
    # Post.objects.all().delete()

    users_list = list(User.objects.all())
    count = Post.objects.count()
    decreasing_number = number_of_posts
    tags_list = ['#' + word for word in fake.words(10)]

    while decreasing_number > count:
        add_title = fake.text(random.randint(5, 20))[:-1]
        add_text = ' '.join(random.choices(tags_list, k=random.randint(0, 3))) + ' ' + fake.text()
        add_date = fake.date_time_between(start_date='-5y', end_date='now', tzinfo=pytz.utc)

        Post(title=add_title, text=add_text, user=random.choice(users_list), date=add_date).save()

        decreasing_number -= 1

    return number_of_posts - count


def create_likes_table(number_of_likes):
    # Like.objects.all().delete()

    users_list = list(User.objects.all())
    posts_list = list(Post.objects.all())
    if number_of_likes > len(users_list) * len(posts_list):
        number_of_likes = len(users_list) * len(posts_list)
    count = Like.objects.count()
    decreasing_number = number_of_likes

    while decreasing_number > count:
        post = random.choice(posts_list)
        user = random.choice(users_list)

        add_date = fake.date_time_between(start_date=post.date, end_date='now', tzinfo=pytz.utc)

        if not list(Like.objects.filter(post=post, user=user).all()):
            Like(post=post, user=user, date=add_date).save()
            decreasing_number -= 1

    return number_of_likes - count


# def create_tags_table(number_of_tags):
#     # Tag.objects.all().delete()
#
#     Tag.objects.filter(post=None).delete()
#
#     posts_list = list(Post.objects.all())
#     count = Tag.objects.count()
#     decreasing_number = number_of_tags
#
#     while decreasing_number > count:
#         add_name = fake.word()
#         add_posts_list = random.choices(posts_list, k=random.randint(1, int(len(posts_list) / 2)))
#
#         Tag.objects.create(name=add_name).post_set.set(add_posts_list)
#
#         decreasing_number -= 1
#
#     return number_of_tags - count


def create_images_table(number_of_images):
    posts_list = list(Post.objects.all())
    count = Image.objects.count()
    decreasing_number = number_of_images

    while decreasing_number > count:
        post = random.choice(posts_list)
        user = post.user
        # image_path = 'https://picsum.photos/200/300?random=1'
        # add_image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(),
        #                                content_type='image/jpeg')
        with urllib.request.urlopen("https://picsum.photos/300/200") as url:
            add_image = SimpleUploadedFile(name='test_image.jpg', content=url.read())
        add_date = fake.date_time_between(start_date=post.date, end_date='now', tzinfo=pytz.utc)
        Image(date=add_date, post=post, user=user, image=add_image).save()

        decreasing_number -= 1

    return number_of_images - count
