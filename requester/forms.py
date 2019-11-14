from django import forms
from django.forms import ModelForm, Form
from django.apps import apps


class CreateTask(ModelForm):

    tags = forms.CharField(label='Tags', max_length=40, help_text='Separate your tags with a comma')

    class Meta:
        model = apps.get_model('participant', 'Task')
        exclude = ['requester', 'participants', 'status']

        labels = {
            'max_num_participants': 'Maximum Number of Participants',
            'participant_qualifications': 'Participant Qualifications',
            'reward_amount': 'Reward ',
            'link_to': 'Link to Google Form',
        }

        help_texts = {
            'participant_qualifications': 'List the qualities you want your participants to possess. Ex: "Freshman, CS Major"',
            'reward_amount': 'Amount of compensation (in $) per task per participant',
            'end_date': 'MM/DD/YYYY',
        }


class CreateApproval(ModelForm):
    class Meta:
        model = apps.get_model('participant', 'Task')
        fields = ['participants']

    def __init__(self, participants_set=None, *args,**kwargs):
        participants_set = kwargs.pop('participants_set', None)
        super(CreateApproval,self).__init__(*args,**kwargs)
        self.fields['participants'] = forms.ModelMultipleChoiceField(
                                        queryset=participants_set,
                                        widget=forms.CheckboxSelectMultiple,
                                        to_field_name='name',)
