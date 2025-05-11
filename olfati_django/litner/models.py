from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import UserModel
from core.models import CreateMixin, UpdateMixin, SoftDeleteMixin
from utils.vlaidations import validate_image_size


class MyLinterClass(CreateMixin, UpdateMixin, SoftDeleteMixin):
    class Meta:
        db_table = "linter_class"
        verbose_name = _('کلاس')
        verbose_name_plural = _('کلاس‌ها')
        ordering = ("-created_at",)

    title = models.CharField(verbose_name=_("عنوان"), max_length=255)
    study_field = models.CharField(max_length=100, verbose_name=_("رشته تحصیلی"))
    cover_image = models.ImageField(
        upload_to="linter_class/%Y/%m/%d",
        null=True,
        validators=[validate_image_size],
        verbose_name=_("تصویر کاور")
    )
    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        verbose_name=_("نویسنده"),
        limit_choices_to={'is_staff': True}
    )

    def __str__(self):
        return self.title


class LinterModel(CreateMixin, UpdateMixin, SoftDeleteMixin):
    class Meta:
        db_table = "linter_model"
        verbose_name = _('فصل')
        verbose_name_plural = _('فصل‌ها')
        ordering = ("-created_at",)

    title = models.CharField(verbose_name=_('عنوان'), max_length=255)
    description = models.TextField(verbose_name=_('توضیحات'))
    cover_image = models.ImageField(
        upload_to="linter_season/%Y/%m/%d",
        null=True,
        validators=[validate_image_size],
        verbose_name=_("تصویر کاور")
    )
    price = models.FloatField(verbose_name=_('قیمت فصل'))
    myclass = models.ForeignKey(
        MyLinterClass,
        related_name='linter',
        on_delete=models.CASCADE,
        verbose_name=_('کلاس مربوطه')
    )
    paid_users = models.ManyToManyField(
        UserModel,
        related_name='paid_litner',
        blank=True,
        verbose_name=_('دسترسی کاربران')
    )
    is_sale = models.BooleanField(
        default=True,
        verbose_name=_("قابل فروش باشد"),
        help_text=_("قابل فروش باشد")
    )

    def is_paid_user(self, user):
        return self.paid_users.filter(id=user.id).only("id").exists()

    def is_author(self, user):
        return user.id == self.myclass.author.id

    @property
    def paid_user_count(self):
        return self.paid_users.count()

    def __str__(self):
        return self.title


class LeitnerBox(CreateMixin, UpdateMixin, SoftDeleteMixin):
    """
    مدل برای خانه‌های لایتنر (5 خانه)
    """
    BOX_NUMBERS = (
        (1, _('خانه ۱')),
        (2, _('خانه ۲')),
        (3, _('خانه ۳')),
        (4, _('خانه ۴')),
        (5, _('خانه ۵')),
        (6, _('خانه ۶')),
    )
    linter = models.ForeignKey(
        LinterModel,
        on_delete=models.CASCADE,
        verbose_name=_("فصل"),
        related_name="linter_box"
    )
    box_number = models.IntegerField(
        choices=BOX_NUMBERS,
        default=1,
        verbose_name=_("شماره خانه")
    )

    class Meta:
        verbose_name = _("باکس")
        verbose_name_plural = _("باکس‌ها")
        db_table = "linter_box"
        unique_together = ('linter', 'box_number')


class LinterFlashCart(CreateMixin, UpdateMixin, SoftDeleteMixin):
    # box = models.PositiveIntegerField(default=1, verbose_name=_("باکس"))
    season = models.ForeignKey(
        LinterModel,
        on_delete=models.CASCADE,
        related_name="linter_flash_cart",
        null=True,
        verbose_name=_("فصل")
    )
    question_text = models.CharField(
        max_length=255,
        verbose_name=_("سوال را وارد کنید")
    )
    answers_text = models.TextField(
        max_length=200,
        verbose_name=_("جواب را وارد کنید"),
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("فعال")
    )

    def __str__(self):

        return self.question_text


    class Meta:
        db_table = 'linter_flash_cart'
        verbose_name = _("فلش کارت")
        verbose_name_plural = _("فلش کارت‌ها")


class UserLinterFlashCart(CreateMixin, UpdateMixin, SoftDeleteMixin):
    flash_cart = models.ForeignKey(LinterFlashCart, on_delete=models.DO_NOTHING, related_name='linter_flash_cart',
                                   verbose_name=_("فلش کارت"))
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, related_name="user_flash_cart",
                             verbose_name=_("کاربر"))
    box = models.PositiveSmallIntegerField(_("باکس"), default=1)

    class Meta:
        db_table = 'user_linter_flash_cart'
        verbose_name = _("فلش کارت کاربر")
        verbose_name_plural = _("فلش کارت های کاربر")


class UserAnswer(CreateMixin, UpdateMixin, SoftDeleteMixin):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="user_answer",
        null=True,
        verbose_name=_("کاربر")
    )
    flash_cart = models.ForeignKey(
        UserLinterFlashCart,
        on_delete=models.CASCADE,
        related_name="user_answer_flash_cart",
        null=True,
        verbose_name=_("فلش کارت")
    )
    is_correct = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_("پاسخ صحیح"),
        help_text=_("در صورت عدم پاسخ مقدار نال یا همان بی پاسخ ذخیره خواهد شد")
    )

    class Meta:
        db_table = 'leitner_user_answers'
        verbose_name = _('پاسخ کاربر')
        verbose_name_plural = _('پاسخ‌های کاربران')
