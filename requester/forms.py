from django.forms import ModelForm

from django.apps import apps

class CreateJob(ModelForm):
    class Meta:
        model = apps.get_model('participant', 'Task')
        exclude = ['requester']

        labels = {
            'min_participant_req' : 'Number of participants',
            'ideal_participant' : 'Participant profile',
            'reward_amount' : 'Reward',
            'link_to' : 'Link to form',
        }
