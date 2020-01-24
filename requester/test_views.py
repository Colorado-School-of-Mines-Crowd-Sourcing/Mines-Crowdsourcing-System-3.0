from django.test import TestCase, Client
from django.apps import apps
from django.urls import reverse

from requester.views import *

class Create(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_url = reverse('requester_create')

    def test_create_GET(self):
        print('**************test_create_GET()******************')

        response = self.client.get(self.create_url)
        print('Response status code : ' + str(response.status_code))

        self.assertEquals(response.status_code, 200)
