from .models import MarketHubModel, MarketHubQuestionModel
from rest_framework import serializers


# اگه پرداخت نکرده بود
class MarketHubSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketHubModel
        fields = ( 'title','description','cover_image', 'author', 'price','data_created')


class MarketHubQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketHubQuestionModel
        fields = "__all__"


# اگه پرداخت کرده بود


class MarketHubPaidSerializer(serializers.ModelSerializer):
    question = MarketHubQuestionSerializer(many=True,read_only=True)
    cover_image = serializers.ImageField(source="markethub.cover_image")
    title = serializers.CharField(source="markethub.title")
    description = serializers.CharField(source="markethub.description")
    class Meta:
        model =MarketHubQuestionModel
        fields ='__all__'



