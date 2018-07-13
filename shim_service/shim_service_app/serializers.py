from rest_framework import serializers
from django.http import JsonResponse
from rest_framework import status
from avengers_django_models_app.models import uploadedImages, inferRequests, resultTable
import requests
from django.conf import settings
import json
import logging
logger = logging.getLogger(__name__)
# import os
# from django.conf import settings

models_list = {
    'rooftop_damage_analysis': 'rooftop',
    'car_damage_detection': 'cardamage',
    # Add any new model name here for reference and
    # add it's corresponding requestParser below
}


class shimEndpointSerializer(serializers.Serializer):
    model = serializers.CharField(max_length=50)
    hashes = serializers.ListField(child=serializers.CharField(max_length=32), min_length=1, max_length=5)
    AuthToken = serializers.CharField(max_length=50)
    futures = {}

    def create(self, validated_data):
        hashes = validated_data['hashes']
        # print(hashes,"**********")
        print (validated_data['model'])
        model_name = validated_data['model'].split(':')[0]
        model_version = ''
        try:
            model_version = validated_data['model'].split(':')[1]
        except Exception as e:
            pass

        # Inserting transaction to DB
        infer_row = inferRequests.objects.create(fileHashes=validated_data['hashes'],
                                                 DLmodel=validated_data['model'],authToken=validated_data['AuthToken'], nos_hashes_submitted=len(validated_data['hashes']))
        infer_row.save()
        txnID = str(infer_row.txnID)

        # Separating valid and invalid hashes
        result_rows = []
        image_rows = []
        valid_hashes = []
        invalid_hashes = []
        # Elimination of invalid image hashes
        for fileHash in validated_data['hashes']:
            try:
                image_rows.append(uploadedImages.objects.get(imageHash=fileHash))
                result_rows.append(resultTable(txnID_fileHash=txnID + '_' + fileHash))
                valid_hashes.append(fileHash)
            except Exception as e:
                invalid_hashes.append(fileHash)
                result_rows.append(resultTable(txnID_fileHash=txnID + '_' + fileHash, status=3, result={'error': 'image does not exist'}))

        # Invalid hash's request end their lifecycle here, with status = errored
        result_rows = resultTable.objects.bulk_create(result_rows)
        # In case all were invalid, we're done
        if len(valid_hashes) < 1:
            return {'txnID': txnID, 'hashes': hashes}, status.HTTP_202_ACCEPTED

        # relay to model's request parsers
        if model_name == 'rooftop_damage_analysis':
            authToken=validated_data['AuthToken']
            print(authToken)
            return self.rooftop_damage_detection_requestParser(model_name, txnID, infer_row, valid_hashes, hashes, model_version,authToken)
        elif model_name == 'car_damage_detection':
            authToken=validated_data['AuthToken']
            print(authToken)
            return self.car_damage_detection_requestParser(model_name, txnID, infer_row, valid_hashes, hashes, model_version,authToken)
        else:
            txnID_fileHash_list = [txnID + '_' + fileHash for fileHash in valid_hashes]
            resultTable.objects.update_or_create(txnID_fileHash__in=txnID_fileHash_list, status=3, result={'error': 'server error'})
            return {'error': 'Invalid model name provided'}, status.HTTP_422_UNPROCESSABLE_ENTITY
        # Shoudln't ever come here, but still...
        return {'error': 'unexpected server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR

    def rooftop_damage_detection_requestParser(self, model_name, txnID, infer_row, valid_hashes, hashes, image_rows,authToken,model_version='latest'):
        # Preparing data for POST to BusinessModel
        host = settings.ROOFTOP_DAMAGE_ANALYSIS_TEST_HOST
        port = settings.ROOFTOP_DAMAGE_ANALYSIS_TEST_PORT
        relative_url = models_list[model_name]
        url = str("http://{}:{}/{}".format(host, port, relative_url))
        data = {
            'txnID': txnID,
            'hashes': valid_hashes
        }
        headers = {'Authorization':'Token '+authToken }
        response = {}
        try:
            response = requests.post(url, data,headers=headers)
        except Exception as e:
            txnID_fileHash_list = [txnID + '_' + fileHash for fileHash in valid_hashes]
            resultTable.objects.update_or_create(txnID_fileHash__in=txnID_fileHash_list, status=3, result={'error': 'server error'})
            return {'txnID': txnID, 'hashes': hashes, 'error': 'model service requested is down'}, status.HTTP_503_SERVICE_UNAVAILABLE

        # Might not need to return hash. doing it just for ease
        if response.status_code == 201:
            return {'txnID': txnID, 'hashes': hashes}, status.HTTP_202_ACCEPTED
        else:
            txnID_fileHash_list = [txnID + '_' + fileHash for fileHash in valid_hashes]
            resultTable.objects.update_or_create(txnID_fileHash__in=txnID_fileHash_list, status=3, result={'error': 'server error'})
            return {'txnID': txnID, 'hashes': hashes, 'error': 'model service requested is down'}, status.HTTP_503_SERVICE_UNAVAILABLE

    def car_damage_detection_requestParser(self, model_name, txnID, infer_row, valid_hashes, hashes, image_rows, authToken,model_version='latest'):
        host = settings.CAR_DAMAGE_ANALYSIS_TEST_HOST
        port = settings.CAR_DAMAGE_ANALYSIS_TEST_PORT
        print(host, port)
        print(model_name)
        relative_url = models_list[model_name]
        url = str("http://{}:{}/{}".format(host, port, relative_url))
        print(url)
        data = {
            'txnID': txnID,
            'hashes': hashes
        }
        print(authToken)
        headers = {'Authorization':'Token '+authToken }
        print (headers)
        print(data)
        response = requests.post(url, data, headers=headers)
        print(response.text)
        return {'txnID': txnID, 'hashes': hashes}, status.HTTP_202_ACCEPTED
        

    class Meta:
        fields = '__all__'
