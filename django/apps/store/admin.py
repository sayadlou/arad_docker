from django.contrib import admin

# Register your models here.
from .models import Cart, CartItem


def has_superuser_permission(request):
    return request.user.is_active and request.user.is_superuser


# Only active superuser can access root admin site (default)
admin.site.has_permission = has_superuser_permission


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    search_fields = ['owner']
    list_display = ['owner']
    readonly_fields = ['id']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    search_fields = ['cart']
    list_display = ['cart']
    readonly_fields = ['id']
