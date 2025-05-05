from django.urls import path
from rest_framework_nested import routers

from . import views

router = routers.SimpleRouter()
router.register("class_purchase", views.PurchaseLinterClassViewSet, basename="user_class_purchase")

class_purchase = routers.NestedSimpleRouter(router, "class_purchase", lookup="class_purchase")
class_purchase.register("season_purchase", views.PurchaseLinterSeasonViewSet, basename="season_purchase")

urlpatterns = [
    path("user-profile/", views.ProfileView.as_view(), name='user-profile'),
    path("profile/linter_class/", views.ProfileLinterClassView.as_view(), name='profile_linter_class'),
    path("profile/linter_class/<int:class_pk>/linter_season/",
         views.ProfileLinterSeasonView.as_view({"get": "list"}),
         name='profile_linter_season'),
    path("signup-login", views.SendCode.as_view(), name='user_login'),
    path("verify-otp", views.VerifyOTPView.as_view(), name='verify_otp'),
    # Admin:
    # path("admin-login", views.AdminLoginView.as_view()),
    # path("admin-reset", views.ResetPasswordView.as_view()),
    # path("admin-edite", views.EditProfileView.as_view()),

] + router.urls + class_purchase.urls
