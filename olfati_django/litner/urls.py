from django.urls import path

from litner.views import LitnerListView, LitnerView, ListCreateMyClassView

urlpatterns = [
    path('class-list/', ListCreateMyClassView.as_view({'get': 'list'})),
    path('class-list/<int:pk>/', ListCreateMyClassView.as_view({'get': 'retrieve'})),
    path("list", LitnerListView.as_view()),
    path("<int:pk>", LitnerListView.as_view()),
    path("list/<int:pk>/", LitnerListView.as_view()),
    path("", LitnerView.as_view()),
   # path("kar-name/", LitnerKarNameView.as_view())

]
