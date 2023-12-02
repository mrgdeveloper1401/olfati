from django.db import models
from accounts.models import UserModel



class Myclass(models.Model):
    title = models.CharField(max_length=100)
    study_field = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='media/classes_image_cover/', null=True)
    author= models.ForeignKey(UserModel, on_delete=models.PROTECT)
    

class MarketHubModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='media/markethub_image_cover/', null=True)
    price = models.SmallIntegerField()
    myclass = models.ForeignKey(Myclass, related_name='markethubs', on_delete=models.CASCADE)
    data_created = models.DateTimeField(auto_now_add=True)
    paid_users = models.ManyToManyField(UserModel, related_name='paid_market_hubs', blank=True)

    @property
    def author (self):
        return self.myclass.author

    def is_paid_user(self, user):
        return self.paid_users.filter(id=user.id).exists()
    
    def is_author(self, user):
        return user.id == self.myclass.author.id
    
    #امتحان داده
    def have_karname(self, user):
        return MarketHubKarNameModel.objects.filter(user=user).exists()


class MarketHubQuestionModel(models.Model):
    markethub = models.ForeignKey(MarketHubModel, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=150)
    answers_text = models.CharField(max_length=100)


class MarketHubKarNameModel(models.Model):
    exam_id = models.OneToOneField(MarketHubModel, on_delete=models.CASCADE, related_name='exam_id')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, )
    

class MarketHubAnswer(models.Model):
    karname = models.ForeignKey(MarketHubKarNameModel, on_delete=models.PROTECT, related_name="litner_azmon")
    question = models.ForeignKey(MarketHubQuestionModel, on_delete=models.PROTECT, )
    is_correct = models.BooleanField(default=False)


class MarketHubKarNameDBModel(models.Model):
    question = models.ForeignKey(MarketHubQuestionModel, on_delete=models.PROTECT, related_name='question_id')
    is_correct = models.BooleanField(null=True)
    karname = models.ForeignKey(MarketHubKarNameModel, on_delete=models.PROTECT, related_name="karname")







