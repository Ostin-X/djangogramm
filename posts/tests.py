from django.test import TestCase
import pytest
from create_db.views import fake

from posts.models import Post
from users.models import Profile
from django.contrib.auth.models import User


class UsersTestCase(TestCase):
    def setUp(self):
        for i in range(5):
            User.objects.create(username=fake.name(), email=fake.email(), password=fake.password())

    def test_create_user_objects(self):
        assert User.objects.count() == 5

    def test_auto_create_profile_objects(self):
        assert Profile.objects.count() == 5


@pytest.fixture(scope='session')
def fixture_1():
    print('run_fixture_1')
    return 1


@pytest.mark.django_db
def test_example_db1():
    User.objects.create_user('ostin', 'ostin@ostin.gmal.com', 'ostin')
    assert User.objects.count() == 1


@pytest.mark.xfail
def test_example2(fixture_1):
    num = fixture_1
    assert num == 2


@pytest.mark.skip
def test_post_example():
    print('')
    print('test1')
    assert True
