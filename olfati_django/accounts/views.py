from rest_framework import status, response, views, mixins, viewsets, permissions, generics, decorators
from rest_framework_simplejwt.tokens import RefreshToken

from litner.models import MyLinterClass, LinterModel
from litner.serializer import MyLinterClassSerializer, LinterSerializer

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
            user = UserModel.objects.filter(phone_number=phone_number).only(
                "phone_number", "is_active", "is_staff"
            ).last()

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
                        "is_admin": user.is_staff
                    }
                )


class ProfileViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    پروفایل کاربر
    """
    queryset = UserModel.objects.only('first_name', "last_name", 'study_field', 'username', 'melli_code',
                                      'phone_number', 'email', 'date_joined')
    serializer_class = serializer.UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        else:
            return self.queryset.filter(id=self.request.user.id)


class ProfileLinterClassView(generics.ListAPIView):
    """
    کلاس هایی که توسط یک کاربر ایجاد شده باشد
    """
    serializer_class = MyLinterClassSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return MyLinterClass.objects.filter(author=self.request.user).only(
        "author__first_name", "author__last_name", "title", "study_field", "created_at", "cover_image",
        "updated_at",
    )


class ProfileLinterSeasonView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    فصل های هر کلاس که توسط یه کاربر ایجاد شده باشد
    """
    serializer_class = LinterSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return LinterModel.objects.filter(myclass__author=self.request.user).only(
        "title", "price", 'description', 'created_at', "myclass__author__phone_number", "created_at",
            "updated_at", "cover_image",  "myclass__author__first_name", "myclass__author__last_name", "is_sale"
    ).select_related("myclass__author",)


class SaleLinterClassViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    اون کلاسی که کاربر حداقل یک فصل ان را خریده هست
    """
    serializer_class = MyLinterClassSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        return MyLinterClass.objects.filter(
            linter__paid_users=self.request.user
    ).distinct()
