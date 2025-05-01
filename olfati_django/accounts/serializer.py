from django.utils.crypto import get_random_string
from rest_framework import serializers, exceptions

from utils.vlaidations import PhoneValidator
from .models import OtpModel, UserModel


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'


class RequestOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=[PhoneValidator()])

    def validate(self, attrs):
        phone = attrs.get('phone_number')
        otp = OtpModel.objects.filter(phone_number=phone).only("phone_number").last()

        if otp and otp.is_expired_otp_code is False:
            raise exceptions.ValidationError({"message": "you have already otp code please wait 2 minute"})

        return attrs


class VerifyOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp_code = serializers.IntegerField()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = UserModel
        fields = [
            'first_name',
            'last_name',
            'study_field',
            'username',
            'melli_code',
            'phone_number',
            'password',
            'password2',
            'email',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = UserModel.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (
            'id',
            'first_name',
            "last_name",
            'study_field',
            'username',
            'melli_code',
            'phone_number',
            'email',
            'date_joined',
        )
        read_only_fields = ("date_joined",)
