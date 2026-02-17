from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import Category, Product, Order


# ---- Category signals ----
@receiver([post_save, post_delete], sender=Category)
def invalidate_category_cache(sender, instance, **kwargs):
    cache.delete('shop_categories')
    cache.delete('admin_categories')
    cache.delete(f'category_{instance.slug}')


# ---- Product signals ----
@receiver([post_save, post_delete], sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    cache.delete('shop_categories')
    cache.delete(f'category_{instance.category.slug}')


# ---- Order signals ----
@receiver(post_save, sender=Order)
def invalidate_analytics_cache(sender, instance, **kwargs):
    cache.delete_pattern('analytics_*')
