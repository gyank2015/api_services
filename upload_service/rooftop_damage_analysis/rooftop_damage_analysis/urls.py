"""rooftop_damage_analysis URL Configuration

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
# from . import views
from rest_framework_swagger.views import get_swagger_view
from django.conf import settings

schema_view = get_swagger_view(title='rooftop damage analysis')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view),
    path('', include('rooftop_damage_analysis_app.urls'), name='infer')
]
