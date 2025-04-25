from rest_framework import status, permissions, viewsets, mixins, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializer, models

import logging

from utils.vlaidations import CommonPagination
from .permissions import IsOwnerOrReadOnlyLinterModel, IsOwnerOrReadOnlyLinterClass

logger = logging.getLogger(__name__)
permission_error = Response({'اجازه این کار را ندارید.'}, status.HTTP_403_FORBIDDEN)


class LinterClassViewSet(viewsets.ModelViewSet):
    serializer_class = serializer.MyLinterClassSerializer
    queryset = models.MyLinterClass.objects.select_related(
        "author"
    ).only(
        "author__first_name", "author__last_name", "title", "study_field", "cover_image__title", "created_at",
        "updated_at", "cover_image__image_url"
    ).select_related("cover_image")
    pagination_class = CommonPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnlyLinterClass,)

    # def get_permissions(self):
    #     if self.request.method in ['POST', "PUT", "PATCH", "DELETE"]:
    #         self.permission_classes = (permissions.IsAdminUser,)
    #     else:
    #         self.permission_classes = (permissions.IsAuthenticated,)
    #     return super().get_permissions()
    #
    # def get_queryset(self):
    #     query = MyLitnerclass.objects.all()
    #
    #     if self.request.user.is_staff is False:
    #         query = query.filter(is_publish=True)
    #
    #     return query


