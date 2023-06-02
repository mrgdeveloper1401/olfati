from rest_framework import serializers

from markethub.models import MarketHubModel


class MarketHubSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketHubModel
        fields = "__all__"

