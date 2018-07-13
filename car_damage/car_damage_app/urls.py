from django.urls import path, include
from django.conf import settings
from . import views
from django.contrib.auth.views import login
# from rest_framework.authtoken.models import Token
from . import views

urlpatterns = [
    path('cardamage', views.infer_request.as_view(), name='cardamage'),
    path('cardamageUI', views.infer_requestUI, name='cardamageUI'),
    path('signup/', views.SignUp.as_view(), name='signup'),

]

from rest_framework.authtoken import views

    
urlpatterns+=[path('api-token-auth/', views.obtain_auth_token)]