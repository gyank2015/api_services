from django.urls import path, include
from django.conf import settings
from . import views

urlpatterns = [
    path('rooftop', views.infer_request.as_view(), name='rooftop'),
    # path('rooftopUI', views.infer_requestUI, name='rooftopUI')
]
