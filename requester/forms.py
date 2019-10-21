from django import forms
from django.forms import ModelForm, Form
from django.apps import apps


class CreateTask(ModelForm):
    class Meta:
        model = apps.get_model('participant', 'Task')
        exclude = ['requester']

        labels = {
            'min_participant_req': 'Number of participants',
            'ideal_participant': 'Participant profile',
            'reward_amount': 'Reward',
            'link_to': 'Link to Google Form',
        }

        help_texts = {
            'min_participant_req': 'This is the minimum number.',
            'ideal_participant': 'List the qualities you want your participants to possess. Ex: "Freshman, CS Major"',
            'end_date': 'MM/DD/YYYY',
        }

class CreateTags(Form):
    tags = forms.Charfield(label="Tags")
