from django.urls import path
from markethub.views import MarketHubListView, MarketHubView, QuestionView

urlpatterns = [
#class Markethub
    path("", MarketHubListView.as_view()),
    path("<int:pk>", MarketHubListView.as_view()),
    path('MarketHubQuestionPaid/<int:pk>',MarketHubListView.as_view()),
  
    path('update/<int:pk>', MarketHubView.as_view()),
    path('delete/<int:pk>', MarketHubView.as_view()),
    path('detail/<int:pk>',MarketHubView.as_view()),

    path('question/<int:pk>', QuestionView.as_view()),
]
