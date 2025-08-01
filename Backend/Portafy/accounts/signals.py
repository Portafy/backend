from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import User, Customer


# create customer profile when user is registered
@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
