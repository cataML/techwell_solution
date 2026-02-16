from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import DigitalProfile, ClientProfile


@receiver(post_save, sender=User)
def create_user_profiles(sender, instance, created, **kwargs):
    if created:
        # Create both profiles when user is created
        DigitalProfile.objects.get_or_create(user=instance)
        ClientProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profiles(sender, instance, **kwargs):
    # Only save if the profile exists
    if hasattr(instance, 'digitalprofile'):
        instance.digitalprofile.save()
    if hasattr(instance, 'clientprofile'):
        instance.clientprofile.save()