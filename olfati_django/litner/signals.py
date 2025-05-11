from django.db.models.signals import post_save, pre_save, m2m_changed
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


@receiver(m2m_changed, sender=models.LinterModel.paid_users.through)
def create_user_flash_cart_after_add_user(sender, instance, action, pk_set, **kwargs):
    """
    وقتی کاربری به فصل اضافه می‌شود، فلش کارت‌های آن فصل را برای کاربر ایجاد می‌کند
    """
    if action == "post_add":
        # دریافت فصل مربوطه
        season = instance

        # دریافت تمام فلش کارت‌های این فصل
        flash_cards = season.linter_flash_cart.all()

        # دریافت کاربران جدیدی که اضافه شده‌اند
        new_users = models.UserModel.objects.filter(id__in=pk_set).only("phone_number", "first_name", "last_name")

        # ایجاد UserLinterFlashCart برای هر کاربر جدید و هر فلش کارت
        user_flash_cards_to_create = []
        for user in new_users:
            for flash_card in flash_cards:
                if not models.UserLinterFlashCart.objects.filter(user=user, flash_cart=flash_card).exists():
                    user_flash_cards_to_create.append(
                        models.UserLinterFlashCart(
                            user=user,
                            flash_cart=flash_card,
                            box=1  # مقدار پیش‌فرض برای باکس
                        )
                    )

        if user_flash_cards_to_create:
            models.UserLinterFlashCart.objects.bulk_create(user_flash_cards_to_create)