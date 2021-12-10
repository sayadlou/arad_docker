from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView, FormView


# Create your views here.
class Home(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        pass


# Create your views here.
class AboutUs(TemplateView):
    template_name = 'core/about_us.html'

    def get_context_data(self, **kwargs):
        pass
