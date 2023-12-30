from django.urls import path

from litner.views import LitnerListView, LitnerView, ListCreateMyClassView,LitnerTakingExam,ListProfileMyClassView,ListProfileMyClassCreatorView

urlpatterns = [
   
    path("list/<int:pk>/", LitnerTakingExam.as_view()),
    path("class-list/", ListCreateMyClassView.as_view({'get': 'list'})),
    path("class-list/<int:pk>/", ListCreateMyClassView.as_view({'get': 'retrieve'})),
    #  گرفتن فصول یک کلاس اونایی ک خریدی
    path('<int:pk>/litner/list/', LitnerListView.as_view({'get': 'list'})),
    # ساختن یک فصل
    path("litner/", LitnerListView.as_view({'post': 'create'})),
    # ویرایش، حذف یک فصل و  گرفتن جزئیات یک فصل شامل سوالات
    path("litner/<int:pk>/", LitnerListView.as_view({'get':'retrieve', 'put':'partial_update', 'delete': 'destroy'})),
    path('profile/class-list/', ListProfileMyClassView.as_view()),
    path('profile/my-class-list/', ListProfileMyClassCreatorView.as_view()),
  

]
