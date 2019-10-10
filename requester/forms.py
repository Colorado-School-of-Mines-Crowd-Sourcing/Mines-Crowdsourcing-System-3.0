from django.forms import ModelForm

from django.apps import apps

class CreateJob(ModelForm):
    class Meta:
        model = apps.get_model('participant', 'Task')
        exclude = ['requester']
