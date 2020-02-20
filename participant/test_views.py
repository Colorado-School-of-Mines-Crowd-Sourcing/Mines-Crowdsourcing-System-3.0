from django.test import TestCase, Client
from django.apps import apps
from django.urls import reverse, reverse_lazy
import datetime

from .models import Task, User


class Search(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_url = reverse('all_tasks')
        self.requester = User.objects.create_user('test',
                                                  'requester',
                                                  'requester@test.com',
                                                  1111,
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
