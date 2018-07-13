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
# Create your views here.


class infer_request(APIView):
    authentication_classes = (authentication.TokenAuthentication,) #TBD

    def get_serializer(self):
        return inferRequestSerializer()

    def post(self, request, format=None):
        print(request.data)
        serializer = inferRequestSerializer(data=request.data)

        if serializer.is_valid():
            ret = serializer.save()
            return JsonResponse(ret, status=status.HTTP_201_CREATED)
        return JsonResponse({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def infer_requestUI(request):
    if request.method == 'GET':
        logger.info('rooftop_damage_analysis_app:rooftopUI view hit by user auth-token:')
        return render(request, 'rooftop_damage_analysis_app/rooftopUI.html',)
