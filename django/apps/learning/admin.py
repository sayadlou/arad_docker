from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from mptt.admin import DraggableMPTTAdmin

from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 10
    readonly_fields = ['id']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'slug']
    list_display = ['title', 'slug']
    readonly_fields = ['id']
    prepopulated_fields = {'slug': ('title',)}

    def get_urls(self):
        urls = super(PostAdmin, self).get_urls()
        my_urls = [
            url(r"^export/$", export)
        ]
        return my_urls + urls


@staff_member_required
def export(self, request):
    print("Take Arvan")
    return HttpResponse("salam")
