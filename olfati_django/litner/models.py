from django.db import models

from accounts.models import UserModel


class LitnerModel(models.Model):
    title = models.CharField(max_length=100)
    study_field = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='litner_image_cover/', null=True)
    author = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    data_created = models.DateTimeField(auto_now_add=True)


class LitnerQuestionModel(models.Model):
    litner = models.ForeignKey(LitnerModel, on_delete=models.CASCADE, related_name='litner')
    question_text = models.CharField(max_length=150)
    answers_text = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.question_text} | {self.answers_text}"


class LitnerKarNameModel(models.Model):
    litner = models.OneToOneField(LitnerModel, on_delete=models.CASCADE, related_name='karname')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

class LitnerAnswer(models.Model):
    ANSWER_TYPE = (
        ("N", "No Answer"),
        ("F", "False Answer"),
        ("T", "True Answer"),
    )

    litner_azmon = models.ForeignKey(LitnerKarNameModel, on_delete=models.PROTECT, related_name="litner_azmon")
    answer = models.ForeignKey(LitnerQuestionModel, on_delete=models.PROTECT, )
    type = models.CharField(max_length=1, choices=ANSWER_TYPE)
