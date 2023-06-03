from django.urls import path

from markethub.views import MarketHubListView,MarketHubView

urlpatterns = [
    path("", MarketHubListView.as_view()),
    path("<int:pk>", MarketHubListView.as_view()),
    path('update/<int:pk>',MarketHubView.as_view()),
    path('delete/<int:pk>',MarketHubView.as_view())
]
