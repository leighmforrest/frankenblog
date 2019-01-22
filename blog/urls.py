from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('create/', views.PostCreateView.as_view(), name='create'),
    path('<pk>/', views.PostDetailView.as_view(), name='post'),
    path('<pk>/update', views.PostUpdateView.as_view(), name='update'),
    path('<pk>/comment', views.CommentCreateView.as_view(), name='comment'),
]
