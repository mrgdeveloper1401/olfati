from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _



def validate_image_size(value):
    size = 2
    # Set the maximum allowed size (in bytes), for example, 2 MB
    max_size = size * 1024 * 1024

    if value.size > max_size:
        raise ValidationError(f'محدودیت سایز تا حداکثر {size} مگابایت')


class CommonPagination(PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'data': data,
        })


class PhoneValidator(RegexValidator):
    regex = r'^\d{11}$'
    message = _("enter a valid phone number, and phone number must be 11 character")
