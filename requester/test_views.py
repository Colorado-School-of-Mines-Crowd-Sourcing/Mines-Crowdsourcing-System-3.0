import datetime

from django.apps import apps
from django.test import Client, TestCase
from django.urls import reverse, reverse_lazy

from participant.models import Task, User
from requester.views import *


class Create(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_url = reverse('requester_create')

    def test_create_GET_200(self):
        print('******************test_create_GET_200()**********************')

        response = self.client.get(self.create_url)
        print('Response status code : ' + str(response.status_code))

        self.assertEquals(response.status_code, 200)


class SeeTasks(TestCase):
    def setUp(self):
        self.client = Client()
        self.see_task_url = reverse('requester_tasks')

    def test_see_GET_200(self):
        print('********************test_see_GET_200()************************')

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
                                                  True)
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

    def test_approve_GET_404_no_task(self):
        """
        GIVEN A requester tries to access a task
        WHEN that task does not exist
        THEN a 404 is returned
        """
        print('**************test_approve_GET_404_no task()******************')

        response = self.client.force_login(self.requester)
        approve_url = reverse_lazy('contributor_approval', args=[1000])
        response = self.client.get(approve_url)
        print('Response status code : ' + str(response.status_code))

        self.assertEquals(response.status_code, 404)

    def test_approve_GET_404_invalid_user(self):
        """
        GIVEN A regular user tries to access a task
        WHEN that user is not a requester
        THEN a 404 is returned
        """
        print('************test_approve_GET_404_invalid_user()****************')

        response = self.client.force_login(self.participant)
        approve_url = reverse_lazy('contributor_approval', args=[1])
        response = self.client.get(approve_url)
        print('Response status code : ' + str(response.status_code))

        self.assertEquals(response.status_code, 404)

    def test_approve_GET_200(self):
        """
        GIVEN A requester tries to access a task
        WHEN that requester created that task
        THEN the task is displayed
        """
        print('******************test_approve_GET_200()**********************')

        response = self.client.force_login(self.requester)
        approve_url = reverse_lazy('contributor_approval', args=[1])
        response = self.client.get(approve_url)
        print('Response status code : ' + str(response.status_code))

        self.assertEquals(response.status_code, 200)
