from rest_framework import serializers
from avengers_django_models_app.models import uploadedImages, CustomUser ,Token
import hashlib
from functools import partial
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from PIL import Image


def hash_image(file, block_size=65536):
    # Utility function to hash images
    hasher = hashlib.md5()
    for buf in iter(partial(file.read, block_size), b''):
        hasher.update(buf)

    return hasher.hexdigest()


class uploadedImagesSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return uploadedImages.objects.create(**validated_data)

    class Meta:
        model = uploadedImages
        fields = ('imageHash', 'imageType', 'uploadedBy')


class testUploadSerializer(serializers.Serializer):
    # use_url gives file url, i.e. MEDIA_URL + filename
    images = serializers.ListField(child=serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True), min_length=1, max_length=5)
    AuthToken = serializers.CharField(max_length=50)
    def create(self, validated_data):
        images = validated_data.get('images')
        # print(validated_data)
        images_to_upload = []
        uploadedHashes = []

        # Save each image
        for image in images:

            # Creating data for the image to be added to DB
            imageHash = hash_image(image)
            if uploadedImages.objects.filter(imageHash=imageHash).count() > 0:
                uploadedHashes.append(imageHash)
                continue

            image_name = image.name
            image_extension = image_name.split('.')[-1]

            data = {
                'imageHash': imageHash,
                'imageType': image_extension,
                'uploadedBy': validated_data['AuthToken'],
            }
            # Try to write file to volume
            image.seek(0)
            try:
                image.name = imageHash + '.' + image_extension

                path = default_storage.save(str(image), ContentFile(image.read()))
            except Exception as e:
                return JsonResponse({'error': 'image save failed'}, status=400)

            # For use ListSerializer in future for bulk upload
            images_to_upload.append(data)

            uploaded_image_serializer = uploadedImagesSerializer(data=data)
            # uploaded_image_serializer.create(image_data)
            if uploaded_image_serializer.is_valid():
                ret = uploaded_image_serializer.save()
                uploadedHashes.append(imageHash)
            else:
                return JsonResponse({'error': 'uploaded_image_serializer.errors'}, status=400)

        # Returns hash of images in case there's no error
        # otherwise the error has to be returned above
        return JsonResponse({'hashes': uploadedHashes}, status=201)
