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
            for i in range(1, 6)
        ]
        models.LeitnerBox.objects.bulk_create(lst)


# @receiver(post_save, sender=models.LinterModel)
# def set_created_by(sender, instance, created, **kwargs):
#     if created and not instance.created_by:
#         current_user = get_current_user()
#         if current_user and current_user.is_authenticated:
#             instance.created_by = current_user
#             instance.save()
