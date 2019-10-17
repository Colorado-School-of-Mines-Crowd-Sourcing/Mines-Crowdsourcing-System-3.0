from django.forms import ModelForm
from django.apps import apps


class CreateJob(ModelForm):
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
            'ideal_participant': 'List the qualities you would your participants to possess. Ex: "Freshman, CS Major"',
            'end_date': 'MM/DD/YYYY',
        }
