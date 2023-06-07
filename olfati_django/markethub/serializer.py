from markethub.models import MarketHubModel, MarketHubQuestionModel
from rest_framework import serializers


# اگه پرداخت نکرده بود
class MarketHubSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketHubModel
        fields = "__all__"


class MarketHubQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketHubQuestionModel
        fields = "__all__"


# اگه پرداخت کرده بود
class MarketHubPaidSerializer(serializers.ModelSerializer):
    markethub_question = MarketHubQuestionSerializer(many=True)

    class Meta:
        model = MarketHubModel
        fields = ('title', "data_created", 'cover_image', "markethub_question",)
