from rest_framework import serializers, generics, exceptions

from catalog_app.models import Image
from . import models
# from accounts.serializer import UserSerializers


# class LitnerAwnsereserilizer(serializers.ModelSerializer):
#     class Meta:
#         model = LitnerAnswer
#         fields = ('is_correct',)


# class UserQuestionAnswerCountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserQuestionAnswerCount
#         fields = ['id', 'user', 'question', 'is_hide', 'is_correct']
#
#     def create(self, validated_data):
#         return UserQuestionAnswerCount.objects.create(*validated_data)


# class LitnerQuestionSerializer(serializers.ModelSerializer):
#     correct_answer_count = UserQuestionAnswerCountSerializer(read_only=True, many=True)
#
#     class Meta:
#         model = LitnerQuestionModel
#         fields = ('id', 'question_text', 'answers_text', 'litner', 'hide_question', 'correct_answer_count')
#         extra_kwargs = {'id': {'read_only': False, 'required': False}}
#
#     def create(self, validated_data):
#         validated_data.pop('id', None)
#         return super().create(validated_data)
#
#     def update(self, instance, validated_data):
#         validated_data.pop('id', None)
#         return super().update(instance, validated_data)
#
#     def get_visible_question(self, obj):
#         user = self.context.get['request'].user
#         visible_questions = obj.question.filter(userquestionanswercount__user=user,
#                                                 userquestionanswercount__correct_answer_count__lt=6)
#         return UserQuestionAnswerCountSerializer(visible_questions, many=True).data
#
#     def get_serialized(self, obj):
#         question_to_display = self.context.get("question_to_display", None)
#         if question_to_display:
#             return LitnerQuestionSerializer(question_to_display, many=True).data
        # else:
        #    return LitnerQuestionSerializer(obj.question.filter(hide_question=False),many=True).data


class LinterSerializer(serializers.ModelSerializer):
    # have_karname = serializers.SerializerMethodField(read_only=True)
    is_author_season_class = serializers.SerializerMethodField()
    cover_image = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects.only("title"),
    )
    author_full_name = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()
    is_paid = serializers.SerializerMethodField()

    class Meta:
        model = models.LinterModel
        exclude = ("is_deleted", "deleted_at", "paid_users", "myclass")

    def get_is_author_season_class(self, obj):
        return obj.myclass.author_id == self.context['request'].user.id

    def create(self, validated_data):
        linter_class = self.context['linter_class_pk']
        return models.LinterModel.objects.create(myclass_id=linter_class, **validated_data)

    def get_author_full_name(self, obj):
        return obj.myclass.author.get_full_name()

    def get_cover_image_url(self, obj):
        return obj.cover_image.image_url

    def get_is_paid(self, obj):
        return obj.paid_users == self.context['request'].user

    def validate(self, attrs):
        user = self.context['request'].user
        linter_class = self.context['linter_class_pk']
        linter_class = models.MyLinterClass.objects.filter(author=user, id=linter_class).only(
            "id",
            "author__phone_number",
        )

        if not linter_class:
            raise exceptions.PermissionDenied()
        else:
            get_image = attrs.get('cover_image')

            if get_image:
                user_image = Image.objects.filter(user=self.context['request'].user).only("title")
                if not user_image:
                    raise exceptions.ValidationError({"cover_image": "image not found"})
        return attrs


class MyLinterClassSerializer(serializers.ModelSerializer):
    litners = LinterSerializer(many=True, read_only=True)
    author_full_name = serializers.SerializerMethodField()
    cover_image = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects.only('title')
    )
    cover_image_url = serializers.SerializerMethodField()
    is_author_create_class = serializers.SerializerMethodField()

    class Meta:
        model = models.MyLinterClass
        exclude = ("is_deleted", "deleted_at", "created_by")
        read_only_fields = ("author",)

    def get_author_full_name(self, obj):
        return obj.author.get_full_name() if obj.author.get_full_name else None

    def get_cover_image_url(self, obj):
        return obj.cover_image.image_url

    def get_is_author_create_class(self, obj):
        return obj.author == self.context['request'].user

    # def to_representation(self, instance):
    #     request = self.context.get("request")
    #     rep = super().to_representation(instance)
    #     if not request.parser_context.get("kwargs").get("pk"):
    #         rep.pop("litners", None)
    #     return rep

    def validate(self, attrs):
        get_image = attrs.get('cover_image')

        if get_image:
            user_image = Image.objects.filter(user=self.context['request'].user).only("title")

            if not user_image:
                raise exceptions.ValidationError({"cover_image": "image not found"})

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        return models.MyLinterClass.objects.create(
            author=user,
            **validated_data
        )


class AdminLinterBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LeitnerBox
        fields = '__all__'
        read_only_fields = ("linter",)

    def create(self, validated_data):
        linter_season_pk = self.context['linter_season_pk']
        return models.LeitnerBox.objects.create(linter_id=linter_season_pk, **validated_data)

    def validate(self, attrs):
        try:
            generics.get_object_or_404(models.LitnerModel, id=self.context['linter_season_pk'])
        except models.LitnerModel.DoesNotExist as e:
            raise e
        return attrs


class UserLinterBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LeitnerBox
        fields = ("id", "box_number")


class LinterFlashCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LinterFlashCart
        fields = ("id", "question_text", "answers_text", "box", "get_box_number")
        read_only_fields = ("box",)

    def create(self, validated_data):
        linter_box_pk = self.context['linter_box_pk']
        return models.LinterFlashCart.objects.create(box_id=linter_box_pk, **validated_data)

    def validate(self, attrs):
        try:
            generics.get_object_or_404(models.LeitnerBox, id=self.context['linter_box_pk'])
        except models.LinterFlashCart.DoesNotExist as e:
            raise e
        return attrs


class LinterUserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserAnswer
        fields = ("id", "box", "box_number", "answer_text", "status")
