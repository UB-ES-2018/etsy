from .models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

@receiver(post_save, sender=Product)
def index_post(sender, instance, **kwargs):
    if settings.INDEX_TO_ELASTIC:
        instance.indexing()
