from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .permissions import HasPurchasedAccess, IsAuthenticated
from .serializer import MarketHubSerializer, MarketHubPaidSerializer, MarketHubTakeExamSerializer, \
    MarketHubDetailSerializer


#  برای دیدن لیست مارکت هاب ها و امتحان
class MarketHubListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        # search | GetDetail | Get all
        if pk is None:
            try:
                exams = MarketHubModel.objects.all()
                serializer = MarketHubSerializer(exams, many=True)
                return Response({'data': serializer.data}, status.HTTP_200_OK)
            except Exception as ins:
                return Response({'message': str(ins)}, self.e404)
        else:
            try:
                exams = MarketHubModel.objects.get(pk=pk)
                serializer = MarketHubDetailSerializer(exams)
                return Response({'data': serializer.data}, status.HTTP_200_OK)
            except Exception as ins:
                return Response({'message': 'markethub notFound'}, self.e404)

    def post(self, request, pk):
        exam = get_object_or_404(MarketHubModel, pk=pk)
        try:
            karname = MarketHubKarNameModel.objects.get(request.user, exam_id=exam)
            answers = MarketHubKarNameDBModel.objects.filter(karname=karname)
            is_corrects = []
            is_false = []
            is_null = []
            for answer in answers:
                if not answer.is_correct is None:
                    if answer.is_correct == True:
                        is_corrects.append(
                            {
                                'question_id': answer.question.id,
                                #  'question_text':answer.question.question_text,
                                #  'answer_text':answer.answerss
                            })
                    else:
                        if answer.is_correct == False:
                            is_false.append(
                                {
                                    'question_id': answer.question.id,
                                    # 'question_text':answer.question.question_text,
                                    #   'answer_text':answer.answerss
                                })
                else:
                    is_null.append(
                        {
                            'question_id': answer.question.id,
                        })

            result = {
                'True answers': is_corrects,
                'False answers': is_false,
                'None answers': is_null}
            return Response(result)


        except:
            data = {'user': request.user.id, 'exam_id': pk}
            if request.data:
                data['karname'] = request.data
            else:
                data['karname'] = []
            srz = MarketHubTakeExamSerializer(data=data, context={'request': request, exam: pk})
            if srz.is_valid():
                srz.save()
                return Response(srz.data, 200)
            else:
                return Response(srz.errors, status=404)

    def put(self, request, pk):
        data = {'user': request.user.id, 'exam_id': pk}
        if request.data:
            data['karname'] = request.data
        else:
            data['karname'] = []
        exam = get_object_or_404(MarketHubModel, pk=pk)
        karname = get_object_or_404(MarketHubKarNameModel, user=request.user, exam_id=exam)
        srz = MarketHubTakeExamSerializer(instance=karname, data=data, context={'request': request, 'exam': exam},
                                          partial=True)
        if srz.is_valid():
            try:
                srz.save()
            except Exception:
                return Response(srz.errors, status=404)
            else:
                return Response(srz.errors, status=404)
            return Response(srz.data)


#  برای دیلیت و دیدن دیتیل و اپدیت مارکت هاب
class MarketHubView(generics.RetrieveAPIView, generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, HasPurchasedAccess]

    def get(self, request, pk=None):
        payment = Payment.objects.get(MarketHub=pk)
        if request.user.is_authenticated and payment.has_access == True:
            data = MarketHubQuestionModel.objects.filter(pk=pk)
            srz_data = MarketHubPaidSerializer(instance=data, many=True)
            return Response(srz_data.data)
        else:
            data = MarketHubModel.objects.get(pk=pk)
            srz_data = MarketHubSerializer(data)
            return Response(srz_data.data)

    def put(self, request, pk=None):
        data = MarketHubModel.objects.get(pk=pk)
        srz_data = MarketHubSerializer(instance=data, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        data = MarketHubModel.objects.get(pk=pk)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#  نشان دادن کوسشن به یوزر  در صورت پرداخت در غیر این صورت نشان دادن مارکت هاب
class QuestionView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, HasPurchasedAccess]

    def get(self, request, pk):
        payment = Payment.objects.get(MarketHub=pk)
        if request.user.is_authenticated and payment.has_access == True:
            data = MarketHubQuestionModel.objects.filter(pk=pk)
            srz_data = MarketHubPaidSerializer(instance=data, many=True)
            return Response(srz_data.data)

        data = get_object_or_404(MarketHubModel, pk=pk)
        srz_data = MarketHubSerializer(instance=data)
        return Response(srz_data.data)
