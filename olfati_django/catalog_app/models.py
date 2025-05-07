from django.db import models
from django.utils.text import slugify
import os
from django.utils.translation import gettext_lazy as _

from core.models import CreateMixin, UpdateMixin, SoftDeleteMixin
from utils.vlaidations import validate_image_size


def image_upload_path(instance, filename):
    """Generate upload path based on model name and image title."""
    base_filename, file_extension = os.path.splitext(filename)
    return f"catalog/images/{slugify(instance.title)}/{slugify(base_filename)}{file_extension}"


class Image(CreateMixin, UpdateMixin, SoftDeleteMixin):
    user = models.ForeignKey("accounts.UserModel", on_delete=models.PROTECT, related_name="user_upload_user",
                             null=True, verbose_name=_("کاربر"))
    # فیلدهای اصلی
    title = models.CharField(
        _("عنوان تصویر"),
        max_length=200,
        help_text="عنوان توصیفی برای تصویر (ضروری)"
    )
    image_file = models.ImageField(
        upload_to=image_upload_path,
        verbose_name=_("فایل تصویر"),
        help_text="فرمت‌های پشتیبانی: JPG, PNG, WebP",
        width_field="image_width",
        height_field="image_height",
        validators=[validate_image_size]
    )
    image_width = models.PositiveIntegerField(_("عرض تصویر"), editable=False, null=True)
    image_height = models.PositiveIntegerField(_("ارتفاع تصویر"), editable=False, null=True)
    image_url = models.CharField(_("ادرس عکس"), max_length=255, editable=False, null=True)

    # متادیتا
    # alt_text = models.CharField(
    #     max_length=200,
    #     blank=True,
    #     verbose_name="متن جایگزین (Alt)",
    #     help_text="برای دسترسی‌پذیری و SEO"
    # )
    caption = models.TextField(
        _("توضیح تصویر"),
        blank=True,
        help_text="توضیح اختیاری درباره تصویر"
    )

    # دسته‌بندی و تگ‌ها
    # category = models.ForeignKey(
    #     'Category',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     verbose_name="دسته‌بندی"
    # )
    # tags = models.ManyToManyField(
    #     'Tag',
    #     blank=True,
    #     verbose_name="تگ‌ها"
    # )

    # مدیریت فایل
    file_size = models.PositiveIntegerField(
        _("حجم فایل به صورت بایت"),
        editable=False,
        null=True,
    )
    file_format = models.CharField(
        _("فرمت فایل"),
        max_length=10,
        editable=False,
    )

    # فعال/غیرفعال
    # is_active = models.BooleanField(
    #     default=True,
    #     verbose_name="فعال",
    #     help_text="نمایش/عدم نمایش تصویر در سایت"
    # )

    class Meta:
        verbose_name = "تصویر"
        verbose_name_plural = "تصاویر"
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """محاسبه خودکار فرمت، حجم فایل و ابعاد تصویر قبل از ذخیره."""
        if self.image_file:
            self.file_size = self.image_file.size
            self.file_format = os.path.splitext(self.image_file.name)[1][1:].upper()
            self.image_url = self.image_file.url
        super().save(*args, **kwargs)


# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(unique=True)


# class Tag(models.Model):
#     name = models.CharField(max_length=50)
#     slug = models.SlugField(unique=True)
