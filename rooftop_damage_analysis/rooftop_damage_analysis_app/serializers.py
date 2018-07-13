from rest_framework import serializers
from .rooftop import rooftop_damage_analysis
from avengers_django_models_app.models import uploadedImages, inferRequests, resultTable


class inferRequestSerializer(serializers.Serializer):
    txnID = serializers.CharField(max_length=50)
    hashes = serializers.ListField(child=serializers.CharField(max_length=32), min_length=1, max_length=5)

    def create(self, validated_data):
        txnID = validated_data['txnID']
        # Verify txnID is correct here
        image_rows = []
        infer_row = inferRequests.objects.get(txnID=txnID)
        print(infer_row)

        # Elimination invalid image hashes
        for hash in validated_data['hashes']:
            try:
                image_rows.append(uploadedImages.objects.get(imageHash=hash))
                print(image_rows)
            except:
                result_row = resultTable.objects.get(txnID_fileHash=txnID + '_' + hash)
                result_row.status = 3
                result_row.result = {'error': 'image does not exist'}
                # EXTREME_CAUTION: fetch infer row with lock update then release lock
                # Here this is okay because no other place will get a inference request with this txnID
                # i.e. Only one process updating the row with this txnID, at this time.
                infer_row.nos_hashes_inferred = infer_row.nos_hashes_inferred + 1
                result_row.save()
        infer_row.save()

        damage_details = []
        for image_entry in image_rows:
            result_row = resultTable.objects.get(txnID_fileHash=txnID + '_' + image_entry.imageHash)
            result_row.status = 1
            result_row.save()

            # Doing computations here for now. Later: Push images to queue here and update status.
            try:
                filename = image_entry.imageHash + '.' + image_entry.imageType
                result_filename = str(txnID) + '_' + image_entry.imageHash + '.png'
                # filepath = os.path.join(settings.ABS_MEDIA_ROOT, 'upload_service/filename')
                damage_ret = rooftop_damage_analysis(filename, result_filename)
                result_filepath = '/media/rooftop_damage_analysis/result/' + result_filename
                damage_ret['result_image'] = result_filepath
                damage_details.append(damage_ret)
                result_row.status = 2
                result_row.result = damage_ret
            except:
                damage_details.append({'error': 'result computation errored'})
                result_row.status = 3
            # EXTREME_CAUTION: fetch infer row with lock update then release lock
            infer_row.nos_hashes_inferred = infer_row.nos_hashes_inferred + 1
            result_row.save()
            infer_row.save()
        # Later return only the txnID, txnID_hash with corresponding status(in queue or errored)
        return {'txnID': validated_data['txnID'], 'damage_details': damage_details}

    class Meta:
        fields = '__all__'
