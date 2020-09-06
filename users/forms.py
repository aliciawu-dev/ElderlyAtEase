from django.forms import ModelForm 
from django.contrib.auth.models import User
from django import forms
from .models import Profile, VerifyInfo

class ProfileEditForm(ModelForm): 
    class Meta: 
        model = Profile 
        fields = ['full_name', 'bio', 'location', 'image', 'caretaker']

class VerificationInfoForm(ModelForm):
    via = forms.ChoiceField(choices=[('sms', 'SMS'), ('call', 'Call')])

    def __init__(self, *args, **kwargs): 
        super(VerificationInfoForm, self).__init__(*args, **kwargs) 

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['phone_number'] = 'form-control'
        self.fields['country_code'].widget.attrs['country_code'] = 'form-control'

    class Meta: 
        model = VerifyInfo 
        fields = ['email', 'phone_number', 'country_code']

class VerificationTokenForm(forms.Form): 
    token = forms.CharField()