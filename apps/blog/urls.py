from django.urls import path

from .views import Blog, PostView, SlugView, Tag, show_genres, CategoryView

urlpatterns = [
    # path('category/<str:cat>', views.category, name='blog_category_cat'),
    path('', Blog.as_view(), name='home'),
    path('tag/', Tag.as_view(), name='tag'),
    # path('category/', Tag.as_view(), name='tag'),
    path('post/<int:pk>', PostView.as_view(), name='blog_post'),
    path('post/<slug:slug>', SlugView.as_view(), name='blog_slug'),
    path('category/<str:category>', CategoryView.as_view(), name='blog_slug'),
    path('cat_temp/', show_genres),
]
