from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Post as LearningPost
from ..blog.views import Blog, PostDetail as BlogPost, Slug as BlogSlug, Tag as BlogTag, CategoryList as BlogCategory, \
    Tag, CategoryList


class IndexView(Blog):
    model = LearningPost


class SlugView(UserPassesTestMixin, BlogSlug):
    model = LearningPost
    raise_exception = False

    def handle_no_permission(self):
        return render(self.request, template_name="learning/pervent_message.html")

    def test_func(self):
        slug = self.kwargs.get(self.slug_url_kwarg)
        post = get_object_or_404(LearningPost, slug__iexact=slug)
        user_id = self.request.user.pk
        is_user_owner = post.purchaser.filter(pk=user_id).count()
        if is_user_owner == 1 and self.request.user.is_authenticated:
            return True
        return False


class TagView(Tag):
    model = LearningPost


class CategoryView(CategoryList):
    model = LearningPost
