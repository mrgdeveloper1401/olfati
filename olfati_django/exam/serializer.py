from rest_framework import serializers

from .models import ExamModel, ChoiceModel, QuestionModel, KarNameModel, KarNameDBModel


class KarNameDBlSerializer(serializers.ModelSerializer):
    class Meta:
        model = KarNameDBModel
        fields = "__all__"


class KarNameSerializer(serializers.ModelSerializer):
    questions = KarNameDBlSerializer(many=True)

    class Meta:
        model = KarNameModel
        fields = ( "exam_id", "questions",)


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceModel
        fields = ('id', 'choice_text', 'is_correct',)


class ExamQuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = QuestionModel
        fields = ('id', 'question_text', 'choices')


class ExamDetailsSerializer(serializers.ModelSerializer):
    questions = ExamQuestionSerializer(many=True)

    class Meta:
        model = ExamModel
        fields = ('author', 'id', 'title', 'study_field', 'questions', 'data_created')

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        exam = ExamModel.objects.create(**validated_data)

        for question_data in questions_data:
            choices_data = question_data.pop('choices', [])
            question = QuestionModel.objects.create(exam=exam, **question_data)
            for choice_data in choices_data:
                choice = ChoiceModel.objects.create(question=question, **choice_data)

        return exam

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', [])
        # Update Exam fields
        instance.title = validated_data.get('title', instance.title)
        instance.study_field = validated_data.get('study_field', instance.study_field)
        instance.save()
        return instance


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamModel
        fields = "__all__"
