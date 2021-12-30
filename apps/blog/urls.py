from django.urls import path

from .views import Blog, PostView, SlugView, Tag, CategoryView

urlpatterns = [
    path('', Blog.as_view(), name='home'),
    path('tag/', Tag.as_view(), name='tag'),
    path('post/<int:pk>', PostView.as_view(), name='post'),
    path('post/<slug:slug>', SlugView.as_view(), name='slug'),
    path('category/<str:category>', CategoryView.as_view(), name='category'),
]
