import codecs

# from django.contrib.auth.models import Group
from rest_framework import status, response, views, mixins, viewsets, permissions
from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate

from utils.sed_code import send_sms_verify
from .models import OtpModel, UserModel
from .permissions import NotAuthenticated
from . import serializer


class UserRegistrationView(views.APIView):
    serializer_class = serializer.UserRegistrationSerializer
    permission_classes = (NotAuthenticated,)

    def post(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        refresh = RefreshToken.for_user(user)
        data = {
            'user_id': user.id,
            'phone_number': user.phone_number,
            'access': str(refresh.access_token),
            'message': 'User registered successfully'
        }
        return response.Response(data, status=status.HTTP_201_CREATED)


class SendCode(views.APIView):
    serializer_class = serializer.RequestOtpSerializer
    permission_classes = (NotAuthenticated,)

    def post(self, request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)
        phone_number = ser.validated_data['phone_number']

        otp = OtpModel.objects.create(phone_number=phone_number)
        send_sms_verify(otp.phone_number, otp.otp_code)
        return response.Response({'message': 'Code Sent!'}, status.HTTP_201_CREATED)


class VerifyOTPView(views.APIView):
    serializer_class = serializer.VerifyOtpSerializer
    permission_classes = (NotAuthenticated,)

    def post(self, request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)
        phone_number = ser.validated_data['phone_number']
        code = ser.validated_data['otp_code']

        otp_code = OtpModel.objects.filter(
            phone_number=phone_number,
            otp_code=code
        ).only("phone_number", "otp_code", "expired_date").last()

        if not otp_code:
            return response.Response({'message': 'OTP not found'}, status=status.HTTP_404_NOT_FOUND)

        elif otp_code and otp_code.is_expired_otp_code is True:
            otp_code.delete()
            return response.Response({"message": "otp code is expired"}, status=status.HTTP_403_FORBIDDEN)

        else:
            user = UserModel.objects.filter(phone_number=phone_number).only("phone_number", "is_active").last()

            if not user:
                return response.Response({'message': 'you must create account'}, status.HTTP_404_NOT_FOUND)

            if user and user.is_active is False:
                return response.Response({'message': 'your account is benned'}, status.HTTP_403_FORBIDDEN)

            else:
                otp_code.delete()
                token = RefreshToken.for_user(user)
                return response.Response(
                    data={
                        "access_token": str(token.access_token),
                    }
                )


# class AdminLoginView(views.APIView):
    #  permission_classes = [AllowAny]

    # def post(self, request):
    #     username = request.data.get('username')
    #     # password = request.data.get('password')
    #     user = authenticate(username=username)
    #     if user is not None and user.is_superuser:
    #         refresh = RefreshToken.for_user(user)
    #         return response.Response({
    #             'refresh': str(refresh),
    #             'access': str(refresh.access_token),
    #         })
    #     else:
    #         return response.Response({'error': 'Invalid Credentials or Not Superuser'}, status=status.HTTP_401_UNAUTHORIZED)


# class ResetPasswordView(views.APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         new_password = request.data.get('new_password')
#         try:
#             user = UserModel.objects.get(username=username)
#             user.set_password(new_password)
#             user.save()

            # اضافه کردن کاربر به گروه مورد نظر (مثلاً گروه staff)
            # staff_group = Group.objects.get(name='teacher')  # فرضاً که گروهی به نام staff وجود دارد
            # user.groups.add(staff_group)

        #     return response.Response({'message': 'Password reset successfully. User now has access to admin panel.'})
        # except UserModel.DoesNotExist:
        #     return response.Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)


# class EditProfileView(views.APIView):
#     def post(self, request):
        # if not request.user.is_superuser:
        #    return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

        # username = request.data.get('username')
        # new_username = request.data.get('new_username', None)
        # first_name = request.data.get('first_name', None)
        # last_name = request.data.get('last_name', None)
        # study_field = request.data.get('study_field', None)
        # melli_code = request.data.get('melli_code', None)
        # phone_number = request.data.get('phone_number', None)
        # try:
        #     user = UserModel.objects.get(username=username)
        #     if new_username:
        #         user.username = new_username
        #     if last_name:
        #         user.last_name = last_name
        #     if first_name:
        #         user.first_name = first_name
        #     if study_field:
        #         user.study_field = study_field
        #     if melli_code:
        #         user.melli_code = melli_code
        #     if phone_number:
        #         user.phone_number = phone_number
        #     user.save()
            # سریالایز و برگرداندن داده‌های کاربر
            # user_data = serializer.UserSerializers(user).data
            # return response.Response({'message': 'Profile updated successfully', 'data': user_data})
        # except UserModel.DoesNotExist:
        #     return response.Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)


class ProfileViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = UserModel.objects.only('first_name', "last_name", 'study_field', 'username', 'melli_code',
                                      'phone_number', 'email', 'date_joined')
    serializer_class = serializer.UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        else:
            return self.queryset.filter(id=self.request.user.id)
