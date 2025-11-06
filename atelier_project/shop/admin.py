from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Payment

# Registrazione di Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # genera slug in automatico


# Registrazione di Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'model_name', 'color')
    ordering = ('-created_at',)


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)