# from django.test import TestCase
# import pytest
#
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
