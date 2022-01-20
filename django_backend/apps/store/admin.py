from django.contrib import admin

# Register your models here.
from .models import Cart, CartItem




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
