from django.urls import path

from .views import SlugView, TagView, CategoryView, IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('post/<slug:slug>', SlugView.as_view(), name='slug'),
    path('tag/', TagView.as_view(), name='tag'),
    path('category/<str:category>', CategoryView.as_view(), name='category'),
]
