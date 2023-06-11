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


class Payment(models.Model):
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    has_access = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    MarketHub = models.ForeignKey(MarketHubModel,on_delete=models.CASCADE)

    


class MarketHubQuestionModel(models.Model):
    markethub = models.ForeignKey(MarketHubModel, on_delete=models.CASCADE, related_name='markethub')
    question_text = models.CharField(max_length=150)
    answers_text = models.CharField(max_length=100)
