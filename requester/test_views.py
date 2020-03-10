from django.test import TestCase, Client
from django.apps import apps
from django.urls import reverse, reverse_lazy
import datetime

from requester.views import *
from participant.models import Task, User


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
        self.requester = User.objects.create_user('test',
                                                  'requester',
                                                  'requester@test.com',
                                                  1111,
                                                  False)
        self.participant = User.objects.create_user('foo',
                                                    'bar',
                                                    'myemail@test.com',
                                                    1234,
                                                    False)
        test_task = Task(link_to='IamAnInvalidLink',
                         participant_qualifications='some qualifications',
                         reward_amount=12.34,
                         max_num_participants=69,
                         title='some task title',
                         payment_index=1234,
                         description='a task description',
                         end_date=datetime.date(2020, 10, 30),
                         requester=User.objects.get(CWID=1111),
                         )
        test_task.save()

    def test_see_GET_404(self):
        print('**************test_see_GET_404_no task()******************')

        self.client.login(username='foo', password='test')
        self.approve_url = reverse_lazy('contributor_approval', args=[1000])
        response = self.client.get(self.approve_url)
        print('Response status code : ' + str(response.status_code))

        self.assertEquals(response.status_code, 404)
