from rest_framework import serializers
from markethub.models import MarketHubModel,MarketHubQuestionModel


class MarketHubSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketHubModel
        fields = "__all__"



class MarketHubQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketHubQuestionModel
        fields = "__all__"

