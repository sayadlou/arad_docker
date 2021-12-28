from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, InvalidPage
from django.views.generic import ListView, DetailView

from .models import Post, Category
from ..account.models import UserProfile


class Blog(ListView):
    template_name = 'blog/index.html'
    model = Post
    paginate_by = 6

    # all_posts = Post.objects.order_by('pub_date').filter(status='Published')

    def get_queryset(self):
        return Post.objects.order_by('pub_date').filter(status='Published')


class Tag(ListView):
    template_name = 'blog/tag.html'
    model = Post
    paginate_by = 6

    def get_queryset(self):
        tag = self.request.GET.get("tag", "")
        tag = tag.lower()
        return Post.objects.order_by('pub_date').filter(status='Published').filter(tags__contains=[tag])


class PostView(DetailView):
    template_name = 'blog/slug.html'
    model = Post


class SlugView(DetailView):
    template_name = 'blog/slug.html'
    model = Post


class CategoryView(ListView):
    template_name = 'blog/category.html'
    model = Post
    paginate_by = 6

    def get_queryset(self):
        category = self.kwargs['category']
        category = category.lower()
        return Post.objects.order_by('pub_date').filter(category__name__iexact=category)


def show_genres(request):
    return render(request, "blog/genres.html", {'genres': Category.objects.all()})
