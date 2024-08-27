from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from litner.models import LitnerModel, LitnerKarNameModel, LitnerKarNameDBModel, MyLitnerclass,LitnerQuestionModel,UserQuestionAnswerCount,NotificationModel
from litner.serializer import LitnerSerializer, LitnerDetailSerializer, LitnerTakeExamSerializer, MyLitnerClassSerializer
from rest_framework import generics
from django.utils import timezone
from django.db.models import Q


permission_error = Response({'اجازه این کار را ندارید.'}, status.HTTP_403_FORBIDDEN)

class ListCreateMyClassView(ModelViewSet):
    permission_classes = [IsAuthenticated,]
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
            serializer = self.get_serializer(page, many=True, context = {'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data":serializer.data})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data.get('litners', None)
        return Response({"data":data})
    

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
    permission_classes = [IsAuthenticated]
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
            queryset =LitnerModel.objects.filter(myclass_id = self.kwargs.get('pk', None))
        return queryset   

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data":serializer.data})

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_author(request.user):
            return permission_error
        return super().partial_update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not (instance.is_author(request.user) or instance.is_paid_user(request.user)):
            return permission_error
        questions_to_display = LitnerQuestionModel.objects.filter(litner=instance)  # یا هر منطق دیگر
        serializer = self.get_serializer(instance, context={'request': request, 'questions_to_display': questions_to_display})
        data = serializer.data.get('question')
        return Response({'data':data})


class LitnerView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        data = LitnerDetailSerializer(data=request.data, context = {'request': request})
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
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None): 
        if pk is None: 
            try: 
                litners = LitnerModel.objects.all() 
                serializer = LitnerSerializer(litners, many=True) 
                return Response({'data': serializer.data}, status.HTTP_200_OK) 
            except Exception as ins: 
                return Response({'message': str(ins)}, status.HTTP_404_NOT_FOUND) 

        else: 
            try: 
                # Get the litner instance for the specified class id and the user
                litner = LitnerModel.objects.get(myclass_id=pk, paid_users=self.request.user)
                
                # Fetch questions for this litner
                questions = LitnerQuestionModel.objects.filter(litner=litner)
                
                # Get the count of how many times the user answered each question correctly
                user_question_answer_counts = UserQuestionAnswerCount.objects.filter(user=request.user, question__in=questions)

                if user_question_answer_counts.exists():  
                    # Get the question IDs of those the user answered less than 6 times correctly
                    question_ids_with_correct_counts = user_question_answer_counts.filter(correct_answer_count__lt=6, is_hide=False).values_list('question_id', flat=True)
                    
                    if question_ids_with_correct_counts.exists():
                        questions_to_display = questions.filter(id__in=question_ids_with_correct_counts)
                    else:
                        # If there are no questions the user answered less than 6 times correctly, display all questions
                        questions_to_display = questions
                else:
                    # If no recorded answers are found, display all questions
                    questions_to_display = questions

                serializer = LitnerDetailSerializer(litner, context={'request': request, 'exam': pk, 'questions_to_display': questions_to_display}) 
                
                return Response({'data': serializer.data}, status.HTTP_200_OK) 

            except LitnerModel.DoesNotExist:
                return Response({'message': 'litner not found'}, status.HTTP_404_NOT_FOUND) 
            except Exception as ins: 
                print(ins)
                return Response({'message': 'An error occurred'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


        
    def post(self, request, pk):
     exam = get_object_or_404(LitnerModel, pk=pk)
     try:
        karname = LitnerKarNameModel.objects.get(user=request.user, exam_id=exam)
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
            user_answer_count, created = UserQuestionAnswerCount.objects.get_or_create(user=request.user, question=question)
            # Increment correct_answer_count for the question
            user_answer_count.correct_answer_count += 1
            if user_answer_count.correct_answer_count>6:
                user_answer_count.is_hide=True
                user_answer_count.save()
            user_answer_count.save()
        
        for answer in is_false:
            question = answer.question
            user_answer_count, created = UserQuestionAnswerCount.objects.get_or_create(user=request.user, question=question)
            notification,created = NotificationModel.objects.get_or_create(user=request.user,question=question)
            notification.save()
            user_answer_count.save()

        for answer in is_null:
            question = answer.question
            user_answer_count, created = UserQuestionAnswerCount.objects.get_or_create(user=request.user, question=question)
            user_answer_count.save()

            


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
        exam.save()
        return Response(result)

     except Exception as e:
        # Error handling
        data = {'user': request.user.id, "exam_id": pk}
        if request.data:
            data['karname'] = request.data
        else:
            data['karname'] = []

        serializer = LitnerTakeExamSerializer(data=data, context={'request': request, 'exam': pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        
    def put(self, request, pk): 
        data = {'user': request.user.id, "exam_id": pk} 
        if request.data: 
            data['karname'] = request.data 
        else: 
            data['karname'] = [] 
        exam = get_object_or_404(LitnerModel, pk=pk) 
        karname = get_object_or_404(LitnerKarNameModel, user=request.user, exam_id=exam) 
        serializer = LitnerTakeExamSerializer(instance=karname, data=data, context={'request': request, 'exam': pk}, 
                                              partial=True) 
        if serializer.is_valid(): 
            try:
                serializer.save()
            except Exception:
                return Response(serializer.errors, status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)








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
        return Response({"data":serializer.data})
    



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
        return Response({"data":serializer.data})