from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from olfati_django.custom_middlewere import get_current_user
from . import models


@receiver(post_save, sender=models.LinterModel)
def create_linter_box(sender, instance, created, **kwargs):
    if created:
        lst =[
            models.LeitnerBox(
                linter=instance,
                box_number=i
            )
            for i in range(1, 7)
        ]
        models.LeitnerBox.objects.bulk_create(lst)


@receiver(post_save, sender=models.LinterFlashCart)
def create_user_linter_flash_cart(sender, instance, created, **kwargs):
    if created:
        all_paid_users = instance.season.paid_users.all()
        lst = [
            models.UserLinterFlashCart(
                user=i,
                flash_cart=instance
            )
            for i in all_paid_users
        ]

        if lst:
            models.UserLinterFlashCart.objects.bulk_create(lst)
