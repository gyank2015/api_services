from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, authentication, permissions
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import shimEndpointSerializer
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import logging
from rest_framework.authentication import TokenAuthentication
logger = logging.getLogger(__name__)
# Create your views here.


class shimEndpoint(APIView):
    authentication_classes = (authentication.TokenAuthentication,) #TBD

    def get_serializer(self):
        return shimEndpointSerializer()

    def post(self, request, format=None):
        AuthToken = request.META['HTTP_AUTHORIZATION']
        print(AuthToken)
        data = request.data.copy()
        data['AuthToken'] = AuthToken.split(" ")[1]
        serializer = shimEndpointSerializer(data=data)
        if serializer.is_valid():
            json_data, status_to_return = serializer.save()
            return JsonResponse(json_data, status=status_to_return, safe=False)
        return JsonResponse({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
