from django.db import models
from django.utils.translation import gettext_lazy as _


class CreateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UpdateMixin(models.Model):
    updated_at = models.DateTimeField(_("اخرین بروزرسانی"), auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    deleted_at = models.DateTimeField(_("تاریخ حذف"), editable=False, blank=True, null=True)
    is_deleted = models.BooleanField(_("حذف شده یا خیر"), editable=False, null=True, blank=True)

    class Meta:
        abstract = True


class OwnerMixin(models.Model):
    created_by = models.ForeignKey(
        "accounts.UserModel",
        on_delete=models.PROTECT,
        verbose_name=_("ایجاد کننده"),
        related_name="%(class)s_created",
        null=True,
        editable=False,
    )

    class Meta:
        abstract = True