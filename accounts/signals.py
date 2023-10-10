from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Profile, User


@receiver(post_save, sender=User)
def createUserProfile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            profile = Profile.objects.get(user=instance)
            profile.save()
        except:
            Profile.objects.create(user=instance)