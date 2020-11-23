from django.contrib.auth.forms import UserCreationForm
from django.apps import apps

class SignUpForm(UserCreationForm):
    class Meta:
        model = apps.get_model('participant', 'User')
        fields = ['email', 'name', 'CWID', 'sex', 'ethnicity', 'age', 'major']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['major'].label = 'What is your major?'
        self.fields['password1'].help_text = 'You should NOT use your multipass password'
        self.fields['age'].help_text = 'You must be at least 18 to use the Mines Crowdsourcing System'
