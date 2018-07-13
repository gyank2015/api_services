from rest_framework import serializers
# import hashlib
from functools import partial
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
# from PIL import Image
# from .cardamage import carpart_damage_analysis
from avengers_django_models_app.models import uploadedImages, resultTable, inferRequests, infer_requests_status_choices
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.utils import timezone



class imageSerializer(serializers.Serializer):
	txnID_filehash = serializers.CharField(max_length=82)

	def create(self, validated_data):
		txnID_filehash = validated_data['txnID_filehash']
		result = {'result':[],'status':{}}
		result['result'].append({'txnID_filehash':txnID_filehash})
		if len(resultTable.objects.filter(txnID_fileHash=txnID_filehash))==0:
			result['result'] = "image doesnot exist"
			result['status'] = status.HTTP_400_BAD_REQUEST
		else:
			row = resultTable.objects.get(txnID_fileHash=txnID_filehash)
			result['status'] = status.HTTP_201_CREATED
			if row.status==0:
				result['result'] = "file submitted"
			elif row.status == 1:
				result['result'] = "file is being processed"
			else:
				result['result'].append({'result':row.result})
		return result
	class Meta:
		fields = ('txnID_filehash')

class batchSerializer(serializers.Serializer):
	txnID = serializers.CharField(max_length=36)
	def create(self,validated_data):
		txnID = validated_data['txnID']
		result = {'result':[] , 'status' :{}}
		if len(inferRequests.objects.filter(txnID=txnID))==0:
			result['result'] = "Invalid Transaction ID"
			result['status'] = status.HTTP_400_BAD_REQUEST
		else:
			batch = inferRequests.objects.get(txnID=txnID)
			images = batch.fileHashes
			imagelist = images.split(",")
			print(type(imagelist))
			print(imagelist)
			for image in imagelist:
				txnID_filehash = txnID+'_'+image
				print(txnID_filehash)
				response = {'txnID_filehash':{},'result':{}}
				response['txnID_filehash'] = txnID_filehash
				if len(resultTable.objects.filter(txnID_fileHash=txnID_filehash))==0:
					response['result'] = "image doesnot exist"
				else:
					row = resultTable.objects.get(txnID_fileHash=txnID_filehash)
					if row.status == 0:
						response['result'] = "file submitted"
					elif row.status == 1:
						response['result'] = "file is being processed"
					elif row.status == 2:
						response['result'] = row.result
					else:
						response['result'] = row.result
				result['result'].append(response)

			result['status'] = status.HTTP_201_CREATED
		return result
	class Meta:
		fields = ('txnID')

class clusterSerializer(serializers.Serializer):
	imagehashcluster = serializers.CharField(max_length=200)
	txnID = serializers.CharField(max_length=36)
	def create(self,validated_data):
		imagehashcluster = validated_data['imagehashcluster']
		txnID = validated_data['txnID']
		result = {'result':[] , 'status' :{}}
		imagelist = imagehashcluster.split("&")
		print(imagelist)
		for image in imagelist:
			txnID_filehash = txnID+'_'+image
			print(txnID_filehash)
			response = {'txnID_filehash':{},'result':{}}
			response['txnID_filehash'] = txnID_filehash
			if len(resultTable.objects.filter(txnID_fileHash=txnID_filehash))==0:
				response['result'] = "image doesnot exist"
			else:
				row = resultTable.objects.get(txnID_fileHash=txnID_filehash)
				if row.status == 0:
					response['result'] = "file submitted"
				elif row.status == 1:
					response['result'] = "file is being processed"
				elif row.status == 2:
					response['result'] = row.result
				else:
					response['result'] = row.result
			result['result'].append(response)

		result['status'] = status.HTTP_201_CREATED
		return result
	class Meta:
		fields = ('txnID','imagehashcluster')

