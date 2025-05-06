import random
from datetime import timedelta

from django.contrib.auth import models as auth_models
from django.db import models
from django.utils import timezone

from core.models import CreateMixin, SoftDeleteMixin
from utils.vlaidations import PhoneValidator
from .managers import UserManager


class UserModel(auth_models.AbstractUser, SoftDeleteMixin):
    # full_name = models.CharField(max_length=35, verbose_name="نام کامل")
    study_field = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=30, blank=True)
    melli_code = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=12, unique=True, validators=[PhoneValidator()])
    is_complete = models.BooleanField(default=False)

    class Meta:
        db_table = "user"
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ('username', 'melli_code')

    def __str__(self):
        return self.phone_number

    def save(self, *args, **kwargs):
        if self.is_complete is False:
            if self.username and self.first_name and self.last_name and self.melli_code and self.study_field:
                self.is_complete = True
        return super().save(*args, **kwargs)


class OtpModel(CreateMixin):
    phone_number = models.CharField(max_length=12)
    otp_code = models.CharField(max_length=6, blank=True)
    expired_date = models.DateTimeField(blank=True, editable=False, null=True)

    def __str__(self):
        return f"{self.phone_number} | {self.otp_code}"

    def save(self, *args, **kwargs):
        self.otp_code = random.randint(111111, 999999)
        self.expired_date = timezone.now() + timedelta(minutes=2)
        return super().save(*args, **kwargs)

    @property
    def is_expired_otp_code(self):
        return self.expired_date < timezone.now()

    class Meta:
        db_table = "otp_code"
