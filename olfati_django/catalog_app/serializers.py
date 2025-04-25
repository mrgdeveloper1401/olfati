from rest_framework import serializers

from . import models


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        exclude = ("is_deleted", "deleted_at", "user")

    def create(self, validated_data):
        user = self.context['request'].user
        return models.Image.objects.create(user=user, **validated_data)
