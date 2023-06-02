from rest_framework import serializers

from litner.models import LitnerModel, LitnerQuestionModel, LitnerKarNameModel


class LitnerQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LitnerQuestionModel
        fields = ('id', 'question_text', 'answers_text',)


class LitnerSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = LitnerModel
        fields = "__all__"


class LitnerDetailSerializer(serializers.ModelSerializer):
    litner = LitnerQuestionSerializer(many=True)

    class Meta:
        model = LitnerModel
        fields = ("id", "title", "study_field", "author", "cover_image", "data_created", "litner",)

    def create(self, validated_data):
        questions_data = validated_data.pop('litner', [])
        litner = LitnerModel.objects.create(**validated_data)
        for question in questions_data:
            print(question)
            LitnerQuestionModel.objects.create(litner=litner, **question)
        return litner


class LitnerKarNameSerializer(serializers.ModelSerializer):
    # false_answer = serializers.StringRelatedField()
    # true_answer = serializers.StringRelatedField()
    # no_answer = serializers.StringRelatedField()

    class Meta:
        model = LitnerKarNameModel
        fields = ("false_answer", "true_answer", "no_answer",)
#
