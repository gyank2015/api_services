from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, authentication, permissions
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import imageSerializer ,batchSerializer, clusterSerializer
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import logging
logger = logging.getLogger(__name__)
from avengers_django_models_app.models import uploadedImages, resultTable, inferRequests
from django.http import HttpResponse
import requests
import json

# Create your views here.


class image_result(APIView):
    def get(self,request,*args,**kwargs):
    	txnID_filehash=kwargs['txnID']+ '_'+ kwargs['hash']
    	print(txnID_filehash)
    	serializer = imageSerializer(data={'txnID_filehash':txnID_filehash})
    	if serializer.is_valid():
    		response = serializer.save()
    		return JsonResponse(response['result'], status=response['status'],safe=False)
    	else:
    		print("invalid serializer")

    		return JsonResponse({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




class batch_result(APIView):
	def get(self,request,*args,**kwargs):
		txnID=kwargs['txnID']
		print(txnID)
		serializer = batchSerializer(data = {'txnID':txnID})
		if serializer.is_valid():
			response = serializer.save()
			return JsonResponse(response['result'], status=response['status'],safe=False)
		else:
			print("invalid serializer")
			return JsonResponse({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


def resultUI(request, txnID):
	if request.method=='GET':
		images = inferRequests.objects.get(txnID=txnID).fileHashes
		imagelist = images.split(",")
		return render(request,'result_api_app/index.html',{'imagelist':imagelist, 'txnID':txnID})
	else:
		# print(request.POST['txnID'])
		txnIDlist = request.POST.getlist('txnID')
		# print(txnID)
		imagehashes = request.POST.getlist('imagehash')
		if len(txnIDlist)==0:
			imagehashcluster =""
			for image in imagehashes:
				imagehashcluster += (image+'&')
			imagehashcluster = imagehashcluster [:-1]
			imagehashes = imagehashcluster.split("&")
			url = 'http://172.16.28.59:3130/result/list/'+txnID+'/'+imagehashcluster
			r = requests.request('GET', url, data = {'txnID':txnID , 'imagehashcluster':imagehashcluster})
			json_data = json.loads(r.text)
			return JsonResponse(json_data,safe = False)
		else :
			url = 'http://172.16.28.59:3130/result/list/'+txnIDlist[0]
			r = requests.request('GET' , url , data = {'txnID':txnIDlist[0]})
			json_data = json.loads(r.text)
			return JsonResponse(json_data ,safe =False)


class imagehash_cluster_result(APIView):
	def get(self,request,*args,**kwargs):
		imagehashcluster=kwargs['imagehashcluster']
		txnID = kwargs['txnID']
		print(imagehashcluster)
		serializer = clusterSerializer(data = {'imagehashcluster':imagehashcluster,'txnID':txnID})
		if serializer.is_valid():
			response = serializer.save()
			return JsonResponse(response['result'], status=response['status'],safe=False)
		else:
			print("invalid serializer")
			return JsonResponse({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




# @csrf_exempt
# def infer_requestUI(request):
#     if request.method == 'GET':
#         # logger.info('rooftop_damage_analysis_app:rooftopUI view hit by user auth-token:')
#         return render(request, 'car_damage_app/cardamageUI.html',)
