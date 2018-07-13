from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import logging
logger = logging.getLogger(__name__)
from django.urls import reverse_lazy
from django.views import generic
from avengers_django_models_app.models import uploadedImages, resultTable , CustomUser ,Token

from avengers_django_models_app.forms import CustomUserCreationForm
import requests
from rest_framework.authentication import TokenAuthentication
from rest_framework import authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required



@csrf_exempt
@login_required(login_url='/login/')
def test_test_upload(request):
	if request.method == 'GET':
	    # print(response.text)
	    token = Token.objects.get(user=request.user)
	    print(token.key)
	    AuthToken  = 'Token '+token.key
	    print(AuthToken)
	    return render(request, 'test_upload/test_test_upload.html' , {'Token':AuthToken})
	if request.method == 'POST':
		return HttpResponse('<h1> Your files have been uploaded !</h1>')


class SignUp(generic.CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'signup.html'