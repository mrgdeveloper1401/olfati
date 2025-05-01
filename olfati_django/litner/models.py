from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import UserModel
from core.models import CreateMixin, UpdateMixin, SoftDeleteMixin


class MyLinterClass(CreateMixin, UpdateMixin, SoftDeleteMixin):
    class Meta:
        db_table = "linter_class"
        verbose_name = 'کلاس'
        verbose_name_plural = 'کلاس ها'
        ordering = ("-created_at",)

    title = models.CharField(verbose_name="عنوان", max_length=255)
    study_field = models.CharField(max_length=100, verbose_name="رشته تحصیلی")
    cover_image = models.ImageField(upload_to="linter_class/%Y/%m/%d", null=True)
    author = models.ForeignKey(UserModel, on_delete=models.PROTECT, verbose_name="نویسنده")

    def __str__(self):
        return self.title


class LinterModel(CreateMixin, UpdateMixin, SoftDeleteMixin):
    class Meta:
        db_table = "linter_model"
        verbose_name = 'فصل'
        verbose_name_plural = 'فصل ها'
        ordering = ("-created_at",)

    title = models.CharField(verbose_name='عنوان', max_length=255)
    description = models.TextField()
    cover_image = models.ImageField(upload_to="linter_season/%Y/%m/%d", null=True)
    price = models.FloatField(verbose_name='قیمیت فصل')
    myclass = models.ForeignKey(MyLinterClass, related_name='linter', on_delete=models.PROTECT,
                                verbose_name='کلاس مربوطه')
    # data_created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    paid_users = models.ManyToManyField(UserModel, related_name='paid_litner', blank=True,
                                        verbose_name='دسترسی کاربران')
    is_sale = models.BooleanField(default=False, help_text="قابل فروش باشد")

    def is_paid_user(self, user):
        return self.paid_users.filter(id=user.id).only("id").exists()

    # def have_karname(self, user):
    #     return LitnerKarNameModel.objects.filter(user=user).only("id").exists()

    def is_author(self, user):
        return user.id == self.myclass.author.id

    @property
    def paid_user_count(self):
        return self.paid_users.count()

    def __str__(self):
        return self.title


class LeitnerBox(CreateMixin, UpdateMixin):
    """
    مدل برای خانه‌های لایتنر (5 خانه)
    """
    BOX_NUMBERS = (
        (1, 'خانه ۱'),
        (2, 'خانه ۲'),
        (3, 'خانه ۳'),
        (4, 'خانه ۴'),
        (5, 'خانه ۵'),
    )
    linter = models.ForeignKey(LinterModel, on_delete=models.PROTECT, verbose_name="فصل", related_name="linter_box")
    box_number = models.IntegerField(choices=BOX_NUMBERS, default=1, verbose_name="شماره خانه")
    # is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("باکس")
        verbose_name_plural = _("باکس ها")
        db_table = "linter_box"
        unique_together = ('linter', 'box_number')

    def move_to_next_box(self):
        """انتقال کارت به خانه بعدی"""
        if self.box_number < 5:
            self.box_number += 1
            self.save()

    def reset_to_first_box(self):
        """بازگشت کارت به خانه اول"""
        self.box_number = 1
        self.save()

# TODO, when clean migration we must remove field=True in field season
class LinterFlashCart(CreateMixin, UpdateMixin):
    box = models.PositiveIntegerField(default=1)
    season = models.ForeignKey(LinterModel, on_delete=models.PROTECT, related_name="linter_flash_cart", null=True)
    question_text = models.CharField(max_length=255, verbose_name="سوال را وارد کنید")
    answers_text = models.TextField(max_length=200, verbose_name="جواب را وارد کنید", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    @property
    def get_box_number(self):
        return self.box

    class Meta:
        db_table = 'linter_flash_cart'
        verbose_name = _("فلش کارت")
        verbose_name_plural = _("فلش کارت ها")

# TODO, when clean migration we remove field null=True
class UserAnswer(CreateMixin, UpdateMixin):
    flash_cart = models.ForeignKey(LinterFlashCart, on_delete=models.PROTECT, related_name="linter_flash_cart",
                                   null=True)
    is_correct = models.BooleanField(default=False)

    class Meta:
        db_table = 'leitner_user_answers'
        verbose_name = _('پاسخ کاربر')
        verbose_name_plural = _('پاسخ‌های کاربران')


class UserProgress(CreateMixin, UpdateMixin, SoftDeleteMixin, ):
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name='leitner_progress')
    linter = models.ForeignKey(LinterModel, on_delete=models.PROTECT, related_name='user_progress')
    total_questions = models.PositiveIntegerField(verbose_name=_('تعداد کل سوالات'), default=0)
    answered_questions = models.PositiveIntegerField(verbose_name=_('تعداد پاسخ‌های داده شده'), default=0)
    correct_answers = models.PositiveIntegerField(verbose_name=_('تعداد پاسخ‌های صحیح'), default=0)
    current_box_distribution = models.JSONField(
        verbose_name=_('توزیع کارت‌ها در خانه‌ها'),
        default=dict,
        help_text=_('تعداد کارت‌ها در هر خانه لایتنر')
    )
    last_activity = models.DateTimeField(auto_now=True, verbose_name=_('آخرین فعالیت'))

    class Meta:
        db_table = 'leitner_user_progress'
        verbose_name = _('پیشرفت کاربر')
        verbose_name_plural = _('پیشرفت‌های کاربران')
        unique_together = ('user', 'linter')

    def update_progress(self, answer):
        if answer.is_correct:
            self.correct_answers += 1
        self.answered_questions += 1
        self.save()
        self.update_box_distribution()

    def update_box_distribution(self):
        boxes = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        user_flashcards = LinterFlashCart.objects.filter(
            box__linter=self.linter,
            useranswer__user=self.user
        ).distinct()

        for card in user_flashcards:
            boxes[card.box.box_number] += 1

        self.current_box_distribution = boxes
        self.save()
