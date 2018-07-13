from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, authentication, permissions
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import inferRequestSerializer
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import logging
logger = logging.getLogger(__name__)
from django.urls import reverse_lazy
from django.views import generic
from avengers_django_models_app.models import uploadedImages, resultTable , CustomUser ,Token

from avengers_django_models_app.forms import CustomUserCreationForm
from rest_framework import authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
# Create your views here.
from rest_framework.permissions import IsAuthenticated



class infer_request(APIView):
    authentication_classes = (authentication.TokenAuthentication,) #TBD
    # permission_classes = (IsAuthenticated,)


    def get_serializer(self):
        return inferRequestSerializer()

    def post(self, request, format=None):
        serializer = inferRequestSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            response = serializer.save()
            return JsonResponse(response['data'], status=response['status'])
        return JsonResponse({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def infer_requestUI(request):
    if request.method == 'GET':
        # logger.info('rooftop_damage_analysis_app:rooftopUI view hit by user auth-token:')
        token = Token.objects.get(user=request.user)
        print(token.key)
        return render(request, 'car_damage_app/cardamageUI.html',)


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'