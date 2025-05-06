from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from . import models

@admin.register(models.UserModel)
class UserModelAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "username", "melli_code")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_complete",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "melli_code", "username", "usable_password", "password1", "password2"),
            },
        ),
    )
    list_display = ("phone_number", "email", "first_name", "last_name", "is_staff", "is_complete")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("phone_number",)
    ordering = ("-date_joined",)
    list_per_page = 20


@admin.register(models.OtpModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "otp_code", "created_at", "expired_date")
    search_fields = ("phone_number",)
