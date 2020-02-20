from django.test import TestCase, Client
from django.apps import apps
from django.urls import reverse
import datetime as d

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
        self.search_url = reverse('participant_all_tasks')

    def test_search_title(self):
        print('**************test_search_title()**************')

        response = self.client.get(self.search_url)
        print(self.search_url)

        print(response.context[-1]['all_tasks'])
        task = response.context[-1]['all_tasks'][0]

        self.assertEquals(self.test_task, task)
