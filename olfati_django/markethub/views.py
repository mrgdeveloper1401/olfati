from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import MarketHubModel, Payment, MarketHubQuestionModel
from .permissions import HasPurchasedAccess, IsAuthenticated
from .serializer import MarketHubSerializer, MarketHubQuestionSerializer, MarketHubPaidSerializer

# برای دیدن لیست مارکت هاب ها
class MarketHubListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,pk=None ):
        # search | GetDetail | Get all
        data = MarketHubModel.objects.all()
        srz_data = MarketHubSerializer(data, many=True)
        return Response(srz_data.data)
    def post(self, request):
        data = MarketHubSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        data.save()
        return Response(data.data)

#  برای دیلیت و دیدن دیتیل و اپدیت مارکت هاب
class MarketHubView(generics.RetrieveAPIView,generics.RetrieveUpdateAPIView,generics.DestroyAPIView):
    permission_classes = [IsAuthenticated,HasPurchasedAccess]
    def get(self,request,pk=None):
        payment = Payment.objects.get(MarketHub=pk)
        if request.user.is_authenticated and  payment.has_access == True:
              data = MarketHubQuestionModel.objects.filter(pk=pk)
              srz_data = MarketHubPaidSerializer(instance=data, many=True)
              return Response(srz_data.data)
        else:
          data = MarketHubModel.objects.get(pk=pk)
          srz_data = MarketHubSerializer(data)
          return  Response(srz_data.data)
    
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
    permission_classes = [IsAuthenticated,HasPurchasedAccess]
    def get(self, request,pk):
            payment = Payment.objects.get(MarketHub=pk)
            if request.user.is_authenticated and  payment.has_access == True:
                  data = MarketHubQuestionModel.objects.filter(pk=pk) 
                  srz_data = MarketHubPaidSerializer(instance=data,many=True)
                  return Response(srz_data.data)
            
            data = get_object_or_404(MarketHubModel,pk=pk)
            srz_data = MarketHubSerializer(instance=data)
            return Response(srz_data.data)






