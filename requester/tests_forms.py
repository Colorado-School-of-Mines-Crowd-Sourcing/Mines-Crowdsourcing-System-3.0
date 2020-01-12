from django.test import TestCase
from django.apps import apps
import datetime

from requester.forms import *

# Create your tests here.
class CreateTaskTest(TestCase):

    def test_valid_entry(self):
        data = {
            'link_to': 'https://leoiscool.com',
            'participant_qualifications': 'some qualifications',
            'reward_amount': 12.34,
            'max_num_participants': 69,
            'title': 'some task title',
            'payment_index': 1234,
            'description': 'a task description',
            'end_date': datetime.date(2020, 10, 30),
            'tags': 'some, tags',
        }
        form = CreateTask(data)
        self.assertTrue(form.is_valid())

    def test_invalid_link(self):
        data = {
            'link_to': 'IamAnInvalidLink',
            'participant_qualifications': 'some qualifications',
            'reward_amount': 12.34,
            'max_num_participants': 69,
            'title': 'some task title',
            'payment_index': 1234,
            'description': 'a task description',
            'end_date': datetime.date(2020, 10, 30),
            'tags': 'some, tags',
        }
        form = CreateTask(data)
        self.assertFalse(form.is_valid())
