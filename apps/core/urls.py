from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from .views import Home, ContactUs, AboutUs

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('contac_us/', ContactUs.as_view(), name='contac_us'),
    path('about_us/', AboutUs.as_view(), name='about_us'),

]
