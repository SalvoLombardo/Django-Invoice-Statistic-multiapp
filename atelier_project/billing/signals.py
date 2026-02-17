from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import Invoice


@receiver([post_save, post_delete], sender=Invoice)
def invalidate_invoice_cache(sender, instance, **kwargs):
    cache.delete('invoice_list')
