"""upload_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from . import views
from rest_framework_swagger.views import get_swagger_view
from django.conf import settings


schema_view = get_swagger_view(title='Upload Service API')
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('swagger/', schema_view),
    path('admin/', admin.site.urls),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('test/', include('test_upload_app.urls'), name='test_upload_app'),
]

if settings.DEBUG == True:
    urlpatterns.append(path('test/test/upload/', views.test_test_upload, name='test_test_upload'))


from rest_framework.authtoken import views
urlpatterns+=[path('api-token-auth/', views.obtain_auth_token)]
