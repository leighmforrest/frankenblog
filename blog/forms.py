from django.forms import ModelForm
from django.core.exceptions import ValidationError

from blog.models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

    def clean_title(self):
        data = self.cleaned_data['title']

        # check if title is more than 64 characters
        if len(data) > 128:
            raise ValidationError('Title cannot be more than 128 characters.')
        return data

    def clean_content(self):
        data = self.cleaned_data['content']

        # check if title is more than 3000 characters
        if len(data) > 3000:
            raise ValidationError('Content cannot be more than 300 characters.')
        return data


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        data = self.cleaned_data['content']
        # check if title is more than 3000 characters
        if len(data) > 512:
            raise ValidationError('Content cannot be more than 300 characters.')
        return data
