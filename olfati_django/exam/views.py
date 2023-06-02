from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ExamModel, KarNameModel
from .serializer import ExamDetailsSerializer, ExamSerializer, KarNameSerializer


class ExamListView(APIView):
    permission_classes = [IsAuthenticated]
    e404 = status.HTTP_400_BAD_REQUEST

    def get(self, request, pk=None):
        if pk is None:
            try:
                exams = ExamModel.objects.all()
                serializer = ExamSerializer(exams, many=True)
                return Response({'status': status.HTTP_200_OK, 'data': serializer.data})
            except Exception as ins:
                return Response({'status': self.e404, 'message': str(ins)}, status=self.e404)
        else:
            try:
                exams = ExamModel.objects.get(pk=pk)
                serializer = ExamDetailsSerializer(exams)
                return Response(serializer.data)
            except Exception as ins:
                return Response({'status': self.e404, 'message': 'آزمون یافت نشد!'}, status=self.e404)


class ExamView(APIView):
    permission_classes = [IsAdminUser]
    e404 = status.HTTP_400_BAD_REQUEST

    def post(self, request):
        try:
            serializer = ExamDetailsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {'status': status.HTTP_201_CREATED, 'message': 'آزمون با موفقیت ساخته شد', 'data': serializer.data})
            return Response({'status': self.e404, 'data': serializer.errors}, status=self.e404)
        except Exception as e:
            return Response({'status': self.e404, 'data': 'اطلاعات وارد شده کامل نیست!'}, status=self.e404)

    def put(self, request, pk):
        query = ExamModel.objects.get(pk=pk)
        serializer = ExamDetailsSerializer(instance=query, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'status': status.HTTP_200_OK, 'message': 'آزمون با موفقیت بروزرسانی شد', 'data': serializer.data})
        return Response({'status': self.e404, 'message': serializer.errors}, status=self.e404)

    def delete(self, request, pk):
        try:
            query = ExamModel.objects.get(pk=pk)
            query.delete()
            return Response({'status': status.HTTP_200_OK, 'message': 'آزمون با موفقیت حذف شد'})
        except Exception as e:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'message': 'آزمون یافت نشد'})


class ExamKarNameView(APIView):

    def get(self, request):
        query = KarNameModel.objects.all()
        srz_data = KarNameSerializer(query).data
        return Response(srz_data)