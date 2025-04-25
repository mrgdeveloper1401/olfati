from rest_framework import viewsets, permissions

from utils.vlaidations import CommonPagination
from . import serializers
from . import models


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ImageSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CommonPagination

    def get_queryset(self):
        return models.Image.objects.defer("is_deleted", "deleted_at").filter(
            user=self.request.user
        )
