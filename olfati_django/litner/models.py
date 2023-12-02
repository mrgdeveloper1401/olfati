from django.db import models
from accounts.models import UserModel

from utils.vlaidations import validate_image_size


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
    cover_image = models.ImageField(upload_to='media/litner_image_cover/', null=True, validators=[validate_image_size],
                                    verbose_name='عکس کاور')
    data_created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    myclass = models.ForeignKey(MyLitnerclass, related_name='litners', on_delete=models.CASCADE, verbose_name='کلاس')

    def have_karname(self, user):
        return LitnerKarNameModel.objects.filter(user=user).exists()

    def __str__(self):
        return self.title


class LitnerQuestionModel(models.Model):
    class Meta:
        verbose_name = 'سوال'
        verbose_name_plural = 'سوالات'

    litner = models.ForeignKey(LitnerModel, on_delete=models.CASCADE, related_name='litner', verbose_name="فصل")
    question_text = models.TextField(verbose_name="سوال را وارد کنید")
    answers_text = models.TextField(verbose_name="جواب را وارد کنید")

    def __str__(self):
        return f"{self.question_text} | {self.answers_text}"


class LitnerKarNameModel(models.Model):
    class Meta:
        verbose_name = 'کارنامه'
        verbose_name_plural = 'کارنامه ها'

    exam_id = models.OneToOneField(LitnerModel, on_delete=models.CASCADE, related_name='exam_id', verbose_name="فصل")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name="کاربر")


class LitnerAnswer(models.Model):
    karname = models.ForeignKey(LitnerKarNameModel, on_delete=models.PROTECT, related_name="litner_azmon", verbose_name="کارنامه")
    question = models.ForeignKey(LitnerQuestionModel, on_delete=models.PROTECT, verbose_name="سوال")
    is_correct = models.BooleanField(default=False, verbose_name="صحیح بودن")


class LitnerKarNameDBModel(models.Model):
    question = models.ForeignKey(LitnerQuestionModel, on_delete=models.PROTECT, related_name='question_id')
    is_correct = models.BooleanField(null=True)
    karname = models.ForeignKey(LitnerKarNameModel, on_delete=models.PROTECT, related_name="karname")
