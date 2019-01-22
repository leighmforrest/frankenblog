from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect


from blog.models import Post
from blog.forms import CommentForm, PostForm


class PostListView(ListView):
    template_name = 'pages/home.html'
    context_object_name = 'posts'
    model = Post


class PostDetailView(DetailView):
    template_name = 'blog/detail.html'
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user and self.request.user.is_authenticated:
            context['form'] = CommentForm()
        return context


class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'blog/create.html'
    model = Post
    form_class = PostForm
    permission_required = 'blog.can_create_post'

    def form_valid(self, form):
        form.instance.author = self.request.user.author.first()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'blog/update.html'
    model = Post
    form_class = PostForm
    context_object_name = 'post'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class CommentCreateView(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    http_method_names = ['post']

    def form_invalid(self, form):
        post = Post.objects.get(pk=self.kwargs['pk'])
        messages.error(self.request, 'Comment not created.')
        return redirect(post.get_absolute_url())

    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs['pk'])
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.post = post
        comment.save()
        return super().form_valid(form)
