from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from litner.models import LitnerModel, LitnerKarNameModel, LitnerKarNameDBModel, MyLitnerclass
from litner.serializer import LitnerSerializer, LitnerDetailSerializer, LitnerTakeExamSerializer, MyLitnerClassSerializer


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


class LitnerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is None:
            try:
                leitners = LitnerModel.objects.all()
                serializer = LitnerSerializer(leitners, many=True, context = {'request': request})
                return Response({'data': serializer.data}, status.HTTP_200_OK)
            except Exception as ins:
                return Response({'message': str(ins)},status.HTTP_404_NOT_FOUND)
        else:
            try:
                leitners = LitnerModel.objects.get(pk=pk)
                serializer = LitnerDetailSerializer(leitners, context = {'request': request})
                data = serializer.data.get("litner")
                return Response({'data': data}, status.HTTP_200_OK)
            except Exception as ins:
                return Response({'message': 'Leitner notFound'}, status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):

        exam = get_object_or_404(LitnerModel, pk=pk)
        try:
            karname = LitnerKarNameModel.objects.get(user=request.user, exam_id=exam)
            answers = LitnerKarNameDBModel.objects.filter(karname=karname)
            is_corrects = []
            is_false = []
            is_null = []
            print(answers)
            for answer in answers:
                if not answer.is_correct is None:
                    if answer.is_correct == True:
                        is_corrects.append(
                            {
                                'question_id': answer.question.id,
                                'question_text': answer.question.question_text,
                                'answer_text': answer.question.answers_text
                            })
                    else:
                        if answer.is_correct == False:
                            is_false.append({
                                'question_id': answer.question.id,
                                'question_text': answer.question.question_text,
                                'answer_text': answer.question.answers_text
                            })
                else:
                    is_null.append({
                        'question_id': answer.question.id,
                        'question_text': answer.question.question_text,
                        'answer_text': answer.question.answers_text
                    })
            result = {
                'True answers': is_corrects,
                'False answers': is_false,
                'None answers': is_null
            }
            exam.save()
            return Response(result)

        except:
            # just questions that have answer
            # [
            #     {
            #         "question": 1,
            #         "is_correct": true or false
            #     }
            # ]
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
                return Response(serializer.errors, status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        # request.data example: you should send new questions and their choices 
        # [
        #     {
        #         "question":1,    #our questuin
        #         "choice":2      #client's answer
        #     },
        #     ...
        # ]
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
            return Response({"massage": "leitner remove successfully"}, status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(
                {"massage": "leitner not found"}, status.HTTP_404_NOT_FOUND)

    def put(self, request):
        pass

# a = {
#     'exam': 1,
#     'user': 20,
#     'answer': [
#         {
#             "id_question": 5,
#             "choice": None  # null
#         }
#     ],
#     # 'true_answer': [
#     #     {
#     #         "question_text": "سوال اول آزمون ریاضی که بود؟",
#     #         "answers_text": "رضا"
#     #     },
#     #     {
#     #         "question_text": "سوال 2 آزمون مامایی که بود؟",
#     #         "answers_text": "احمد"
#     #     },
#     #     {
#     #         "question_text": "سوال اول آزمون عربی که بود؟",
#     #         "answers_text": "علی"
#     #     },
#     # ],
#     # 'no_answer': [
#     #     {
#     #         "question_text": "امیر نمره ریاضیش چند بود؟",
#     #         "answers_text": "10"
#     #     },
#     #     {
#     #         "question_text": "سوال 2 آزمون مامایی که بود؟",
#     #         "answers_text": "احمد"
#     #     },
#     #     {
#     #         "question_text": "سوال اول آزمون عربی که بود؟",
#     #         "answers_text": "علی"
#     #     },
#     # ],
#     # 'false_answer': [
#     #     {
#     #         "question_text": "سوال اول آزمون ریاضی که بود؟",
#     #         "answers_text": "رضا"
#     #     },
#     #     {
#     #         "question_text": "سوال 2 آزمون مامایی که بود؟",
#     #         "answers_text": "احمد"
#     #     },
#     #     {
#     #         "question_text": "سوال اول آزمون عربی که بود؟",
#     #         "answers_text": "علی"
#     #     },
#     # ],
# }
