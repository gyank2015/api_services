from rest_framework import status
from rest_framework.test import APITestCase
import os
# Create your tests here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class APISanityTestCase(APITestCase):

    def setUp(self):
        pass
