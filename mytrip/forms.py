from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class CityForm(forms.Form):
    city = forms.CharField(required=True,label='City',)

codes = (
    ('',''),
    ('SFO', 'SFO-San Francisco'),
    ('ORD', 'ORD-Chicago'),
    ('MIA', 'MIA-Miami'),
    ('DEN','DEN-Denver'),
)
class FlightsForm(forms.Form):
    originplace = forms.ChoiceField(label='Origin', required=True, choices=codes,)
    destinationplace = forms.ChoiceField(label='Destination',choices=codes, required=True,)
    outboundpartialdate = forms.DateField(label='Outbound Date', widget=forms.SelectDateWidget(empty_label="Nothing"), required=True)
    inboundpartialdate = forms.DateField(label='Inbound Date', widget=forms.SelectDateWidget(empty_label="Nothing"), required=True )

