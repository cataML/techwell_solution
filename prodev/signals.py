from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ProdevProfile

@receiver(post_save, sender=User)
def create_or_update_prodev_profile(sender, instance, created, **kwargs):
    if created:
        ProdevProfile.objects.create(user=instance)
    else:
        if hasattr(instance, "prodev_profile"):
            instance.prodev_profile.save()


