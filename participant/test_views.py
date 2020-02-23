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
                              status=Task.ACTIVE,
                              )
        self.test_task.save()

    def test_search_title(self):
        print('**************test_search_title()**************')

        url = reverse('search_on_all_tasks') + \
            "?q=%s&category=title" % self.test_task.title
        response = self.client.get(url)
        task = response.context['resulted_tasks'][0]

        print(task.title)
        self.assertEquals(self.test_task, task)

    def test_search_requester(self):
        print('**************test_search_requester()**************')

        url = reverse('search_on_all_tasks') + \
            "?q=%s&category=requester" % self.test_task.requester.name
        response = self.client.get(url)
        task = response.context['resulted_tasks'][0]

        print(task.requester)
        self.assertEquals(self.test_task, task)

    def test_search_reward(self):
        print('**************test_search_reward()**************')

        url = reverse('search_on_all_tasks') + \
            "?q=%s&category=reward" % self.test_task.reward_amount
        response = self.client.get(url)
        task = response.context['resulted_tasks'][0]

        print(task.reward_amount)
        self.assertEquals(self.test_task, task)

    def test_search_qualification(self):
        print('**************test_search_qualification()**************')

        url = reverse('search_on_all_tasks') + \
            "?q=%s&category=qualifications" % self.test_task.participant_qualifications
        response = self.client.get(url)
        task = response.context['resulted_tasks'][0]

        print(task.participant_qualifications)
        self.assertEquals(self.test_task, task)

    def test_search_end_date(self):
        print('**************test_search_end_date()**************')
        url = reverse('search_on_all_tasks') + \
            "?q=%s&category=end_date" % self.test_task.end_date.strftime(
                "%m/%d/%Y")
        response = self.client.get(url)
        task = response.context['resulted_tasks'][0]

        print(task.end_date)
        self.assertEquals(self.test_task, task)
