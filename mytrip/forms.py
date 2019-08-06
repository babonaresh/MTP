from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

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
    ('SFO-San Francisco', 'San Francisco International Airport-San Francisco'),
    ('ORD-Chicago', 'O-Hare International Airport-Chicago'),
    ('MDW-Chicago', 'Midway International Airport-Chicago'),
    ('MIA-Miami', 'Miami International Airport-Miami'),
    ('DEN-Denver', 'Denver International Airport-Denver'),
    ('ATL-Atlanta', 'Hartsfield–Jackson Atlanta International Airport-Atlanta'),
    ('LAX-Los Angeles', 'Los Angeles International Airport-Los Angeles'),
    ('DFW-Dallas', 'Dallas/Fort Worth International Airport-Dallas'),
    ('MSP-Minneapolis', 'Minneapolis–Saint Paul International Airport-Minneapolis'),
    ('DTW-Detroit', 'Detroit Metropolitan Airport- Detroit'),
    ('PHL-Philadelphia', 'Philadelphia International Airport-Philadelphia'),
    ('LGA-New York', 'LaGuardia Airport-New York'),
    ('BWI-Baltimore', 'Baltimore–Washington International Airport-Baltimore'),
    ('SLC-Salt Lake City', 'Salt Lake City International Airport-Salt Lake City'),
    ('DCA-Washington, D.C.', 'Ronald Reagan Washington National Airport-Washington, D.C.'),
    ('SAN-San Diego', 'San Diego International Airport-San Diego'),
    ('TPA-Tampa', 'Tampa International Airport-Tampa'),
    ('PDX-Portland', '	Portland International Airport-Portland'),
    ('FLL-Fort Lauderdale', 'Fort Lauderdale–Hollywood International Airport-Fort Lauderdale'),
    ('BOS-Boston', 'Logan International Airport-Boston'),
    ('IAH-Houston', 'George Bush Intercontinental Airport-Houston'),
    ('PHX-Phoenix', 'Phoenix Sky Harbor International Airport-Phoenix'),
    ('MCO-Orlando', 'Orlando International Airport-Orlando'),
    ('EWR-Newark', 'Newark Liberty International Airport-Newark'),
    ('CLT-Charlotte', 'Charlotte Douglas International Airport-Charlotte'),
    ('SEA-Seattle', 'Seattle–Tacoma International Airport-Seattle'),
    ('LAS-Las Vegas', 'McCarran International Airport-Las Vegas'),
    ('JFK-New York', 'John F. Kennedy International Airport- New York'),
)
class FlightsForm(forms.Form):
    originplace = forms.ChoiceField(label='Origin', required=True, choices=codes,)
    destinationplace = forms.ChoiceField(label='Destination',choices=codes, required=True,)
    outboundpartialdate = forms.DateField(widget=forms.DateInput(
                attrs={'type': 'date'}
            ), required=True, label= 'Start Date')
    inboundpartialdate = forms.DateField(widget=forms.DateInput(
                attrs={'type': 'date'}
            ),required=True, label= 'End Date')


class ZomatoForm(forms.Form):
    searchkeyword = forms.CharField()
    cuisines = forms.CharField()

class Hotels(forms.Form):
    city = forms.CharField(required=True, label='Destination City')
    indate = forms.DateField(widget=forms.DateInput(
                attrs={'type': 'date'}
            ), required=True, label= 'Start Date')
    outdate = forms.DateField(widget=forms.DateInput(
                attrs={'type': 'date'}
            ),required=True, label= 'End Date')

