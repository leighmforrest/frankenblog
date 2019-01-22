from django.db import models
from django.urls import reverse
from users.models import CustomUser


class Author(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='author')
    bio = models.TextField()

    def __str__(self):
        return f'{self.author.username}'


class Post(models.Model):
    title = models.CharField(max_length=200, help_text='Enter your post title here.')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='posts')
    content = models.TextField(help_text='Enter your blog post here.')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (('can_create_post', 'can_create_post'),)
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.title} by {self.author.author.username}'


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='comments', null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', help_text='Enter your blog post here.')
    content = models.TextField(help_text='Enter your comment here.')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.content[:100]}'

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'pk': self.post.pk})
