from datetime import timedelta
from django.db import models
from django.utils import timezone

from accounts.models import UserModel
from utils.vlaidations import validate_image_size
from django.db.models.signals import post_save
from django.dispatch import receiver


class MyLitnerclass(models.Model):
    class Meta:
        verbose_name = 'کلاس'
        verbose_name_plural = 'کلاس ها'

    title = models.TextField(verbose_name="عنوان")
    study_field = models.CharField(max_length=100, verbose_name="رشته تحصیلی")
    cover_image = models.ImageField(upload_to='media/classes_image_cover/', null=True, validators=[validate_image_size],
                                    verbose_name="عکس کاور")
    author = models.ForeignKey(UserModel, on_delete=models.PROTECT, verbose_name="نویسنده")

    def __str__(self):
        return self.title


class LitnerModel(models.Model):
    class Meta:
        verbose_name = 'فصل'
        verbose_name_plural = 'فصل ها'

    title = models.TextField(verbose_name='عنوان')
    description = models.TextField(max_length=100, null=True)
    cover_image = models.ImageField(upload_to='media/litner_image_cover/', null=True, validators=[validate_image_size],
                                    verbose_name='عکس کاور')
    price = models.SmallIntegerField(null=True, verbose_name='قیمیت فصل')
    myclass = models.ForeignKey(MyLitnerclass, related_name='litners', on_delete=models.CASCADE,
                                verbose_name='کلاس مربوطه')
    data_created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    paid_users = models.ManyToManyField(UserModel, related_name='paid_litner', blank=True, null=True,
                                        verbose_name='دسترسی کاربران')

    @property
    def author(self):
        return self.myclass.author

    def is_paid_user(self, user):
        return self.paid_users.filter(id=user.id).exists()

    def have_karname(self, user):
        return LitnerKarNameModel.objects.filter(user=user).exists()

    def is_author(self, user):
        return user.id == self.myclass.author.id

    def __str__(self):
        return self.title


class LitnerQuestionModel(models.Model):
    class Meta:
        verbose_name = 'سوال'
        verbose_name_plural = 'سوالات'

    litner = models.ForeignKey(LitnerModel, on_delete=models.CASCADE, related_name='question', verbose_name="فصل")
    question_text = models.CharField(max_length=200, verbose_name="سوال را وارد کنید")
    answers_text = models.CharField(max_length=200, verbose_name="جواب را وارد کنید")
    hide_question = models.BooleanField(default=False)


class UserQuestionAnswerCount(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name="کاربر")
    question = models.ForeignKey(LitnerQuestionModel, related_name='user_answers', on_delete=models.CASCADE, verbose_name="سوال")
    is_correctt = models.BooleanField(default=False, null=True)
    answered_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('user', 'question')  # Ensure that each user can only have one count for each question


def current_time():
    return timezone.now()


class LitnerKarNameModel(models.Model):
    class Meta:
        verbose_name = 'کارنامه'
        verbose_name_plural = 'کارنامه ها'

    exam_id = models.OneToOneField(LitnerModel, on_delete=models.CASCADE, related_name='exam_id', verbose_name="فصل")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name="کاربر")
    completed_at = models.DateTimeField(default=current_time, null=True, blank=True, verbose_name="کامل شده در")


class LitnerAnswer(models.Model):
    karname = models.ForeignKey(LitnerKarNameModel, on_delete=models.CASCADE, related_name="litner_azmon",
                                verbose_name="کارنامه")
    question = models.ForeignKey(LitnerQuestionModel, on_delete=models.PROTECT, verbose_name="سوال")
    is_correct = models.BooleanField(default=False, verbose_name="صحیح بودن")


class LitnerKarNameDBModel(models.Model):
    question = models.ForeignKey(LitnerQuestionModel, on_delete=models.CASCADE, related_name='question_id')
    is_correct = models.BooleanField(null=True)
    karname = models.ForeignKey(LitnerKarNameModel, on_delete=models.CASCADE, related_name="karname")
    answered_at = models.DateTimeField(auto_now_add=True, null=True)
