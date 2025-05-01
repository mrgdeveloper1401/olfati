from django.contrib.auth import models as auth_models


class UserManager(auth_models.BaseUserManager):
    def create_user(self, username: str, melli_code: str, phone_number: str, **kwargs):
        if not phone_number:
            raise ValueError('user must have Phone Number')

        if not username:
            raise ValueError('user must have username')

        if not melli_code:
            raise ValueError('user must have Melli Code')

        user = self.model(phone_number=phone_number, username=username, melli_code=melli_code, **kwargs)
        user.is_active = True
        user.save()
        return user

    def create_superuser(self, username: str, melli_code: str, phone_number: str, password: str = None, **kwargs):
        user = self.create_user(
            username=username,
            melli_code=melli_code,
            phone_number=phone_number,
            **kwargs
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

    def create_user_by_phone(self, phone_number, password=None):
        if not phone_number:
            raise ValueError('user must have mobile number')

        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save()
        return user
