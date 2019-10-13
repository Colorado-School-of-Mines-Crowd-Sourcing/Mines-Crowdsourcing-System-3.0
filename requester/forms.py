from django.forms import ModelForm

from django.apps import apps

class CreateJob(ModelForm):
    class Meta:
        model = apps.get_model('participant', 'Task')
        exclude = ['requester']

        field_order = [
            'title',
            'min_participant_req',
            'ideal_participant',
            'description',
            'reward_amount',
            'end_date',
            'payment_index',
            'link_to',
        ]

        labels = {
            'min_participant_req' : 'Number of participants',
            'ideal_participant' : 'Participant profile',
            'reward_amount' : 'Reward',
            'link_to' : 'Link to form',
        }
