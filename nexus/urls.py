"""
URL configuration for nexus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


@csrf_exempt
def simple_health(request):
    """Ultra simple health check for Railway"""
    return HttpResponse("OK", status=200, content_type="text/plain")


@api_view(['GET'])
@csrf_exempt
def api_root(request):
    """API root endpoint"""
    return Response({
        'message': 'Welcome to Nexus Movie Recommendation API',
        'version': '1.0',
        'endpoints': {
            'movies': '/api/movies/',
            'genres': '/api/genres/',
            'users': '/api/users/',
            'swagger': '/swagger/',
            'redoc': '/redoc/',
            'admin': '/admin/',
        }
    })


@api_view(['GET'])
@csrf_exempt
def health_check(request):
    """Health check endpoint for Railway"""
    return Response({
        'status': 'healthy',
        'service': 'nexus-api',
        'timestamp': timezone.now().isoformat()
    })


schema_view = get_schema_view(
   openapi.Info(
      title="Nexus Movie API",
      default_version='v1',
      description="API documentation for Nexus Movie Recommendation Platform",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', simple_health, name='root-health'),  # Root path for Railway health check
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health-check'),
    path('api/', api_root, name='api-root'),
    path('api/movies/', include('movies.urls')),
    path('api/users/', include('users.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-docs'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
