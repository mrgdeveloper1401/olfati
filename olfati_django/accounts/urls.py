from django.urls import path
from rest_framework import routers

from . import views
from .views import ProfileViewSet

router = routers.SimpleRouter()
router.register('profile', ProfileViewSet, basename="user_profile")

urlpatterns = [
    path("login", views.SendCode.as_view(), name='user_login'),
    path("verify-otp", views.VerifyOTPView.as_view(), name='verify_otp'),
    path("create-user", views.UserRegistrationView.as_view(), name="create-user"),
    # Admin:
    # path("admin-login", views.AdminLoginView.as_view()),
    # path("admin-reset", views.ResetPasswordView.as_view()),
    # path("admin-edite", views.EditProfileView.as_view()),

] + router.urls
