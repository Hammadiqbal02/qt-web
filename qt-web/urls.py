from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from rest_framework.authentication import TokenAuthentication
from drf_yasg import openapi
from django.conf.urls.static import static
from django.conf import settings
schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="Api URls",
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(r'^swagger(?P<format>\.json|\.yaml)$',
     schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger',
                             cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('accounts/', admin.site.urls),
    path('user/', include('account.urls')),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)