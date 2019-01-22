
from django.test import TestCase

from blog.forms import PostForm, CommentForm


class TestPostForm(TestCase):

    def test_passing_form(self):
        form_data = {'title': 'r' * 128, 'content': 'r' * 3000}
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_failing_form_content_more_than_3000_characters(self):
        content = 'r' * 3001
        form = PostForm(data={'title': 'Hello There', 'content': content})
        self.assertFalse(form.is_valid())

    def test_failing_form_title_more_than_128_characters(self):
        title = 'r' * 129
        form = PostForm(data={'title': title, 'content': 'Hello there!'})
        self.assertFalse(form.is_valid())

    def test_title_field_has_help_text(self):
        form = PostForm()
        self.assertEqual(form.fields['title'].help_text, 'Enter your post title here.')

    def test_content_field_has_help_text(self):
        form = PostForm()
        self.assertEqual(form.fields['content'].help_text, 'Enter your blog post here.')


class TestCommentForm(TestCase):

    def test_passing_form(self):
        form_data = {'content': 'r' * 512}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_failing_form_content_more_than_512_characters(self):
        content = 'r' * 513
        form = CommentForm(data={'content': content})
        self.assertFalse(form.is_valid())

    def test_content_field_has_help_text(self):
        form = CommentForm()
        self.assertEqual(form.fields['content'].help_text, 'Enter your comment here.')
