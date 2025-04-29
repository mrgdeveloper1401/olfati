from django.urls import path
from rest_framework_nested import routers

from . import views

router = routers.SimpleRouter()

# show all class-list
router.register("class", views.LinterClassViewSet, basename="linter-class")
router.register("flash_cart", views.LinterFlashCartViewSet, basename="linter_flash_cart")
router.register("admin_list_linter_class", views.AdminListLinterClassViewSet, basename="admin_list_linter_class")

linter_class_router = routers.NestedSimpleRouter(router, "class", lookup="class")
linter_class_router.register("season", views.LinterSeasonViewSet, basename="linter-season")
linter_class_router.register("sale_season", views.SaleLinterSeasonViewSet, basename="linter-sale-season")

linter_session_router = routers.NestedSimpleRouter(linter_class_router, r"season",
                                                   lookup="season")
linter_session_router.register("box", views.LinterBoxViewSet, basename="linter-box")


urlpatterns = [

    path("answer/", views.LinterUserAnswerView.as_view(), name='linter_flash_cart_answer'),
] + router.urls + linter_class_router.urls + linter_session_router.urls + linter_session_router.urls
