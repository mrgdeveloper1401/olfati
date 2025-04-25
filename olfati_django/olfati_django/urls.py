from django.contrib import admin
from django.core.files import images
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from olfati_django.settings import MEDIA_URL, MEDIA_ROOT, DEBUG

v1_api = [
    path('v1/account/', include('accounts.urls')),
    path('v1/exam/', include('exam.urls')),
    path('v1/linter/', include('litner.urls')),
    path('v1/markethub/', include('markethub.urls')),
    path("v1/images/", include('catalog_app.urls')),
]

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('admin/', admin.site.urls),
]  + v1_api


if DEBUG:
    from django.conf.urls.static import static
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()
