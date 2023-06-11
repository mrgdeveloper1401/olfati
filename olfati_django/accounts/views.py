from sqlite3 import IntegrityError
import codecs
from datetime import timedelta, datetime
from random import randint
from django.utils import timezone
from kavenegar import KavenegarAPI
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import OtpModel, UserModel
from .serializer import OtpSerializers, UserSerializers


class UserView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            if UserModel.objects.filter(phone_number=phone_number).exists():
                return Response({'error': 'شماره تلفن تکراری است.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    user_instance = serializer.save(is_active=True)
                    refresh = RefreshToken.for_user(user_instance)
                    token = {'refresh': str(refresh), 'access': str(refresh.access_token)}
                    response_data = {
                        'message': 'پروفایل با موفقیت تکمیل شد.',
                        'user': serializer.data,
                        'token': token
                    }
                    return Response(response_data, status=status.HTTP_201_CREATED)
                except IntegrityError:
                    return Response({'error': 'خطای دیگری رخ داد.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        userData = UserModel.objects.all()
        srz = UserSerializers(instance=userData, many=True)
        return Response(srz.data)


class Helper:
    @staticmethod
    def generate_otp_code():
        return str(randint(1000, 9999))


class SendCode(APIView):
    wait_time = timedelta(minutes=1)  # مدت زمان انتظار بین درخواست‌ها

    def post(self, request):
        phone_number = request.data.get("phone_number")
        if not phone_number:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'Invalid phone number.'})
        try:
            current_time = timezone.now()
            code = Helper.generate_otp_code()
            # بررسی محدودیت ارسال برای هر شماره تلفن منحصر به فرد
            last_request_time = request.session.get(f'last_request_time_{phone_number}')
            if last_request_time:
                last_request_time = datetime.fromisoformat(last_request_time)
                time_difference = current_time - last_request_time
                if time_difference < self.wait_time:
                    remaining_time = self.wait_time - time_difference
                    return Response({
                        'status': status.HTTP_429_TOO_MANY_REQUESTS,
                        'message': f'Please wait {remaining_time.seconds} seconds'
                    })
            api_key = '68664A5153554961366569533949395878794951444D2F77732F7378523737783070482B4D434F516549513D'
            params = {'sender': '10008663', 'receptor': phone_number, 'message': f'کدتایید شما: \n {code}'}
            api = KavenegarAPI(api_key)
            api.sms_send(params)
            request.session[f'last_request_time_{phone_number}'] = str(current_time)  # ذخیره زمان ارسال آخرین درخواست
            OtpModel.objects.create(phone_number=phone_number, otpCode=code)
            return Response({'status': status.HTTP_200_OK, 'message': f'Code Sent! {code}'})
        except Exception as e:
            error_message = str(e)
            decoded_error_message = codecs.decode(error_message, 'unicode-escape').encode('latin-1').decode('utf-8')
            return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': error_message})


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OtpSerializers(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = serializer.validated_data['otpCode']
            try:
                otp_code = OtpModel.objects.get(phone_number=phone_number, otpCode=code)
                try:
                    user = UserModel.objects.get(phone_number=phone_number, is_active=True)
                    userSRZ = UserSerializers(instance=user).data
                    print(user)
                    print("+++++++++++++")
                    print(userSRZ)
                    refresh = RefreshToken.for_user(user)
                    token = {'refresh': str(refresh), 'access': str(refresh.access_token)}
                    otp_code.delete()
                    return Response({'status': status.HTTP_200_OK, 'is_active': True, 'user': userSRZ, 'token': token})
                except UserModel.DoesNotExist:
                    return Response({'status': status.HTTP_200_OK, 'is_active': False})
            except OtpModel.DoesNotExist:
                return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'کد درست نیست! :('})
        return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': serializer.errors})
