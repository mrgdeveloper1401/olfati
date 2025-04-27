from rest_framework import routers
from . import views

router = routers.DefaultRouter()

# router.register(r'user_images', views.ImageViewSet, basename='image')

urlpatterns = []
urlpatterns += router.urls