class LinterSeasonViewSet(viewsets.ModelViewSet):
    pagination_class = CommonPagination
    serializer_class = serializer.LinterSerializer
    permission_classes = (IsOwnerOrReadOnlyLinterModel,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['linter_class_pk'] = self.kwargs["class_pk"]
        return context

    def get_queryset(self):
        return models.LinterModel.objects.filter(
            myclass_id=self.kwargs['class_pk'],
            # paid_users=self.request.user
        ).only(
        "title", "price", 'description', 'created_at', "myclass__author__phone_number", "created_by",
            "cover_image__image_url", "created_at", "updated_at",
    ).select_related("myclass__author")

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     if not (instance.is_author(request.user) or instance.is_paid_user(request.user)):
    #         return permission_error
    #
    #     try:
    #         karname = LitnerKarNameModel.objects.get(user=request.user, exam_id=instance)
    #     except LitnerKarNameModel.DoesNotExist:
    #         questions_to_display = LitnerQuestionModel.objects.filter(litner=instance)
    #     else:
    #         if timezone.now() < karname.completed_at + timedelta(hours=24):
    #             return Response({'message': 'you cant take another exam'}, status.HTTP_403_FORBIDDEN)
    #
    #         if timezone.now() >= karname.completed_at + timedelta(days=3):
    #             questions_to_display = LitnerQuestionModel.objects.filter(litner=instance)
    #         else:
    #             questions_to_display = LitnerQuestionModel.objects.filter(
    #                 Q(user_answers__isnull=True) | Q(user_answers__is_correctt__isnull=True) |
    #                 Q(user_answers__is_correctt=False), litner=instance
    #             )
    #
    #     serializer = self.get_serializer(instance,
    #                                      context={'request': request, 'questions_to_display': questions_to_display})
    #     data = serializer.data.get('question')
    #     return Response({'data': data})


class LitnerView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        data = serializer.LinterSerializer(data=request.data, context={'request': request})
        data.is_valid(raise_exception=True)
        data.save()
        return Response(data.data)

    def delete(self, request, pk):
        try:
            instance = models.LinterModel.objects.get(pk=pk)
            instance.delete()
            return Response({"massage": "litner remove successfully"}, status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(
                {"massage": "litner not found"}, status.HTTP_404_NOT_FOUND)

    def put(self, request):
        pass


# class LitnerTakingExam(APIView):
#     # permission_classes = [IsAuthenticated]
#
#     def get(self, request, pk=None):
#         if pk is None:
#             try:
#                 litners = LitnerModel.objects.all()
#                 serializer = LitnerSerializer(litners, many=True, context={'request': request})
#                 return Response({'data': serializer.data}, status.HTTP_200_OK)
#             except Exception as exc:
#                 logger.error(f"Error in LitnerTakingExam (GET all): {exc}")
#                 return Response({'message': str(exc)}, status.HTTP_404_NOT_FOUND)
#         else:
#             try:
#                 litner = LitnerModel.objects.get(myclass_id=pk, paid_users=self.request.user)
#                 karname = LitnerKarNameModel.objects.get(user=request.user, exam_id=litner)
#                 time_elapsed = timezone.now() - karname.completed_at
#
#                 if time_elapsed < timedelta(days=3):  # If less than 3 days, restrict access based on answer status
#                     user_answers = UserQuestionAnswerCount.objects.filter(user=request.user,
#                                                                           question__in=litner.question.all())
#
#                     if user_answers.filter(is_correctt=False).exists():
#                         # Show only wrong answers
#                         wrong_questions = user_answers.filter(is_correctt=False).values_list('question', flat=True)
#                         questions_to_display = LitnerQuestionModel.objects.filter(id__in=wrong_questions)
#                     else:
#                         # All answers correct, restrict access completely
#                         return Response({'message': 'You cannot access the exam for 3 days.'},
#                                         status.HTTP_403_FORBIDDEN)
#                 else:
#                     # After 3 days, show all questions again
#                     questions_to_display = LitnerQuestionModel.objects.filter(litner=litner)
#
#                 serializer = LitnerDetailSerializer(litner, context={'request': request, 'exam': pk,
#                                                                      'questions_to_display': questions_to_display})
#                 return Response({'data': serializer.data}, status.HTTP_200_OK)
#
#             except LitnerModel.DoesNotExist:
#                 return Response({'message': 'Litner not found'}, status.HTTP_404_NOT_FOUND)
#             except LitnerKarNameModel.DoesNotExist:
#                 return Response({'message': 'Karname not found'}, status.HTTP_404_NOT_FOUND)
#             except Exception as exc:
#                 logger.error(f"Error in LitnerTakingExam (GET with pk): {exc}")
#                 return Response({'message': f'An error occurred: {exc}'}, status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     def post(self, request, pk):
#         exam = get_object_or_404(LitnerModel, pk=pk)
#         fcm_token = request.data['fcm_token']
#         answers = request.data['answers']
#         send_notification_in_3_days = False
#
#         try:
#             # Check if karname exists or create one
#             test = LitnerKarNameModel.objects.filter(user=request.user, exam_id=exam).exists()
#
#             if not test:
#                 karname = LitnerKarNameModel.objects.create(user=request.user, exam_id=exam)
#                 send_notification_in_3_days = True
#             else:
#                 karname = LitnerKarNameModel.objects.get(user=request.user, exam_id=exam)
#
#                 if timezone.now() < karname.completed_at + timedelta(hours=24):
#                     return Response({'message': 'you cant take another exam'}, status.HTTP_403_FORBIDDEN)
#
#                 if timezone.now() >= karname.completed_at + timedelta(days=3):
#                     send_notification_in_3_days = True
#                     UserQuestionAnswerCount.objects.filter(question__in=karname.exam_id.question.all(),
#                                                            user=request.user).delete()
#                     karname.delete()
#                     karname = LitnerKarNameModel.objects.create(user=request.user, exam_id=exam)
#
#             # Process each answer in the list
#             for answer_data in answers:
#                 # Here we inject the `karname`'s primary key into the request data
#                 answer_data['karname'] = karname.pk  # Pass karname as pk
#
#                 serializer = LitnerTakeExamSerializer(
#                     data=answer_data,
#                     context={'exam': pk, 'request': request}  # You can add more context if needed
#                 )
#                 if serializer.is_valid():
#                     serializer.save()  # Create LitnerKarNameDBModel objects
#                 else:
#                     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#             answers = LitnerKarNameDBModel.objects.filter(karname=karname)
#
#             is_corrects = []
#             is_false = []
#             is_null = []
#
#             for answer in answers:
#                 if answer.is_correct is not None:
#                     if answer.is_correct:
#                         is_corrects.append(answer)
#                     else:
#                         is_false.append(answer)
#                 else:
#                     is_null.append(answer)
#
#             for answer in is_corrects:
#                 question = answer.question
#                 user_answer_check, created = UserQuestionAnswerCount.objects.get_or_create(user=request.user,
#                                                                                            question=question,
#                                                                                            is_correctt=True)
#                 logger.info("Answers check  is_correct: %d", user_answer_check)
#                 #  send_notification_task.delay(token='user_fcm_token', title='Test Title', body='Test Body' ,eta=timezone.now() + timedelta(days=3))
#                 user_answer_check.save()
#
#             for answer in is_false:
#                 question = answer.question
#                 user_answer_count, created = UserQuestionAnswerCount.objects.get_or_create(user=request.user,
#                                                                                            question=question)
#                 logger.info("Answers check is false: %d", user_answer_check)
#                 #    send_notification_task.delay(token='user_fcm_token', title='Test Title', body='Test Body' ,eta=timezone.now() + timedelta(hours=24))
#                 user_answer_count.save()
#
#             for answer in is_null:
#                 question = answer.question
#                 user_answer_check, created = UserQuestionAnswerCount.objects.get_or_create(user=request.user,
#                                                                                            question=question)
#                 logger.info("Answers check is null : %d", user_answer_check)
#                 user_answer_check.save()
#
#             result = {
#                 'True answers': [{
#                     'question_id': answer.question.id,
#                     'question_text': answer.question.question_text,
#                     'answer_text': answer.question.answers_text
#                 } for answer in is_corrects if not answer.question.hide_question],
#                 'False answers': [{
#                     'question_id': answer.question.id,
#                     'question_text': answer.question.question_text,
#                     'answer_text': answer.question.answers_text
#                 } for answer in is_false if not answer.question.hide_question],
#                 'None answers': [{
#                     'question_id': answer.question.id,
#                     'question_text': answer.question.question_text,
#                     'answer_text': answer.question.answers_text
#                 } for answer in is_null if not answer.question.hide_question]
#             }
#             karname.completed_at = timezone.now()  # Update timestamp
#             karname.save()
#             exam.save()
#
#             if send_notification_in_3_days:
#                 send_notification_task.apply_async(
#                     # TODO: change the title and body of the notification
#                     kwargs={'fcm_token': fcm_token, 'title': 'your correct answers are ready',
#                             'body': 'now you have access to correct answers'},
#                     eta=timezone.now() + timedelta(days=3),
#                 )
#             else:
#                 send_notification_task.apply_async(
#                     # TODO: change the title and body of the notification
#                     kwargs={'fcm_token': fcm_token, 'title': 'retake the exam',
#                             'body': 'now you can retake the exam'},
#                     eta=timezone.now() + timedelta(days=1),
#                 )
#
#             return Response(result)
#
#         except Exception as exc:
#             logger.error(f"Error in LitnerTakingExam (POST): {exc}")
#             return Response({'message': f'An error occurred: {exc}'}, status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     def put(self, request, pk):
#         data = {'user': request.user.id, "exam_id": pk}
#
#         if request.data:
#             data['karname'] = request.data
#             print(data)
#         else:
#             data['karname'] = []
#
#         exam = get_object_or_404(LitnerModel, pk=pk)
#
#         karname = get_object_or_404(LitnerKarNameModel, user=request.user, exam_id=exam)
#         return Response(
#             {'karname': {'exam_id': str(karname.exam_id), 'user': str(karname.user), 'completed_at': str(karname.completed_at)}},
#             status.HTTP_200_OK)


# class ListProfileMyClassView(generics.ListAPIView):
#     serializer_class = MyLitnerClassSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         valid_objects = MyLitnerclass.objects.filter(markethubs__paid_users=self.request.user)
#         return valid_objects
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#
#         serializer = self.get_serializer(queryset, many=True)
#         return Response({"data": serializer.data})


# class ListProfileMyClassCreatorView(generics.ListAPIView):
#     serializer_class = MyLitnerClassSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         valid_objects = MyLitnerclass.objects.filter(author=self.request.user)
#         return valid_objects
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#
#         serializer = self.get_serializer(queryset, many=True)
#         return Response({"data": serializer.data})


class LinterBoxViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    def get_queryset(self):
        return models.LeitnerBox.objects.filter(
            linter_id=self.kwargs['season_pk'],
            linter__myclass_id=self.kwargs['class_pk'],
            linter__paid_users=self.request.user
        ).only("box_number")
    serializer_class = serializer.UserLinterBoxSerializer
    permission_classes = (permissions.IsAuthenticated,)

        # if self.request.user.is_staff is False:
        #     query = query.filter(is_active=True).only("box_number")
        #
        # return query

    # def get_permissions(self):
    #     if self.request.method in ['POST', "PUT", "PATCH", "DELETE"]:
    #         self.permission_classes = (permissions.IsAdminUser,)
    #     else:
    #         self.permission_classes = (permissions.IsAuthenticated,)
    #     return super().get_permissions()

    # def get_serializer_class(self):
    #     if self.request.user.is_staff is False:
    #         return serializer.UserLinterBoxSerializer
    #     else:
    #         return serializer.AdminLinterBoxSerializer

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['linter_season_pk'] = self.kwargs['season_pk']
    #     return context


class LinterFlashCartViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializer.LinterFlashCartSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # def get_permissions(self):
    #     if self.request.method in ['POST', "PUT", "PATCH", "DELETE"]:
    #         self.permission_classes = (permissions.IsAdminUser,)
    #     else:
    #         self.permission_classes = (permissions.IsAuthenticated,)
    #     return super().get_permissions()

    def get_queryset(self):
        return models.LinterFlashCart.objects.filter(
            box_id=self.kwargs['box_pk'], box__linter_id=self.kwargs['season_pk'],
            box__linter__myclass_id=self.kwargs['class_pk'],
            box__linter__paid_users=self.request.user
        ).select_related("box").only(
            "question_text", "answers_text", "box__box_number"
        )

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['linter_box_pk'] = self.kwargs['box_pk']
    #     return context


class LinterUserAnswerView(generics.CreateAPIView):
    """
    status --> (correct, wrong, skipped)
    """
    serializer_class = serializer.LinterUserAnswerSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.UserAnswer.objects.all()
