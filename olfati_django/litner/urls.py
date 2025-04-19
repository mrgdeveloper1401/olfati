from django.urls import path
from rest_framework_nested import routers

from litner.views import LinterSeasonViewSet, LinterClassViewSet, LinterBoxViewSet, LinterFlashCartViewSet, \
    LinterUserAnswerView

router = routers.SimpleRouter()

# show all class-list
router.register("class", LinterClassViewSet, basename="linter-class")

linter_class_router = routers.NestedSimpleRouter(router, "class", lookup="class")
linter_class_router.register("season", LinterSeasonViewSet, basename="linter-season")

linter_session_router = routers.NestedSimpleRouter(linter_class_router, r"season",
                                                   lookup="season")
linter_session_router.register("box", LinterBoxViewSet, basename="linter-box")

linter_box_router = routers.NestedSimpleRouter(linter_session_router, r"box", lookup="box")
linter_box_router.register("flash_cart", LinterFlashCartViewSet, basename="linter-flash-cart")

urlpatterns = [

    # حزئیات کلاس ها شامل فصل ها و ادیت یک کلاس و حذف آن
    # path('class-list/<int:pk>/',
    #      LinterClassViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'})),

    #  گرفتن فصول یک کلاس اونایی ک خریدی
    # path('<int:pk>/litner/list/', LinterSeasonViewSet.as_view({'get': 'list'})),

    # {
    # "title": "test",
    # "study_field": "test",
    # "cover_image": null,
    # "price": 10,
    # "description": "test",
    # "myclass": 1,
    # "questions": [{"question_text":"1", "answers_text":"2"}]
    # }
    # ساختن یک فصل
    # path("litner/", LinterSeasonViewSet.as_view({'post': 'create'})),
    # {
    # "title": "test",
    # "study_field": "test",
    # "cover_image": null,
    # "price": 10,
    # "description": "test",
    # "myclass": 1,
    # "questions": [{"question_text":"1", "answers_text":"2"}]
    # }
    # ویرایش، حذف یک فصل و  گرفتن جزئیات یک فصل شامل سوالات
    # در متود گت اگر کاربر در ۲۴ ساعت اخیر آزمون داده باشد جزئیات پاسخ به شرح زیر است:
    # status code: 403
    # response body:
    # {'message': 'you cant take another exam'}
    # path("litner/<int:pk>/", LinterSeasonViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'})),

    # فقط سوالایی که جواب دارن در هر دو حالت برای امتحان یا اصلاج
    # {
    #     "answers": [
    #         {
    #             "question": 1,
    #             "is_correct": true or false
    #         }
    #     ],
    #     "fcm_token": <the_user_firebase_token>
    # }
    # امتحان دادن و اصلاح یک فصل
    # path('list/<int:pk>/', LitnerTakingExam.as_view()),
    # path('list/', LitnerTakingExam.as_view()),

    path("answer/", LinterUserAnswerView.as_view(), name='linter_flash_cart_answer'),
] + router.urls + linter_class_router.urls + linter_session_router.urls + linter_session_router.urls + \
              linter_box_router.urls
