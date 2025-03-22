"""
URL configuration for project project.

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
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view as swagger_get_schema_view

# Define schema view for Swagger documentation
schema_view = swagger_get_schema_view (
   openapi.Info(
      title="API",
      default_version='1.0.0',
      description="API for managing and details models.",
    #   terms_of_service="https://www.google.com/policies/terms/",
    #   contact=openapi.Contact(email="contact@dietapi.local"),
    #   license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('api-auth/', include('rest_framework.urls')),
    path("accounts/", include("allauth.urls")),
    path('diet/', include(('diet.urls'), namespace='diet')),
    # path('medication/', include(('medication.urls'), namespace='medication')),
    # path('footcare/', include(('footcare.urls', 'footcare'), namespace='footcare')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    
    ] 

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
