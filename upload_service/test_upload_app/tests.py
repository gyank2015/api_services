from rest_framework import status
from rest_framework.test import APITestCase
import os
from io import BytesIO
from PIL import Image
# Create your tests here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_test_image(mode='RGBA', extension='png', size=(5, 5)):
    # https://wildfish.com/blog/2014/02/27/generating-in-memory-image-for-tests-python/
    file = BytesIO()
    image = Image.new(mode, size=size)
    image.save(file, extension)
    file.name = 'test.' + extension
    file.seek(0)
    return file


def open_test_image(filename):
    file = BytesIO()
    print(BASE_DIR)
    path = os.path.join(BASE_DIR, 'test_upload_app/test/testData/' + filename)
    image = Image.open(path)
    extension = filename.split('.')[-1]
    if extension.lower() == 'jpg':
        extension = 'jpeg'
    image.save(file, extension)
    file.name = filename
    file.seek(0)
    return file


class APISanityTestCase(APITestCase):

    def setUp(self):
        pass

    def test_image_min_limit(self):
        response = self.client.post('/test/upload', {'images': []})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_image_max_limit(self):
        response = self.client.post('/test/upload', {'images': [create_test_image(), create_test_image(),
                                                                create_test_image(), create_test_image(), create_test_image(), create_test_image()]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def not_test_image_empty(self):
        response = self.client.post('/test/upload', {'images': [create_test_image(size=(0, 0))]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def not_test_image_max_size(self):
        response = self.client.post('/test/upload', {'images': [create_test_image(size=(5000, 5000))]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ImageFormatCompatibilityTestCase(APITestCase):

    def setUp(self):
        pass

    def test_can_upload_png(self):
        response = self.client.post('/test/upload', {'images': [open_test_image(filename='png_test.png')]})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_upload_jpg(self):
        response = self.client.post('/test/upload', {'images': [open_test_image(filename='jpg_test.jpg')]})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_upload_bmp(self):
        response = self.client.post('/test/upload', {'images': [open_test_image(filename='bmp_test.bmp')]})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_upload_jpeg(self):
        response = self.client.post('/test/upload', {'images': [open_test_image(filename='jpeg_test.jpeg')]})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_upload_jpeg2000(self):
        response = self.client.post('/test/upload', {'images': [open_test_image(filename='jpeg2000_test.jpg')]})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def not_test_can_upload_tiff(self):
        response = self.client.post('/test/upload', {'images': [open_test_image(filename='tiff_test.TIF')]})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
