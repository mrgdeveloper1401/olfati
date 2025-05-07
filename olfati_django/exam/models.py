from django.db import models
from accounts.models import UserModel
from django.utils.translation import gettext_lazy as _

from utils.vlaidations import validate_image_size


class MyExamClass(models.Model):
    class Meta:
        verbose_name = _('کلاس')
        verbose_name_plural = _('کلاس ها')

    title = models.TextField(verbose_name=_('عنوان'))
    study_field = models.CharField(max_length=100, verbose_name=_('فیلد مطالعه'))
    cover_image = models.ImageField(upload_to='media/classes_image_cover/', null=True, validators=[validate_image_size],
                                    verbose_name=_('عکس کاور'))
    author= models.ForeignKey(UserModel, on_delete=models.PROTECT, verbose_name=_('نویسنده'))

    def __str__(self):
        return self.title



class ExamModel(models.Model):
    class Meta:
        verbose_name = _('فصل')
        verbose_name_plural = _('فصل ها')


    title = models.TextField(verbose_name=_('عنوان'))
    cover_image = models.ImageField(upload_to='media/exam_image_cover/', validators=[validate_image_size],
                                    verbose_name=_('عکس کاور'))
    data_created = models.DateTimeField(auto_now_add=True, verbose_name=_('زمان ایجاد'))
    myclass = models.ForeignKey(MyExamClass, related_name='exams', on_delete=models.CASCADE, verbose_name=_('کلاس'))

    def __str__(self):
        return self.title[:20]

    def have_karname(self, user):
        return KarNameModel.objects.filter(user=user).exists()


class QuestionModel(models.Model):
    class Meta:
        verbose_name = _('سوال')
        verbose_name_plural = _('سوالات')

    exam = models.ForeignKey(ExamModel, on_delete=models.CASCADE, related_name='questions', verbose_name=_('امتحان'))
    question_text = models.TextField(verbose_name=_('متن سوال'))

    def __str__(self):
        return f"{self.question_text[:25]}"


class ChoiceModel(models.Model):
    class Meta:
        verbose_name = _('گزینه')
        verbose_name_plural = _('گزینه ها')

    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, related_name='choices',
                                 verbose_name=_('سوال'))
    choice_text = models.TextField(verbose_name=_('متن انتخاب'))
    is_correct = models.BooleanField(default=False, verbose_name=_('صحیح بون'))

    def __str__(self):
        return f"{self.question.question_text[:25]} | {self.choice_text[:20]}"


class KarNameModel(models.Model):
    class Meta:
        verbose_name = _('کارنامه')
        verbose_name_plural = _('کارنامه ها')

    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, verbose_name=_('کاربر'))
    exam_id = models.ForeignKey(ExamModel, on_delete=models.PROTECT, related_name="exam_id", verbose_name=_('امتحان'))


class KarNameDBModel(models.Model):
    question = models.ForeignKey(QuestionModel, on_delete=models.PROTECT, related_name="question_id",
                                 verbose_name=_('سوال'))
    choice = models.ForeignKey(ChoiceModel, on_delete=models.PROTECT, related_name="choice_id", null=True,
                               verbose_name=_('انتخاب'))
    karname = models.ForeignKey(KarNameModel, on_delete=models.PROTECT, related_name="karname",
                                verbose_name=_('کارنامه'))
