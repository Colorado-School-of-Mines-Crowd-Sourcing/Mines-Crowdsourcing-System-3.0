import datetime as d

from django.apps import apps
from django.test import Client, TestCase
from django.urls import reverse

from participant.views import *

from .models import Task, User


class Search(TestCase):
    def setUp(self):
        self.client = Client()
        self.requester = User.objects.create_user('test',
                                                  'requester',
                                                  'requester@test.com',
                                                  1111,
                                                  False)
        self.test_task = Task(link_to='testlink.com',
                              participant_qualifications='some qualifications',
                              reward_amount=12.34,
                              max_num_participants=69,
                              title='Test Task',
                              payment_index=1234,
                              description='a task description',
                              end_date=d.date(2020, 10, 30),
                              requester=User.objects.get(CWID=1111),
                              )
        self.test_task.save()
        self.search_url = reverse('search_on_all_tasks')

    def test_search_title(self):
        print('**************test_search_title()**************')

        url = self.search_url + "?q=Test&category=title"
        response = self.client.get(url)
        print(response.context['resulted_tasks'])
        print(Task.objects.all())

        # self.assertEquals(self.test_task, task)
