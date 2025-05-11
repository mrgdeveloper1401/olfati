from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers, generics, exceptions

from . import models
from .models import LinterFlashCart, LinterModel, UserAnswer, UserLinterFlashCart


class LinterSerializer(serializers.ModelSerializer):
    is_author_season_class = serializers.SerializerMethodField()
    author_full_name = serializers.SerializerMethodField()
    is_paid = serializers.SerializerMethodField()
    paid_users_count = serializers.SerializerMethodField()

    class Meta:
        model = models.LinterModel
        exclude = ("is_deleted", "deleted_at", "paid_users", "myclass")

    @extend_schema_field(serializers.BooleanField())
    def get_is_author_season_class(self, obj):
        return obj.myclass.author_id == self.context['request'].user.id

    def create(self, validated_data):
        linter_class = self.context['linter_class_pk']
        return models.LinterModel.objects.create(myclass_id=linter_class, **validated_data)

    def get_author_full_name(self, obj):
        return obj.myclass.author.get_full_name()

    def get_cover_image_url(self, obj):
        return obj.cover_image.url

    @extend_schema_field(serializers.BooleanField())
    def get_is_paid(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.paid_users.filter(id=request.user.id).exists()
        return False

    @extend_schema_field(serializers.IntegerField())
    def get_paid_users_count(self, obj):
        return obj.paid_users.count()


class MyLinterClassSerializer(serializers.ModelSerializer):
    author_full_name = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()
    is_author_create_class = serializers.SerializerMethodField()

    class Meta:
        model = models.MyLinterClass
        exclude = ("is_deleted", "deleted_at",)
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
            generics.get_object_or_404(models.LinterModel, id=self.context['linter_season_pk'])
        except models.LinterModel.DoesNotExist as e:
            raise e
        return attrs


class UserLinterBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LeitnerBox
        fields = ("id", "box_number")


class FieldLinterFlashCartSerializer(serializers.Serializer):
    question_text = serializers.CharField()
    answers_text = serializers.CharField()
    season = serializers.PrimaryKeyRelatedField(
        queryset=LinterModel.objects.only("title")
    )


class CreateFlashCartSerializer(serializers.Serializer):
    cart = FieldLinterFlashCartSerializer(many=True)

    def create(self, validated_data):
        cart = validated_data.get("cart")

        if not cart:
            raise exceptions.ValidationError("cart must have data")

        lst = [
            models.LinterFlashCart(
                question_text=i.get("question_text"),
                answers_text=i.get("answers_text"),
                season=i.get("season"),
            )
            for i in validated_data.get("cart", None)
        ]
        if lst:
            created = models.LinterFlashCart.objects.bulk_create(lst)
            return {"cart": created}
        return []


class LinterFlashCartSerializer(serializers.ModelSerializer):
    season_title = serializers.SerializerMethodField()

    class Meta:
        model = models.LinterFlashCart
        fields = ("id", "question_text", "answers_text", "season", "season_title")

    def get_season_title(self, obj):
        return obj.season.title


class LinterUserAnswerSerializer(serializers.Serializer):
    flash_cart = serializers.PrimaryKeyRelatedField(
        queryset=UserLinterFlashCart.objects.only("id")
    )
    is_correct = serializers.BooleanField(allow_null=True)


class CreateLinterUserAnswerSerializer(serializers.Serializer):
    answer = LinterUserAnswerSerializer(many=True)

    def update_flashcard_boxes(self, user_answers):
        flash_cart_list = []
        for i in user_answers:
            cart = i.flash_cart
            if i.is_correct:
                cart.box = min(cart.box + 1, 6)
            else:
                if cart.box != 6:
                    cart.box = 1
            flash_cart_list.append(cart)
        UserLinterFlashCart.objects.bulk_update(flash_cart_list, ["box"])

    def create(self, validated_data):
        answer = validated_data.get("answer")

        if not answer:
            raise serializers.ValidationError({"message": "answer must have data"})
        lst = [
            UserAnswer(
                user=self.context['request'].user,
                flash_cart=i["flash_cart"],
                is_correct=i["is_correct"],
            )
            for i in answer
        ]

        if lst:
            UserAnswer.objects.bulk_create(lst)
            self.update_flashcard_boxes(lst)

        return {"answer": lst}


class LinterUserFlashCartSerializer(serializers.ModelSerializer):
    question_text = serializers.SerializerMethodField()
    answers_text = serializers.SerializerMethodField()
    season_title = serializers.SerializerMethodField()
    season = serializers.SerializerMethodField()

    class Meta:
        model = UserLinterFlashCart
        fields = ("id", "box", "question_text", "answers_text", "season_title", "season")

    def get_question_text(self, obj):
        return str(obj.flash_cart.question_text)

    def get_answers_text(self, obj):
        return str(obj.flash_cart.answers_text)

    def get_season_title(self, obj):
        return str(obj.flash_cart.season.title)

    def get_season(self, obj):
        return str(obj.flash_cart.season)
