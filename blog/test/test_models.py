from django.test import TestCase

from users.models import CustomUser
from blog.models import Author, Post, Comment


class TestAuthor(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create(username='eljefe', password='Passw3rd!')
        author = Author.objects.create(author=user, bio='Hello there!')

        for _ in range(5):
            Post.objects.create(author=author, title='f' * 120, content='h' * 500)

    def setUp(self):
        self.author = Author.objects.first()

    def test_author_exists(self):
        self.assertIsNotNone(self.author)

    def test_author_is_user(self):
        user = CustomUser.objects.first()
        self.assertEqual(self.author.author, user)

    def test_author_string(self):
        format_string = f'{self.author.author.username}'
        self.assertEqual(format_string, str(self.author))

    def test_author_has_related_posts(self):
        posts = self.author.posts.all()
        self.assertTrue(posts.count() > 0)


class TestPost(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create(username='eljefe', password='Passw3rd!')
        author = Author.objects.create(author=user, bio='Hello there!')

        Post.objects.create(author=author, title='first post', content='hello there')
        Post.objects.create(author=author, title='second post', content='hello there again')

    def setUp(self):
        self.posts = Post.objects.all()

    def test_post_exists(self):
        for post in self.posts:
            self.assertIsNotNone(post)

    def test_posts_ordered(self):
        posts = self.posts
        self.assertTrue(posts[0].created_at > posts[1].created_at)

    def test_string(self):
        post = self.posts[0]
        test_string = f'{post.title} by {post.author.author.username}'
        self.assertEqual(test_string, str(post))

    def test_related_name_author_posts(self):
        author = Author.objects.first()
        self.assertEqual(len(author.posts.all()), 2)

    def test_get_absolute_url(self):
        post = Post.objects.first()
        url = f'/blog/{post.id}/'
        self.assertEqual(url, post.get_absolute_url())


class TestComments(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create(username='eljefe', password='Passw3rd!')
        author = Author.objects.create(author=user, bio='Hello there!')

        commentor = CustomUser.objects.create(username='scrubby', password='Passw3rd!')

        post = Post.objects.create(author=author, title='first post', content='hello there')
        Post.objects.create(author=author, title='second post', content='hello there again!')
        Comment.objects.create(post=post, user=commentor, content='Nice job!')

    def setUp(self):
        self.post = Post.objects.last()
        self.commentor = CustomUser.objects.get(username='scrubby')

    def test_add_comment(self):
        comment = Comment.objects.create(post=self.post, user=self.commentor, content='nice package')
        self.assertEqual(Comment.objects.get(content='nice package'), comment)

    def test_related_name_post_comments(self):
        post = self.post
        comment = post.comments.first()
        self.assertEqual(comment.content, 'Nice job!')

    def test_get_absolute_url(self):
        comment = self.post.comments.first()
        url = f'/blog/{comment.post.pk}/'
        self.assertEqual(comment.get_absolute_url(), url)

    def test_comment_str(self):
        comment = self.post.comments.first()
        comment.content = 'r' * 125
        self.assertEqual(comment.content[:100], str(comment))
