from django.test import TestCase

from users.models import CustomUser
from blog.models import Author, Post


class TestHomePage(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create(username='eljefe', password='Passw3rd!')
        author = Author.objects.create(author=user, bio='Hello there!')

        for _ in range(5):
            Post.objects.create(author=author, title='c' * 125, content='x' * 128)

    def test_blog_posts_in_context(self):
        response = self.client.get('/')
        self.assertIsNotNone(response.context['posts'])

    def test_five_blog_posts_in_context(self):
        response = self.client.get('/')
        self.assertEquals(len(response.context['posts']), 5)

    def test_five_blog_posts_in_context_if_more(self):
        author = Author.objects.first()
        Post.objects.create(author=author, title='c' * 125, content='x' * 128)
        response = self.client.get('/')
        self.assertEquals(len(response.context['posts']), 5)
        self.assertNotEqual(response.context['posts'], Post.objects.count())
