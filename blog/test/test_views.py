from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from users.models import CustomUser
from blog.models import Post, Comment, Author
from blog.forms import CommentForm


class TestCommentCreateView(TestCase):
    @classmethod
    def setUpTestData(cls):
        CustomUser = get_user_model()
        user = CustomUser.objects.create_user(username='eljefe', password='Passw3rd!')
        author = Author.objects.create(author=user, bio='Hello there!')

        Post.objects.create(author=author, title='first post', content='hello there')
        Post.objects.create(author=author, title='second post', content='hello there again')

    def setUp(self):
        self.logged_in = self.client.login(username='eljefe', password='Passw3rd!')
        self.assertTrue(self.logged_in)

    def test_post_add_comment(self):
        post = Post.objects.first()

        response = self.client.post(
            reverse('blog:comment', kwargs={'pk': post.pk}), {'content': 'r' * 50}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(post.comments.count() > 0)

    def test_post_invalid_comment(self):
        post = Post.objects.first()

        response = self.client.post(
            reverse('blog:comment', kwargs={'pk': post.pk}), {'content': 'r' * 750},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertTrue(len(messages) > 0)

    def test_cannot_get_request(self):
        post = Post.objects.first()
        response = self.client.get(reverse_lazy('blog:comment', kwargs={'pk': post.pk}))
        self.assertNotEqual(response.status_code, 200)


class TestPostDetailView(TestCase):
    @classmethod
    def setUpTestData(cls):
        CustomUser = get_user_model()
        user = CustomUser.objects.create_user(username='eljefe', password='Passw3rd!')
        author = Author.objects.create(author=user, bio='Hello there!')

        Post.objects.create(author=author, title='first post', content='hello there')
        Post.objects.create(author=author, title='second post', content='hello there again')

    def setUp(self):
        self.logged_in = self.client.login(username='eljefe', password='Passw3rd!')
        self.post = Post.objects.first()
        self.assertTrue(self.logged_in)

    def test_post_in_context_authenticated_user(self):
        response = self.client.get(reverse_lazy('blog:post', kwargs={'pk': self.post.pk}))
        post = response.context['post']
        self.assertEqual(post, self.post)

    def test_post_in_context_unauthenticated_user(self):
        client = Client()
        response = client.get(reverse('blog:post', kwargs={'pk': self.post.pk}))
        post = response.context['post']
        self.assertEqual(post, self.post)

    def test_authenticated_user_get_form(self):
        response = self.client.get(reverse('blog:post', kwargs={'pk': self.post.pk}))
        self.assertIsNotNone(response.context['form'])
        self.assertIsInstance(response.context['form'], CommentForm)

    def test_authenticated_user_form_is_comment_form(self):
        response = self.client.get(reverse('blog:post', kwargs={'pk': self.post.pk}))
        self.assertIsInstance(response.context['form'], CommentForm)

    def test_unauthenticated_user_cannot_get_form(self):
        client = Client()
        response = client.get(reverse('blog:post', kwargs={'pk': self.post.pk}))
        self.assertTrue('form' not in response.context)


class TestPostCreateView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up blogger model
        CustomUser = get_user_model()
        user = CustomUser.objects.create_user(username='eljefe', password='Passw3rd!')
        author = Author.objects.create(author=user, bio='Hello there!')

        # Set up permission
        permission = Permission.objects.get(name='can_create_post')
        user.user_permissions.add(permission)
        user.save()

    def setUp(self):
        self.logged_in = self.client.login(username='eljefe', password='Passw3rd!')
        self.assertTrue(self.logged_in)

        # set up user model
        CustomUser.objects.create_user(username='scrubby', password='Passw3rd!')

    def test_blogger_can_get(self):
        response = self.client.get(reverse_lazy('blog:create'))
        self.assertTrue(response.status_code == 200)

    def test_user_cannot_get(self):
        client = Client()
        client.login(username='scrubby', password='Passw3rd!')
        response = self.client.get(reverse_lazy('blog:create'))
        self.assertTrue(response.status_code != 403)

    def test_blogger_can_create_post(self):
        posts = Post.objects.count()
        self.client.post(reverse_lazy('blog:create'), {'title': 'r' * 127, 'content': 'r' * 3000})
        self.assertTrue(Post.objects.count() > posts)

    def test_user_cannot_post(self):
        client = Client()
        client.login(username='scrubby', password='Passw3rd!')
        response = self.client.post(reverse_lazy('blog:create'), {'title': 'r' * 127, 'content': 'r' * 3000})
        self.assertTrue(response.status_code != 403)


class TestPostUpdateView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up blogger model
        CustomUser = get_user_model()
        user = CustomUser.objects.create_user(username='eljefe', password='Passw3rd!')
        author = Author.objects.create(author=user, bio='Hello there!')

        # set up user model
        CustomUser.objects.create_user(username='scrubby', password='Passw3rd!')

        # Set up permission
        permission = Permission.objects.get(name='can_create_post')
        user.user_permissions.add(permission)
        user.save()

        # Create test object
        post = Post.objects.create(title='Hello', content='This is a journey into sound!', author=author)

    def setUp(self):
        self.logged_in = self.client.login(username='eljefe', password='Passw3rd!')
        self.assertTrue(self.logged_in)

        self.post = Post.objects.first()

    def test_blogger_can_get(self):
        response = self.client.get(reverse_lazy('blog:update', kwargs={'pk': self.post.pk}))
        self.assertTrue(response.status_code == 200)

    def test_anonymous_cannot_get(self):
        client = Client()
        response = client.get(reverse_lazy('blog:update', kwargs={'pk': self.post.pk}))
        print(response.status_code)
        self.assertTrue(response.status_code == 403)

    def test_blogger_can_update_post(self):
        update_data = {'title': 'Hello', 'content': 'World'}
        self.client.post(reverse_lazy('blog:update', kwargs={'pk': self.post.pk}), update_data)
        updated_object = Post.objects.get(pk=self.post.pk)
        self.assertTrue(updated_object.content == update_data['content'])
        self.assertTrue(updated_object.title == update_data['title'])

    def test_user_cannot_update(self):
        update_data = {'title': 'Hello', 'content': 'World'}
        login = self.client.login(username='scrubby', password='Passw3rd!')
        response = self.client.post(reverse('blog:update', kwargs={'pk': self.post.pk}), update_data)
        self.assertEqual(response.status_code, 403)
