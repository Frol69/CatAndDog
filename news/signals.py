from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.dispatch import receiver

from .models import Post


@receiver([post_save, post_delete], sender=Post)
def cache_post(sender, instance, *args, **kwargs):
    cache.delete(f'post-{instance.pk}')
