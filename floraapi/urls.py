from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('api/v1/auth/', include('accounts.urls')),

    # ReDoc
    path('redoc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema-url': 'openapi-schema'}
    ), name='redoc'),

    # Local
    path('api/v1/projects/', include('projects.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
