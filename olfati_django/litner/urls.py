from django.urls import path
from rest_framework_nested import routers

from litner.views import LinterSeasonViewSet, LinterClassViewSet, LinterBoxViewSet, LinterFlashCartViewSet, \
    LinterUserAnswerView, SaleLinterSeasonViewSet

router = routers.SimpleRouter()

# show all class-list
router.register("class", LinterClassViewSet, basename="linter-class")
router.register("flash_cart", LinterFlashCartViewSet, basename="linter_flash_cart")

linter_class_router = routers.NestedSimpleRouter(router, "class", lookup="class")
linter_class_router.register("season", LinterSeasonViewSet, basename="linter-season")
linter_class_router.register("sale_season", SaleLinterSeasonViewSet, basename="linter-sale-season")

linter_session_router = routers.NestedSimpleRouter(linter_class_router, r"season",
                                                   lookup="season")
linter_session_router.register("box", LinterBoxViewSet, basename="linter-box")


urlpatterns = [

    path("answer/", LinterUserAnswerView.as_view(), name='linter_flash_cart_answer'),
] + router.urls + linter_class_router.urls + linter_session_router.urls + linter_session_router.urls
