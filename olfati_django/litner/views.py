from django.db.models import Q
from rest_framework import status, permissions, viewsets, mixins, generics, decorators, response, views
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializer, models

import logging

from utils.vlaidations import CommonPagination
from .models import LinterModel
from .permissions import IsOwnerOrReadOnlyLinterModel, IsOwnerOrReadOnlyLinterClass

logger = logging.getLogger(__name__)
permission_error = Response({'اجازه این کار را ندارید.'}, status.HTTP_403_FORBIDDEN)


class LinterClassViewSet(viewsets.ModelViewSet):
    """
    for filter query set you should authenticate, and you can use this
    ?is_owner=1 --> List of created classes

    کلاس های لاینتر
    """
    serializer_class = serializer.MyLinterClassSerializer
    queryset = models.MyLinterClass.objects.select_related(
        "author"
    ).only(
        "author__first_name", "author__last_name", "title", "study_field", "cover_image", "created_at",
        "updated_at",
    )
    # pagination_class = CommonPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnlyLinterClass,)

    def filter_queryset(self, queryset):
        is_owner = self.request.query_params.get("is_owner", None)

        if (is_owner == "1" or is_owner == 1) and self.request.user.is_authenticated :
            return queryset.filter(author=self.request.user)
        return queryset


class AdminListLinterClassViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    کلاس های لاینتر که توسط کاربر با سطح دسترسی ادمین ایجاد شده
    """
    serializer_class = serializer.MyLinterClassSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_queryset(self):
        return models.MyLinterClass.objects.select_related(
        "author"
    ).only(
        "author__first_name", "author__last_name", "title", "study_field", "cover_image", "created_at",
        "updated_at",
    ).filter(author__is_staff=True)


class AdminListLinterSeasonViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    فصل های هر کلاس با سطح دسترسی ادمین
    یعنی اون فصل هایی که توسط ادمین ایجاد شده هست
    یا توسطه موسسه
    """
    serializer_class = serializer.LinterSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_queryset(self):
        return LinterModel.objects.filter(
            myclass_id=self.kwargs['admin_linter_class_pk'],
            myclass__author__is_staff=True,
        )


class LinterSeasonViewSet(viewsets.ModelViewSet):
    """
    فصل های هر کلاس
    """
    # pagination_class = CommonPagination
    serializer_class = serializer.LinterSerializer
    permission_classes = (IsOwnerOrReadOnlyLinterModel,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['linter_class_pk'] = self.kwargs["class_pk"]
        return context

    def get_queryset(self):
        return models.LinterModel.objects.filter(
            myclass_id=self.kwargs['class_pk'],
        ).only(
        "title", "price", 'description', 'created_at', "myclass__author__phone_number", "cover_image",
            "created_at", "updated_at", "myclass__author__first_name", "myclass__author__last_name", "is_sale"
    ).select_related("myclass__author",)


class SaleLinterSeasonViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    فصل هایی که قابل فروش هستند
    """
    serializer_class = serializer.LinterSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return models.LinterModel.objects.filter(is_sale=True, myclass_id=self.kwargs['class_pk']).only(
        "title", "price", 'description', 'created_at', "myclass__author__phone_number", "created_at",
            "cover_image", "updated_at", "myclass__author__first_name",
            "myclass__author__last_name", "is_sale"
        ).select_related("myclass__author",)


class LinterBoxViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    باکس های یک فصل
    """
    def get_queryset(self):
        return models.LeitnerBox.objects.filter(
            linter_id=self.kwargs['season_pk'],
            linter__myclass_id=self.kwargs['class_pk']
        ).filter(
            Q(linter__myclass__author=self.request.user) | Q(linter__paid_users=self.request.user)
        ).only("box_number",)
    serializer_class = serializer.UserLinterBoxSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CreateLinterFlashCartViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializer.CreateFlashCartSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return models.LinterFlashCart.objects.only(
            "question_text", "answers_text", "box", "season__title"
        ).select_related("season").filter(
            season__paid_users=self.request.user
        )


class LinterFlashCartViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    فلش کارت ها
    for search you can use
    ?box=(range 1 to 5)
    """
    serializer_class = serializer.LinterFlashCartSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return models.LinterFlashCart.objects.only(
            "question_text", "answers_text", "box", "season__title"
        ).select_related("season").filter(
            season__paid_users=self.request.user,
            season_id=self.kwargs['season_pk'],
        )

    def filter_queryset(self, queryset):
        box = self.request.query_params.get("box", None)

        if box:
            return queryset.filter(box=box)
        else:
            return queryset


class LinterUserAnswerView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    """
    ارسال جواب های کاربران از فلش کارت
    """
    serializer_class = serializer.CreateLinterUserAnswerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return models.UserAnswer.objects.only(
            "user__phone_number",
            "flash_cart__question_text",
            "is_correct",
            "created_at"
        ).select_related("user", "flash_cart").filter(user=self.request.user)
