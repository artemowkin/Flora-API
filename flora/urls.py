from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # User management
    path('api/auth/', include('dj_rest_auth.urls')),

    # API v1
    path('api/v1/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns.append(path('api/browsauth/', include('rest_framework.urls')))
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
