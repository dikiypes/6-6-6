from django.urls import path
from .views import BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostEditView, BlogPostDeleteView

app_name = 'blog'

urlpatterns = [
    path('', BlogPostListView.as_view(), name='blog_post_list'),
    path('create/', BlogPostCreateView.as_view(), name='blog_post_create'),
    path('<slug:slug>/', BlogPostDetailView.as_view(), name='blog_post_detail'),
    path('<slug:slug>/edit/', BlogPostEditView.as_view(), name='blog_post_edit'),
    path('<slug:slug>/delete/', BlogPostDeleteView.as_view(),
         name='blog_post_delete'),
]
