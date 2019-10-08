from django import forms

class CreateJob(forms.Form):
        form_url = forms.CharField(label='Form URL', max_length=50)
        reward_amount = forms.DecimalField(max_digits=5, decimal_places=2)
        min_participant_req = forms.IntegerField()
        title = forms.CharField(max_length=100, )
        payment_index = forms.IntegerField()
        description = forms.CharField(max_length=1024, )
        posted_date = forms.DateField()
        end_date = forms.DateField()
