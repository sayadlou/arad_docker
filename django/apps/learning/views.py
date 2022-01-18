from django.views.generic import ListView, DetailView

from .models import Post as LearningPost
from .permitions import BoughtSlugUserMixin


class IndexView(ListView):
    model = LearningPost
    template_name = 'learning/index.html'
    paginate_by = 6

    # all_posts = Post.objects.order_by('pub_date').filter(status='Published')

    def get_queryset(self):
        return self.model.objects.order_by('pub_date').filter(status='Published')


class SlugView(BoughtSlugUserMixin, DetailView):
    template_name = 'learning/slug.html'
    model = LearningPost


class TagView(ListView):
    model = LearningPost
    template_name = 'learning/tag.html'
    paginate_by = 6

    def get_queryset(self):
        tag = self.request.GET.get("tag", "")
        tag = tag.lower()
        return self.model.objects.order_by('pub_date').filter(status='Published').filter(tags__contains=[tag])


class CategoryView(ListView):
    model = LearningPost
    template_name = 'learning/category.html'
    paginate_by = 6

    def get_queryset(self):
        category = self.kwargs['category']
        return self.model.objects.order_by('pub_date').filter(category__name__iexact=category)
