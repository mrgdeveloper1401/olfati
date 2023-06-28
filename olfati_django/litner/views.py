from litner.models import LitnerModel, LitnerKarNameModel
from litner.serializer import LitnerSerializer, LitnerDetailSerializer, LitnerKarNameSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView


class LitnerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is None:
            data = LitnerModel.objects.all()
            srz_data = LitnerSerializer(data, many=True).data
            return Response(srz_data, status.HTTP_200_OK)
        else:
            pk_data = LitnerModel.objects.get(pk=pk)
            srz_data = LitnerDetailSerializer(pk_data).data
            return Response(srz_data, status.HTTP_200_OK)


class LitnerView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        data = LitnerDetailSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        data.save()
        return Response(data.data)

    def delete(self, request, pk):
        try:
            instance = LitnerModel.objects.get(pk=pk)
            instance.delete()
            return Response({"massage": "آزمون حذف شد"}, status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(
                {"massage": "آزمون یافت نشد"}, status.HTTP_404_NOT_FOUND)

    def put(self, request):
        pass


class LitnerKarNameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Add LitnerKarName Database
        data = LitnerKarNameSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        data.save()
        return Response(data.data)

    def get(self, request):
        # GET LitnerKarName Database From ID Litner
        query = LitnerKarNameModel.objects.all()
        total_count = query.count()
        print(total_count)
        srz_data = LitnerKarNameSerializer(query, many=True).data
        return Response(srz_data)

    def put(self, request, pk):
        # Update LitnerKarName Database From ID Litner
        pass


a = {
    'exam': 1,
    'user': 20,
    'answer': [
        {
            "id_question": 5,
            "choice": None #null
        }
    ],
    # 'true_answer': [
    #     {
    #         "question_text": "سوال اول آزمون ریاضی که بود؟",
    #         "answers_text": "رضا"
    #     },
    #     {
    #         "question_text": "سوال 2 آزمون مامایی که بود؟",
    #         "answers_text": "احمد"
    #     },
    #     {
    #         "question_text": "سوال اول آزمون عربی که بود؟",
    #         "answers_text": "علی"
    #     },
    # ],
    # 'no_answer': [
    #     {
    #         "question_text": "امیر نمره ریاضیش چند بود؟",
    #         "answers_text": "10"
    #     },
    #     {
    #         "question_text": "سوال 2 آزمون مامایی که بود؟",
    #         "answers_text": "احمد"
    #     },
    #     {
    #         "question_text": "سوال اول آزمون عربی که بود؟",
    #         "answers_text": "علی"
    #     },
    # ],
    # 'false_answer': [
    #     {
    #         "question_text": "سوال اول آزمون ریاضی که بود؟",
    #         "answers_text": "رضا"
    #     },
    #     {
    #         "question_text": "سوال 2 آزمون مامایی که بود؟",
    #         "answers_text": "احمد"
    #     },
    #     {
    #         "question_text": "سوال اول آزمون عربی که بود؟",
    #         "answers_text": "علی"
    #     },
    # ],
}
