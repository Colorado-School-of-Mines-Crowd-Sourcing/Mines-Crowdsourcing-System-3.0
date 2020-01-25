from django.test import TestCase, Client
from django.apps import apps
from django.urls import reverse, reverse_lazy

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


class SeeTasks(TestCase):
    def setUp(self):
        self.client = Client()
        self.see_task_url = reverse('requester_tasks')

    def test_see_GET(self):
        print('**************test_see_GET()******************')

        response = self.client.get(self.see_task_url)
        print('Response status code : ' + str(response.status_code))

        self.assertEquals(response.status_code, 200)


class ApproveContributors(TestCase):
    def setUp(self):
        self.client = Client()

    def test_see_GET_404(self):
        print('**************test_see_GET()******************')

        self.approve_url = reverse_lazy('contributor_approval', args=[1])
        response = self.client.get(self.approve_url)
        print('Response status code : ' + str(response.status_code))

        self.assertEquals(response.status_code, 404)
