from django.dispatch import receiver
from django.db.models.signals import post_save
# from django.contrib.auth.models import Group

from .models import Vendor, User, Customer


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_vendor:
            # group = Group.objects.get(name='vendors')
            # instance.groups.add(group)
            Vendor.objects.create(user=instance)
        if instance.is_customer:
            Customer.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_vendor:
        instance.vendor.save()
    if instance.is_customer:
        instance.customer.save()
