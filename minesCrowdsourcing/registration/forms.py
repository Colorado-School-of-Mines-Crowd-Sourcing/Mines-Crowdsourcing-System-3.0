from django.contrib.auth.forms import UserCreationForm
from django.apps import apps

class SignUpForm(UserCreationForm):
    class Meta:
        model = apps.get_model('participant', 'User')
        fields = ['multipass_username', 'name', 'CWID']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['password1'].help_text = 'You should NOT use your multipass password'
