from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import BlogPost
from .forms import BlogPostForm
import uuid


class BlogPostListView(View):
    template_name = 'blog/post_list.html'

    def get(self, request):
        posts = BlogPost.objects.filter(is_published=True)
        return render(request, self.template_name, {'posts': posts})


class BlogPostDetailView(View):
    template_name = 'blog/post_detail.html'

    def get(self, request, slug):
        post = get_object_or_404(BlogPost, slug=slug)

        post.views_count += 1
        post.save()

        return render(request, self.template_name, {'post': post})


class BlogPostCreateView(View):
    template_name = 'blog/post_form.html'

    def get(self, request):
        form = BlogPostForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog_post_list')  # Замените на ваш путь
        return render(request, self.template_name, {'form': form})


class BlogPostEditView(View):
    template_name = 'blog/post_form.html'

    def get(self, request, slug):
        post = get_object_or_404(BlogPost, slug=slug)
        form = BlogPostForm(instance=post)
        return render(request, self.template_name, {'form': form})

    def post(self, request, slug):
        post = get_object_or_404(BlogPost, slug=slug)
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('blog:blog_post_detail', slug=post.slug)
        return render(request, self.template_name, {'form': form})


class BlogPostDeleteView(View):
    def get(self, request, slug):
        post = get_object_or_404(BlogPost, slug=slug)
        post.delete()
        return redirect('blog_post_list')
