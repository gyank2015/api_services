from rest_framework import serializers
import hashlib
from functools import partial
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from PIL import Image
from .cardamage import carpart_damage_analysis
from avengers_django_models_app.models import uploadedImages, resultTable , CustomUser ,Token
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.utils import timezone



class inferRequestSerializer(serializers.Serializer):
    hashes = serializers.ListField(child=serializers.CharField(max_length=32), min_length=1, max_length=5)
    txnID = serializers.CharField(max_length=50)
    def create(self, validated_data):
        data = {'result':validated_data['txnID'], 'damage_details':[]}
        flag=0
        response = {'data':{},'status':{}}
        for hash in validated_data['hashes']:
            if len(uploadedImages.objects.filter(imageHash=hash))==0:
                damage_details=[]
                damage_details.append({'imageID':hash})
                damage_details.append({'error':"Image not found"})
                data['damage_details'].append(damage_details)
                flag=1
                continue
            else:
                image = uploadedImages.objects.filter(imageHash=hash)[0]
            filename = image.imageHash + '.' + image.imageType
            print(filename)
            txnID_fileHash = validated_data['txnID']+ '_'+ hash
            # resultTable.objects.create(txnID_fileHash = txnID_fileHash)
            damage_details = carpart_damage_analysis(filename)
            data_row = resultTable.objects.filter(txnID_fileHash=txnID_fileHash)[0]
            data_row.result = damage_details
            data_row.completeTS = timezone.now()
            data_row.status = 2
            data_row.save()
            print(type(damage_details))
            data['damage_details'].append(damage_details)
        if flag==1:
            response['data']=data
            response['status']=status.HTTP_207_MULTI_STATUS
            print("insufficient data found")
            return response
        else:
            response['data']=data
            response['status']=status.HTTP_201_CREATED
            print("all good!!")
            return response
    class Meta:
        fields = '__all__'
