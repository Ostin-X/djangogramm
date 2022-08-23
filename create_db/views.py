from django.shortcuts import render
# from django.utils import timezone
from django.http import HttpResponse
import random
# from lorem_text import lorem
from faker import Faker

from users.models import User
from posts.models import Post, ImageFile, Like
from tags.models import Tag

fake = Faker()


def create_all_db(request):
    created_users = create_users_table(10)
    created_posts = create_posts_table(30)
    created_likes = create_likes_table(1000)
    # created_images = create_images_table()
    created_tags = create_tags_table(100)

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

    # if created_images:
    #     images_return_text = f' {created_images} likes,'
    # else:
    #     images_return_text = ''

    if created_tags:
        tags_return_text = f' {created_tags} tags,'
    else:
        tags_return_text = ''

    return HttpResponse(f'DB created{users_return_text}{posts_return_text}{likes_return_text}{tags_return_text}'[:-1])


def create_users_table(number_of_users):
    User.objects.all().delete()

    count = User.objects.count()
    decreasing_number = number_of_users

    while decreasing_number > count:
        add_email = fake.email()
        add_pass = fake.password()
        add_name = fake.name()

        User(email=add_email, password=add_pass, name=add_name, bio=fake.text()).save()

        decreasing_number -= 1

    return number_of_users - count


def create_posts_table(number_of_posts):
    Post.objects.all().delete()

    users_list = list(User.objects.all())
    count = Post.objects.count()
    decreasing_number = number_of_posts

    while decreasing_number > count:
        # add_title = lorem.words(random.randint(1, 5))
        add_title = fake.text(random.randint(5, 20))[:-1]
        # add_text = lorem.paragraph()
        add_text = fake.text()

        Post(title=add_title, text=add_text, user=random.choice(users_list)).save()

        decreasing_number -= 1

    return number_of_posts - count


def create_likes_table(number_of_likes):
    Like.objects.all().delete()

    users_list = list(User.objects.all())
    posts_list = list(Post.objects.all())
    if number_of_likes > len(users_list) * len(posts_list):
        number_of_likes = len(users_list) * len(posts_list)
    count = Like.objects.count()
    decreasing_number = number_of_likes

    while decreasing_number > count:
        post = random.choice(posts_list)
        user = random.choice(users_list)

        if not list(Like.objects.filter(post=post, user=user).all()):
            Like(post=post, user=user).save()
            decreasing_number -= 1
    # for post in posts_list:
    # print(post.date)
    # print('_______________')
    # print(timezone.now())

    return number_of_likes - count


def create_tags_table(number_of_tags):
    Tag.objects.all().delete()

    posts_list = list(Post.objects.all())
    print(*Post.objects.all())
    count = len(posts_list)
    decreasing_number = number_of_tags

    while decreasing_number > count:
        add_name = fake.word()

        tag = Tag(name=add_name)
        tag.save()
        tag.post_set.set(random.choices(posts_list, k=random.randint(0, int(len(posts_list) / 2))))

        decreasing_number -= 1

    return number_of_tags - count
