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
        return obj.author.get_full_name()

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


# class UserQuestionAnswerCountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserQuestionAnswerCount
#         fields = ['id', 'user', 'question', 'correct_answer_count']
#
#     def create(self, validated_data):
#         return UserQuestionAnswerCount.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.correct_answer_count = validated_data.get('correct_answer_count', instance.correct_answer_count)
#         instance.save()
#         return instance


# class LitnerDetailSerializer(serializers.ModelSerializer):
    # question = serializers.SerializerMethodField()
    # have_karname = serializers.SerializerMethodField(read_only=True)
    # is_paid = serializers.SerializerMethodField(read_only=True)
    # author = serializers.SlugRelatedField(slug_field="get_full_name", read_only=True)
    # is_author = serializers.SerializerMethodField(read_only=True)

    # class Meta:
    #     model = LitnerModel
    #     fields = ("id", "title", "description", "cover_image", "price", "data_created", "author", "is_paid",
    #               "is_author")

    # def get_is_paid(self, obj):
    #     request = self.context.get("request")
    #     return obj.is_paid_user(request.user) or obj.is_author(request.user)

    # def get_have_karname(self, obj):
    #     request = self.context.get("request")
    #     return obj.have_karname(request.user)

    # def get_question(self, obj):
    #     questions_to_display = self.context.get("questions_to_display", None)
    #     if questions_to_display:
    #         return LitnerQuestionSerializer(questions_to_display, many=True).data

    # def get_is_author(self, obj):
    #     request = self.context.get("request")
    #     return obj.is_author(request.user)

    # def create(self, validated_data):
    #     myclass_id = self.context['class_list_pk']
    #     return LitnerModel.objects.create(myclass_id=myclass_id, **validated_data)
        # request = self.context.get("request")
        # if not myclass.author == request.user:
        #     return PermissionError("اجازه اینکار را ندارید")
        # questions_data = validated_data.pop('questions', [])
        # litner = LitnerModel.objects.create(**validated_data)
        # for question in questions_data:
        #     question.pop('id', None)
        #     LitnerQuestionModel.objects.create(**question, litner=litner)
        #     return litner

    # def update(self, instance, validated_data):
    #     request = self.context.get("request")
    #     myclass = validated_data.get('myclass', None)
    #     questions_data = validated_data.pop('questions', [])
    #     for question in questions_data:
    #         question_id = question.get('id', None)
    #         if question_id:
    #             try:
    #                 questionmodel = instance.questions.get(id=question_id)
    #                 for attr, value in question.items():
    #                     setattr(questionmodel, attr, value)
    #                 questionmodel.save()
    #             except:
    #                 pass
    #         else:
    #             LitnerQuestionModel.objects.create(**question, litner=instance)
    #     if myclass:
    #         if not myclass.author == request.user:
    #             return PermissionError
    #         return super().update(instance, validated_data)
    # 

# class LitnerKarnameDBSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LitnerKarNameDBModel
#         fields = ('question', 'is_correct')


# class LitnerKarNameSerializer(serializers.ModelSerializer):
#     user = UserSerializers()
#     exam_id = LitnerDetailSerializer()
#
#     class Meta:
#         model = LitnerKarNameModel
#         fields = '__all__'


# class LitnerTakeExamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LitnerKarNameDBModel
#         fields = '__all__'
#
#     def create(self, validated_data):
#         """
#         Create LitnerKarNameDBModel using validated data, making sure to handle karname as pk.
#         """
#         karname_id = validated_data.get('karname')  # karname should be the pk here
#         question = validated_data.get('question')
#         is_correct = validated_data.get('is_correct')
#
#         # Create the LitnerKarNameDBModel object with karname_id
#         litner_karname_db, created = LitnerKarNameDBModel.objects.get_or_create(
#             karname_id=karname_id.id,  # Pass karname_id directly (foreign key)
#             question=question,
#             is_correct=is_correct
#         )
#         return litner_karname_db
#
#
#     def update(self, instance, validated_data):
#         karname = instance
#         for question_and_choice in validated_data['karname']:
#             question = question_and_choice['question']
#             if question.litner != karname.exam_id:
#                 continue
#             is_correct = question_and_choice['is_correct']
#             answered = LitnerKarNameDBModel.objects.get(question=question, karname=karname)
#             answered.is_correct = is_correct
#             answered.save()
#         return karname


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
