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
    originplace = forms.ChoiceField(label='Origin',required=True, choices=codes,widget=forms.Select(attrs={'class':'myForm ','placeholder': 'Origin Airport'}))
    destinationplace = forms.ChoiceField(label='Destination',choices=codes, required=True,widget=forms.Select(attrs={'class':'myForm ','placeholder': 'Destination Airport '}))
    outboundpartialdate = forms.DateField(widget=forms.DateInput(
                attrs={'type': 'date', 'class':'myForm date'}
            ), required=True, label= 'Start Date')
    inboundpartialdate = forms.DateField(widget=forms.DateInput(
                attrs={'type': 'date','class':'myForm date'}
            ),required=True, label= 'End Date')
city = (
    ('',''),
    ('San Francisco', 'San Francisco'),
    ('Chicago', 'Chicago'),
    ('Miami', 'Miami'),
    ('Denver', 'Denver'),
    ('Atlanta', 'Atlanta'),
    ('Los Angeles', 'Los Angeles'),
    ('Dallas', 'Dallas'),
    ('Minneapolis', 'Minneapolis'),
    ('Detroit', 'Detroit'),
    ('Philadelphia', 'Philadelphia'),
    ('New York', 'New York'),
    ('Baltimore', 'Baltimore'),
    ('Salt Lake City', 'Salt Lake City'),
    ('Washington, D.C.', 'Washington, D.C.'),
    ('San Diego', 'San Diego'),
    ('Tampa', 'Tampa'),
    ('Portland', 'Portland'),
    ('Fort Lauderdale', 'Fort Lauderdale'),
    ('Boston', 'Boston'),
    ('Houston', 'Houston'),
    ('Phoenix', 'Phoenix'),
    ('Orlando', 'Orlando'),
    ('Newark', 'Newark'),
    ('Charlotte', 'Charlotte'),
    ('Seattle', 'Seattle'),
    ('Las Vegas', 'Las Vegas'),
    ('New York', 'New York'),
)
class Location(forms.Form):
    originplace = forms.ChoiceField(label='Origin',required=True, choices=city,widget=forms.Select(attrs={'class':'myForm ','placeholder': 'Origin Airport'}))
    destinationplace = forms.ChoiceField(label='Destination',choices=city, required=True,widget=forms.Select(attrs={'class':'myForm ','placeholder': 'Destination Airport '}))

class SMS(forms.Form):
    phone = forms.CharField(label='Number',required=True,widget=forms.TextInput(attrs={'class':'myForm '}))
    body = forms.CharField(label='body', required=True,widget=forms.TextInput(attrs={'class':'myForm '}))

cities = (
        ('', 'Select a City'),
        ('306', 'San Francisco'),
        ('292', 'Chicago'),
        ('291', 'Miami'),
        ('305', 'Denver'),
        ('288', 'Atlanta'),
        ('281', 'Los Angeles'),
        ('276', 'Dallas'),
        ('5570', 'Minneapolis'),
        ('285', 'Detroit'),
        ('287', 'Philadelphia'),
        ('280', 'New York'),
        ('787', 'Baltimore'),
        ('1213', 'Salt Lake City'),
        ('283', 'Washington, D.C.'),
        ('302', 'San Diego'),
        ('604', 'Tampa'),
        ('286', 'Portland'),
        ('586', 'Fort Lauderdale'),
        ('289', 'Boston'),
        ('277', 'Houston'),
        ('301', 'Phoenix'),
        ('601', 'Orlando'),
        ('3976', 'Newark'),
        ('303', 'Charlotte'),
        ('279', 'Seattle'),
        ('282', 'Las Vegas'),
    )

class ZomatoForm(forms.Form):
    searchkeyword = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'myForm '}))
    cuisines = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'myForm '}))
    citiesList = forms.ChoiceField(label='Cities', required=False, choices=cities,widget=forms.Select(attrs={'class':'myForm '}))


class Hotels(forms.Form):
    city = forms.CharField(required=True, label='Destination City',widget=forms.TextInput(attrs={'class':'myForm '}))
    indate = forms.DateField(widget=forms.DateInput(
                attrs={'type': 'date', 'class':'myForm date'}
            ), required=True, label= 'Start Date')
    outdate = forms.DateField(widget=forms.DateInput(
                attrs={'type': 'date', 'class':'myForm date'}
            ),required=True, label= 'End Date')

