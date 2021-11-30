from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from .views import Home

urlpatterns = [
    path('', Home.as_view(), name='home'),

]
