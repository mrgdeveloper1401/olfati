from django.db import models

from accounts.models import UserModel


class MarketHubModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='litner_image_cover/', null=True)
    author = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    price = models.SmallIntegerField()
    data_created = models.DateTimeField(auto_now_add=True)
    paid_users = models.ManyToManyField(UserModel, related_name='paid_market_hubs', blank=True)

    def is_paid_user(self, user):
        return self.paid_users.filter(id=user.id).exists()


class MarketHubQuestionModel(models.Model):
    litner = models.ForeignKey(MarketHubModel, on_delete=models.CASCADE, related_name='litner')
    question_text = models.CharField(max_length=150)
    answers_text = models.CharField(max_length=100)
