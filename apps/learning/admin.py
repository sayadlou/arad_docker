from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 10


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'slug']
    list_display = ['title', 'slug']
