from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
from .forms import LoginForm,UserRegistrationForm, CityForm, FlightsForm, ZomatoForm
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
            if (json_data['cod']==200) & (forecast['cod']== "200"):
                # print(forecast)
                # print(json_data)
                weather_data = []
                forecast_data=[]
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
                forecast_weather= {
                    'list': forecast['list'],
                }
                # print(forecast_weather)
                weather_data.append(city_weather)
                forecast_data.append(forecast_weather)
                context = {
                    'weather_data': weather_data,
                    'form': form,
                    'forecast_data':forecast_data,
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
                form = FlightsForm()
                return render(request, self.template_name, {'form': form})



    def post(self, request):
        # if request.method == 'POST':
        form = FlightsForm(request.POST)
        if form.is_valid():
            input1 = form.cleaned_data['originplace']
            origin,orgcity = input1.split("-")
            print(origin)
            print(orgcity)
            input2 = form.cleaned_data['destinationplace']
            destination,destcity = input2.split("-")
            print(destination)
            print(destcity)
            url = 'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/USD/en-US/'+ origin + '/' + destination+ '/' + (form.cleaned_data['outboundpartialdate']).strftime("%Y-%m")+ '/' + (form.cleaned_data['inboundpartialdate']).strftime("%Y-%m")
            headers = {'X-RapidAPI-Key': settings.RAPIDAPI_API_KEY}
            api_response = requests.get(url, headers=headers)
            flights_json = api_response.json()
            main_api = 'http://api.openweathermap.org/data/2.5/weather?q='
            api_key = '&units=metric&appid=907d8c401b542c8e7ede79a3ddea8f1a'
            map  = 'https://maps.googleapis.com/maps/api/directions/json?origin="'+orgcity+'"&destination="'+destcity+'"&key=AIzaSyDohjPYxETfcjKzjHoiqYGenuirmd0jWg0'
            url1 = main_api + orgcity + api_key
            url2 = main_api + destcity + api_key
            org_data = requests.get(url1).json()
            dest_data = requests.get(url2).json()
            map_json = []
            map_data = requests.get(map).json()
            map_values = {
                "start": map_data['routes'][0]['legs'][0]['start_address'],
                "end": map_data['routes'][0]['legs'][0]['end_address'],
                "distance": map_data['routes'][0]['legs'][0]['distance']['text'],
                "duration": map_data['routes'][0]['legs'][0]['duration']['text'],
            }
            map_json.append(map_values)
            print(map_values)
            if (api_response.status_code == 200) & (org_data['cod']==200) & (dest_data['cod']== 200):
                form = FlightsForm()

                flights_data = []
                origin_weather = []
                destination_weather = []
                origin_city_weather = {
                    'city': orgcity,
                    'temperature': org_data['main']['temp'],
                    'description': org_data['weather'][0]['description'],
                    'icon': org_data['weather'][0]['icon'],

                }
                destination_city_weather = {
                    'city': destcity,
                    'temperature': dest_data['main']['temp'],
                    'description': dest_data['weather'][0]['description'],
                    'icon': dest_data['weather'][0]['icon'],
                }
                # Resturants Integration Starts
                zomato_api = 'https://developers.zomato.com/api/v2.1/search?&entity_id=' + destcity + "&entity_type=city&count=20&sort=rating&order=desc"
                zomato_header = {"User-agent": "curl/7.43.0", "Accept": "application/json","user_key": "50bf80e7cc40a8869d99583c024cb58a"}
                # Resturants Integration Ends
                # print(map_values)
                origin_weather.append(origin_city_weather)
                destination_weather.append(destination_city_weather)
                print(origin_weather)
                print(destination_weather)
                for quote in flights_json['Quotes']:
                    # if quote['InboundLeg']['CarrierIds']== or  quote['OutboundLeg']['CarrierIds'] ==
                    airline_data={
                        'id':quote['QuoteId'],
                            'origin': origin,
                                'airportorigin': flights_json['Places'][1]['Name'],
                                'destination': destination,
                                'airportdest': flights_json['Places'][0]['Name'],
                                'startdate': quote['OutboundLeg']['DepartureDate'],
                                'returndate': quote['InboundLeg']['DepartureDate'],
                                'price': quote['MinPrice'],
                                'incarrier': quote['InboundLeg']['CarrierIds'],
                                'outcarrier': quote['OutboundLeg']['CarrierIds'],
                                 'carrier':flights_json['Carriers'],
                                'symbol': flights_json['Currencies'][0]['Symbol'],
                            }
                    flights_data.append(airline_data)

                    # print(flights_data)

                header = "Below are the Details for you Trip"
                context = {
                    'flights_data': flights_data,
                    'origin_weather': origin_weather,
                    'destination_weather': destination_weather,
                    'map_json': map_json,
                    'form': form,
                    'header': header,
                    'orgin': orgcity,
                    'destination': destcity,
                    'zomato': requests.get(zomato_api, headers=zomato_header).json()
                    }
                # print(context)
                return render(request, self.template_name, context)
        else:
            error = 'Please Check the Details you entered'
            form = FlightsForm()
            context = {
                    'error' : error,
                    'form' : form,
            }
            return render(request, self.template_name,context)


def location(request):
   return render(request, 'mytrip/location.html',
                 {'mytrip': location})


class getzomato(TemplateView):
    template_name = 'mytrip/getzomato.html'

    def get(self,request):
        form = ZomatoForm()
        return render(request, self.template_name, {'form':form})

    def post(self,request):
        form=ZomatoForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                cuisines = form.cleaned_data['cuisines']
                main_api = 'https://developers.zomato.com/api/v2.1/search?q=' +form.cleaned_data['searchkeyword'] + '&cuisines=' + form.cleaned_data['cuisines'] + "&entity_id=" + form.cleaned_data['citiesList'] + "&entity_type=city&count=20&sort=rating&order=desc"
                header = {"User-agent": "curl/7.43.0", "Accept": "application/json",
                          "user_key": "50bf80e7cc40a8869d99583c024cb58a"}
                form = ZomatoForm
                try:
                    context = {
                        'cuisines':cuisines,
                        'data': requests.get(main_api, headers=header).json(),
                        'form': form,
                        }
                except:
                    pass
                return render(request, self.template_name, context)