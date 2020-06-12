from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Flora API",
        default_version="v1",
        license=openapi.License(name='GPL-3.0')
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # User management
    path('api/auth/', include('dj_rest_auth.urls')),

    # API v1
    path('api/v1/', include('api.urls')),

    # API Docs
    path('api/docs/', schema_view.with_ui('redoc', cache_timeout=0)),
]

if settings.DEBUG:
    urlpatterns.append(path('api/browsauth/', include('rest_framework.urls')))
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
