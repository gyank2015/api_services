from test_upload_app.serializers import testUploadSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework import authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
# Create your views here.


class test_upload(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
     #TBD

    def get_serializer(self):
        return testUploadSerializer()

    def post(self, request, format=None):
        print(request.data)
        AuthToken = request.META['HTTP_AUTHORIZATION']
        request.data['AuthToken'] = AuthToken.split(" ")[1]
        serializer = testUploadSerializer(data=request.data)
        # print(serializer)
        if serializer.is_valid():
            ret = serializer.save()
            return ret
        return JsonResponse({'ret': serializer.errors}, status=400)
