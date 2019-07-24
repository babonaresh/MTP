from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
from .forms import LoginForm,UserRegistrationForm, CityForm, FlightsForm
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.views.generic import TemplateView
import requests
from django.conf import settings
from django.http import JsonResponse

# now = timezone.now()
def home(request):
   return render(request, 'mytrip/home.html',
                 {'mytrip': home})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
            user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'mytrip/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'mytrip/register.html', {'user_form': user_form})




class weather(TemplateView):
    template_name = 'mytrip/weather.html'


    def get(self, request):
        form = CityForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            form = CityForm()
            main_api = 'http://api.openweathermap.org/data/2.5/weather?q='
            api_key = '&units=metric&appid=907d8c401b542c8e7ede79a3ddea8f1a'
            main_api1 = 'http://api.openweathermap.org/data/2.5/forecast?q='
            url1 = main_api1 + city + api_key
            forecast = requests.get(url1).json()
            url= main_api + city + api_key
            json_data= requests.get(url).json()
            if json_data['cod']==200:
                weather_data = []
                city_weather = {
                    'city': city,
                    'temperature': json_data['main']['temp'],
                    'description': json_data['weather'][0]['description'],
                    'icon': json_data['weather'][0]['icon'],
                    'humidity' : json_data['main']['humidity'],
                    'min_temp': json_data['main']['temp_min'],
                    'max_temp': json_data['main']['temp_max'],
                    'wind': json_data['wind']['speed'],
                    'visibility': json_data['visibility'],
                    }
                weather_data.append(city_weather)
                context = {
                    'weather_data': weather_data,
                     'form': form,
                }
                return render(request, self.template_name, context)
            elif forecast['cod']==200:
                context={
                    'forecast':requests.get(url1).json(),
                    'form':form,
                }
                return render(request, self.template_name, context)
            else:
                error='Please Check the Name of the City'
                form= CityForm()
                context={
                    'error':error,
                    'form' : form,
                }
                return render(request, self.template_name, context)

def forecast(self, request):
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            form = CityForm()
            # main_api = 'http://api.openweathermap.org/data/2.5/weather?q='
            # api_key = '&units=metric&appid=907d8c401b542c8e7ede79a3ddea8f1a'
            main_api = 'http://api.openweathermap.org/data/2.5/forecast?q='
            api_key = '&units=metric&appid=907d8c401b542c8e7ede79a3ddea8f1a'
            url= main_api + city + api_key
            json_data= requests.get(url).json()
            if json_data['cod']==200:
                form = CityForm()
                context = {
                    'data': json_data,
                    'form': form,
                }
                return render(request, self.template_name, context)
            else:
                error='Please Check the Name of the City'
                form= CityForm()
                context={
                    'error':error,
                    'form' : form,
                }
                return render(request, self.template_name, context)



class flights(TemplateView):
    template_name = 'mytrip/flights.html'


    def get(self, request):
        # if request.method == 'POST':
        #     radio = form.cleaned_data['one/two']
        #     if radio=='one':
        #         form = FlightsFormOne()
        #         return render(request, self.template_name, {'form': form})
        #     else:
                form = FlightsForm()
                return render(request, self.template_name, {'form': form})

    def post(self, request):
        data = {}
        # if request.method == 'POST':
        form = FlightsForm(request.POST)
        if form.is_valid():
            origin = form.cleaned_data['originplace']
            destination = form.cleaned_data['destinationplace']
            url = 'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/USD/en-US/'+ form.cleaned_data['originplace'] + '/' + form.cleaned_data['destinationplace'] + '/' + (form.cleaned_data['outboundpartialdate']).strftime("%Y-%m-%d")+ '/' + (form.cleaned_data['inboundpartialdate']).strftime("%Y-%m-%d")
            headers = {'X-RapidAPI-Key': settings.RAPIDAPI_API_KEY}
            api_response = requests.get(url, headers=headers)
            if api_response.status_code == 200:
                form = FlightsForm()
                header= "Below are the Details for you Trip"
                context = {
                    'origin': origin,
                    'destination': destination,
                    'data': api_response.json(),
                    'form': form,
                    'header': header,
                }
                return render(request, self.template_name, context)
            else:
                error = 'Please Check the Details you entered'
                form = FlightsForm()
                context = {
                    'error' : error,
                    'form' : form,
                }
                return render(request, self.template_name,context)
