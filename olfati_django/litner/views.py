from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from litner.models import LitnerModel, LitnerKarNameModel, LitnerKarNameDBModel, MyLitnerclass, LitnerQuestionModel, \
    UserQuestionAnswerCount
from litner.notification import schedule_notification
from litner.serializer import LitnerSerializer, LitnerDetailSerializer, LitnerTakeExamSerializer, \
    MyLitnerClassSerializer
from rest_framework import generics
from django.utils import timezone
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

import logging

from .tasks import send_notification_task

logger = logging.getLogger(__name__)
permission_error = Response({'اجازه این کار را ندارید.'}, status.HTTP_403_FORBIDDEN)


class ListCreateMyClassView(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = MyLitnerClassSerializer
    queryset = MyLitnerclass.objects.all()

    def get_serializer_class(self):
        return MyLitnerClassSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data.get('litners', None)
        return Response({"data": data})

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_author(request.user):
            return permission_error
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_author(request.user):
            return permission_error
        return super().destroy(request, *args, **kwargs)


class LitnerListView(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = LitnerModel.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return LitnerSerializer
        else:
            return LitnerDetailSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            print('here is test')
            queryset = LitnerModel.objects.filter(myclass=self.kwargs.get('pk', None))
            print('here is test 2')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_author(request.user):
            return permission_error
        return super().partial_update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not (instance.is_author(request.user) or instance.is_paid_user(request.user)):
            return permission_error

        try:
            karname = LitnerKarNameModel.objects.get(user=request.user, exam_id=instance)
        except LitnerKarNameModel.DoesNotExist:
            questions_to_display = LitnerQuestionModel.objects.filter(litner=instance)
        else:
            if timezone.now() < karname.completed_at + timedelta(hours=24):
                return Response({'message': 'you cant take another exam'}, status.HTTP_403_FORBIDDEN)

            if timezone.now() >= karname.completed_at + timedelta(days=3):
                questions_to_display = LitnerQuestionModel.objects.filter(litner=instance)
            else:
                questions_to_display = LitnerQuestionModel.objects.filter(
                    Q(user_answers__isnull=True) | Q(user_answers__is_correctt__isnull=True) |
                    Q(user_answers__is_correctt=False), litner=instance
                )

        serializer = self.get_serializer(instance,
                                         context={'request': request, 'questions_to_display': questions_to_display})
        data = serializer.data.get('question')
        return Response({'data': data})


class LitnerView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        data = LitnerDetailSerializer(data=request.data, context={'request': request})
        data.is_valid(raise_exception=True)
        data.save()
        return Response(data.data)

    def delete(self, request, pk):
        try:
            instance = LitnerModel.objects.get(pk=pk)
            instance.delete()
            return Response({"massage": "litner remove successfully"}, status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(
                {"massage": "litner not found"}, status.HTTP_404_NOT_FOUND)

    def put(self, request):
        pass


class LitnerTakingExam(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is None:
            try:
                litners = LitnerModel.objects.all()
                serializer = LitnerSerializer(litners, many=True, context={'request': request})
                return Response({'data': serializer.data}, status.HTTP_200_OK)
            except Exception as exc:
                logger.error(f"Error in LitnerTakingExam (GET all): {exc}")
                return Response({'message': str(exc)}, status.HTTP_404_NOT_FOUND)
        else:
            try:
                litner = LitnerModel.objects.get(myclass_id=pk, paid_users=self.request.user)
                karname = LitnerKarNameModel.objects.get(user=request.user, exam_id=litner)
                time_elapsed = timezone.now() - karname.completed_at

                if time_elapsed < timedelta(days=3):  # If less than 3 days, restrict access based on answer status
                    user_answers = UserQuestionAnswerCount.objects.filter(user=request.user,
                                                                          question__in=litner.question.all())

                    if user_answers.filter(is_correctt=False).exists():
                        # Show only wrong answers
                        wrong_questions = user_answers.filter(is_correctt=False).values_list('question', flat=True)
                        questions_to_display = LitnerQuestionModel.objects.filter(id__in=wrong_questions)
                    else:
                        # All answers correct, restrict access completely
                        return Response({'message': 'You cannot access the exam for 3 days.'},
                                        status.HTTP_403_FORBIDDEN)
                else:
                    # After 3 days, show all questions again
                    questions_to_display = LitnerQuestionModel.objects.filter(litner=litner)

                serializer = LitnerDetailSerializer(litner, context={'request': request, 'exam': pk,
                                                                     'questions_to_display': questions_to_display})
                return Response({'data': serializer.data}, status.HTTP_200_OK)

            except LitnerModel.DoesNotExist:
                return Response({'message': 'Litner not found'}, status.HTTP_404_NOT_FOUND)
            except LitnerKarNameModel.DoesNotExist:
                return Response({'message': 'Karname not found'}, status.HTTP_404_NOT_FOUND)
            except Exception as exc:
                logger.error(f"Error in LitnerTakingExam (GET with pk): {exc}")
                return Response({'message': f'An error occurred: {exc}'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, pk):
        exam = get_object_or_404(LitnerModel, pk=pk)
        fcm_token = request.data['fcm_token']
        answers = request.data['answers']
        send_notification_in_3_days = False

        try:
            # Check if karname exists or create one
            test = LitnerKarNameModel.objects.filter(user=request.user, exam_id=exam).exists()

            if not test:
                karname = LitnerKarNameModel.objects.create(user=request.user, exam_id=exam)
                send_notification_in_3_days = True
            else:
                karname = LitnerKarNameModel.objects.get(user=request.user, exam_id=exam)

                if timezone.now() < karname.completed_at + timedelta(hours=24):
                    return Response({'message': 'you cant take another exam'}, status.HTTP_403_FORBIDDEN)

                if timezone.now() >= karname.completed_at + timedelta(days=3):
                    send_notification_in_3_days = True
                    UserQuestionAnswerCount.objects.filter(question__in=karname.exam_id.question.all(),
                                                           user=request.user).delete()
                    karname.delete()
                    karname = LitnerKarNameModel.objects.create(user=request.user, exam_id=exam)

            # Process each answer in the list
            for answer_data in answers:
                # Here we inject the `karname`'s primary key into the request data
                answer_data['karname'] = karname.pk  # Pass karname as pk

                serializer = LitnerTakeExamSerializer(
                    data=answer_data,
                    context={'exam': pk, 'request': request}  # You can add more context if needed
                )
                if serializer.is_valid():
                    serializer.save()  # Create LitnerKarNameDBModel objects
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            answers = LitnerKarNameDBModel.objects.filter(karname=karname)

            is_corrects = []
            is_false = []
            is_null = []

            for answer in answers:
                if answer.is_correct is not None:
                    if answer.is_correct:
                        is_corrects.append(answer)
                    else:
                        is_false.append(answer)
                else:
                    is_null.append(answer)

            for answer in is_corrects:
                question = answer.question
                user_answer_check, created = UserQuestionAnswerCount.objects.get_or_create(user=request.user,
                                                                                           question=question,
                                                                                           is_correctt=True)
                logger.info("Answers check  is_correct: %d", user_answer_check)
                #  send_notification_task.delay(token='user_fcm_token', title='Test Title', body='Test Body' ,eta=timezone.now() + timedelta(days=3))
                user_answer_check.save()

            for answer in is_false:
                question = answer.question
                user_answer_count, created = UserQuestionAnswerCount.objects.get_or_create(user=request.user,
                                                                                           question=question)
                logger.info("Answers check is false: %d", user_answer_check)
                #    send_notification_task.delay(token='user_fcm_token', title='Test Title', body='Test Body' ,eta=timezone.now() + timedelta(hours=24))
                user_answer_count.save()

            for answer in is_null:
                question = answer.question
                user_answer_check, created = UserQuestionAnswerCount.objects.get_or_create(user=request.user,
                                                                                           question=question)
                logger.info("Answers check is null : %d", user_answer_check)
                user_answer_check.save()

            result = {
                'True answers': [{
                    'question_id': answer.question.id,
                    'question_text': answer.question.question_text,
                    'answer_text': answer.question.answers_text
                } for answer in is_corrects if not answer.question.hide_question],
                'False answers': [{
                    'question_id': answer.question.id,
                    'question_text': answer.question.question_text,
                    'answer_text': answer.question.answers_text
                } for answer in is_false if not answer.question.hide_question],
                'None answers': [{
                    'question_id': answer.question.id,
                    'question_text': answer.question.question_text,
                    'answer_text': answer.question.answers_text
                } for answer in is_null if not answer.question.hide_question]
            }
            karname.completed_at = timezone.now()  # Update timestamp
            karname.save()
            exam.save()

            if send_notification_in_3_days:
                send_notification_task.apply_async(
                    # TODO: change the title and body of the notification
                    kwargs={'fcm_token': fcm_token, 'title': 'your correct answers are ready',
                            'body': 'now you have access to correct answers'},
                    eta=timezone.now() + timedelta(days=3),
                )
            else:
                send_notification_task.apply_async(
                    # TODO: change the title and body of the notification
                    kwargs={'fcm_token': fcm_token, 'title': 'retake the exam',
                            'body': 'now you can retake the exam'},
                    eta=timezone.now() + timedelta(days=1),
                )

            return Response(result)

        except Exception as exc:
            logger.error(f"Error in LitnerTakingExam (POST): {exc}")
            return Response({'message': f'An error occurred: {exc}'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        data = {'user': request.user.id, "exam_id": pk}

        if request.data:
            data['karname'] = request.data
            print(data)
        else:
            data['karname'] = []

        exam = get_object_or_404(LitnerModel, pk=pk)

        karname = get_object_or_404(LitnerKarNameModel, user=request.user, exam_id=exam)
        return Response(
            {'karname': {'exam_id': str(karname.exam_id), 'user': str(karname.user), 'completed_at': str(karname.completed_at)}},
            status.HTTP_200_OK)


class ListProfileMyClassView(generics.ListAPIView):
    serializer_class = MyLitnerClassSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        valid_objects = MyLitnerclass.objects.filter(markethubs__paid_users=self.request.user)
        return valid_objects

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})


class ListProfileMyClassCreatorView(generics.ListAPIView):
    serializer_class = MyLitnerClassSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        valid_objects = MyLitnerclass.objects.filter(author=self.request.user)
        return valid_objects

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})
