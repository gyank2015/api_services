from django.urls import path, include
from django.conf import settings
from . import views

urlpatterns = [
    path('shimservice', views.shimEndpoint.as_view(), name='shim_endpoint'),
    # path('rooftopUI', views.infer_requestUI, name='rooftopUI')
]
