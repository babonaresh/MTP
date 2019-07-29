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
    ('SFO', 'San Francisco International Airport-San Francisco'),
    ('ORD', 'O-Hare International Airport-Chicago'),
    ('MDW','Midway International Airport-Chicago'),
    ('MIA', 'Miami International Airport-Miami'),
    ('DEN','Denver International Airport-Denver'),
    ('ATL', 'Hartsfield–Jackson Atlanta International Airport-Atlanta'),
    ('LAX', 'Los Angeles International Airport-Los Angeles'),
    ('DFW', 'Dallas/Fort Worth International Airport-Dallas'),
    ('MSP', 'Minneapolis–Saint Paul International Airport-Minneapolis'),
    ('DTW', 'Detroit Metropolitan Airport- Detroit'),
    ('PHL','Philadelphia International Airport-Philadelphia'),
    ('LGA','LaGuardia Airport-New York'),
    ('BWI','Baltimore–Washington International Airport-Baltimore'),
    ('SLC','Salt Lake City International Airport-Salt Lake City'),
    ('DCA', 'Ronald Reagan Washington National Airport-Washington, D.C.'),
    ('SAN', 'San Diego International Airport-San Diego'),
    ('TPA', 'Tampa International Airport-Tampa'),
    ('HNL', 'Daniel K. Inouye International Airport-Honolulu'),
    ('PDX', '	Portland International Airport-Portland'),
    ('FLL', 'Fort Lauderdale–Hollywood International Airport-Fort Lauderdale'),
    ('BOS', 'Logan International Airport-Boston'),
    ('IAH','George Bush Intercontinental Airport-Houston'),
    ('PHX','Phoenix Sky Harbor International Airport-Phoenix'),
    ('MCO','Orlando International Airport-Orlando'),
    ('EWR','Newark Liberty International Airport-'),
    ('CLT','Charlotte Douglas International Airport-'),
    ('SEA','Seattle–Tacoma International Airport-'),
    ('LAS','McCarran International Airport-'),
    ('JFK','John F. Kennedy International Airport-'),
)
class FlightsForm(forms.Form):
    originplace = forms.ChoiceField(label='Origin', required=True, choices=codes,)
    destinationplace = forms.ChoiceField(label='Destination',choices=codes, required=True,)
    outboundpartialdate = forms.DateField(label='Outbound Date', widget=forms.SelectDateWidget(empty_label="Nothing"), required=True)
    inboundpartialdate = forms.DateField(label='Inbound Date', widget=forms.SelectDateWidget(empty_label="Nothing"), required=True )

