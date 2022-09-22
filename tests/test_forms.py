from django.test import SimpleTestCase

from posts.forms import PostForm


class UsersTestCase(SimpleTestCase):

    def test_post_form_valid(self):
        form = PostForm(data={'title': 'test title', 'text': 'very smart things'})
        form2 = PostForm(data={'title': 'test title2'})
        form3 = PostForm(data={})

        self.assertTrue(form.is_valid())
        self.assertTrue(form2.is_valid())
        self.assertFalse(form3.is_valid())
        self.assertEqual(1, len(form3.errors))
