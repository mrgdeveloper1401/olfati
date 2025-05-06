from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserModel


@receiver(post_save, sender=UserModel)
def change_status_user(sender, instance, **kwargs):
    if instance.first_name and instance.last_name and instance.username and instance.melli_code:
        instance.is_complete = True
        instance.save()
