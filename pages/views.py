from django.views.generic import TemplateView
from blog.models import Post


class HomePageView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()[:5]

        return context


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'
