from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from test_dog_app.models import Profile

"""
    post_save: signal which can be triggered
    User: sender which will trigger our signal 
    receiver: decorator that maps the sender and signal to a function
    Profile: the model that is being created and saved
"""


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
