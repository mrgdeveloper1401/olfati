from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from markethub.models import MarketHubModel
from markethub.serializer import MarketHubSerializer


class MarketHubListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        # search | GetDetail | Get all
        data = MarketHubModel.objects.all()
        srz_data = MarketHubSerializer(data, many=True)

        return Response(srz_data.data)

    def post(self, request):
        data = MarketHubSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        data.save()
        return Response(data.data)


class MarketHubView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request,pk=None):
        data = MarketHubModel.objects.get(pk=pk)
        srz_data = MarketHubSerializer(instance=data,data=request.data,partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk=None):
        data = MarketHubModel.objects.get(pk=pk)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
