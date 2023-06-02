from django.urls import path

from markethub.views import MarketHubListView

urlpatterns = [
    path("", MarketHubListView.as_view()),
    path("<int:pk>", MarketHubListView.as_view()),
]
