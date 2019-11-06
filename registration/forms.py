from django.contrib.auth.forms import UserCreationForm
from django.apps import apps

class SignUpForm(UserCreationForm):
    class Meta:
        model = apps.get_model('participant', 'User')
        fields = ['multipass_username', 'name', 'CWID']
