from rest_framework import serializers, generics, exceptions

from . import models


class LinterSerializer(serializers.ModelSerializer):
    is_author_season_class = serializers.SerializerMethodField()
    author_full_name = serializers.SerializerMethodField()
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
        return obj.cover_image.url

    def get_is_paid(self, obj):
        return obj.paid_users == self.context['request'].user


class MyLinterClassSerializer(serializers.ModelSerializer):
    litners = LinterSerializer(many=True, read_only=True)
    author_full_name = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()
    is_author_create_class = serializers.SerializerMethodField()

    class Meta:
        model = models.MyLinterClass
        exclude = ("is_deleted", "deleted_at", "created_by")
        read_only_fields = ("author",)

    def get_author_full_name(self, obj):
        return obj.author.get_full_name() if obj.author.get_full_name else None

    def get_cover_image_url(self, obj):
        return obj.cover_image.url

    def get_is_author_create_class(self, obj):
        return obj.author == self.context['request'].user

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
