from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
from .forms import LoginForm,UserRegistrationForm, CityForm, FlightsForm, ZomatoForm, Hotels, Location, SMS
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.views.generic import TemplateView
import requests
from django.conf import settings
from django.http import JsonResponse
from twilio.rest import Client
import twilio.rest

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


class flights(TemplateView):
    template_name = 'mytrip/flights.html'


    def get(self, request):
        # if request.method == 'POST':
        #     radio = form.cleaned_data['one/two']
        #     if radio=='one':
        #         form = FlightsFormOne()
        #         return render(request, self.template_name, {'form': form})
        #     else:
                smsform = SMS()
                form = FlightsForm()
                return render(request, self.template_name, {'form': form},{'smsform':smsform})

    def post(self, request):
        data = {}
        # if request.method == 'POST':
        form = FlightsForm(request.POST)
        smsform = SMS(request.POST)
        flights_data = []
        if form.is_valid():
            input1 = form.cleaned_data['originplace']
            origin, orgcity = input1.split("-")
            # print(origin)
            # print(orgcity)
            input2 = form.cleaned_data['destinationplace']
            destination, destcity = input2.split("-")

            url = 'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/USD/en-US/'+ origin + '/' + destination + '/' + (form.cleaned_data['outboundpartialdate']).strftime("%Y-%m-%d")+ '/' + (form.cleaned_data['inboundpartialdate']).strftime("%Y-%m-%d")
            headers = {'X-RapidAPI-Key': settings.RAPIDAPI_API_KEY}
            api_response = requests.get(url, headers=headers)
            flights_json = api_response.json()
            if api_response.status_code == 200:
                form = FlightsForm()
                header= "Below are the Details for you Trip"
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
                th= 'th'
                context = {
                    'origin': origin,
                    'destination': destination,
                    'flights_data': flights_data,
                    'form': form,
                    'smsform':smsform,
                    'header': header,
                    'th':th,
                }

                return render(request, self.template_name, context)
            else:
                error = 'Please Check the Dates you entered'
                form = FlightsForm()
                context = {
                    'error' : error,
                    'form' : form,
                   }
                return render(request, self.template_name,context,)
        if smsform.is_valid():

            print(smsform.cleaned_data['body'])
            print(smsform.cleaned_data['phone'])
            account_sid = 'AC5b8851457d8da824d607170b838d4f7b'
            auth_token = 'd7afab61073fd9dd8b9a9e37c83eb961'
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=smsform.cleaned_data['body'],
                from_='+15313018813',
                to=smsform.cleaned_data['phone'],
            )
            print(message)
            msg='msg'
            context = {
                'msg': msg,
                'message': 'SMS successful',
                'form': form,
                'smsform': smsform,
                'flights_data':flights_data,
            }
            return render(request, self.template_name, context, )

        else:
            msg = 'msg'
            error = 'Please Check the Details you entered'
            form = FlightsForm()
            context = {
                'msg': msg,
                'error' : error,
                'form' : form,
            }
            return render(request, self.template_name,context)



class starter(TemplateView):
    template_name = 'mytrip/starter.html'


    def get(self, request):
                form = FlightsForm()
                return render(request, self.template_name, {'form': form})



    def post(self, request):
        # if request.method == 'POST':
        form = FlightsForm(request.POST)
        if form.is_valid():
            input1 = form.cleaned_data['originplace']
            origin,orgcity = input1.split("-")
            # print(origin)
            # print(orgcity)
            input2 = form.cleaned_data['destinationplace']
            destination,destcity = input2.split("-")
            start = form.cleaned_data['outboundpartialdate'].strftime("%m/%d/%Y")
            end = form.cleaned_data['inboundpartialdate'].strftime("%m/%d/%Y")

            username = request.user.username
            if UserInterest.objects.filter(user=username).exists():
                if UserInterest.objects.filter(user=username).filter(origin=orgcity).filter(destination=destcity).exists():
                    object = UserInterest.objects.filter(user=username).get(origin=orgcity, destination=destcity)
                    object.searches = object.searches + 1
                    object.save()
                else:
                    entry = UserInterest(user=username, origin=orgcity, destination=destcity, searches=1)
                    entry.save()
            else:
                entry = UserInterest(user=username, origin=orgcity, destination=destcity, searches=1)
                entry.save()

            url = 'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/USD/en-US/'+ origin + '/' + destination+ '/' + (form.cleaned_data['outboundpartialdate']).strftime("%Y-%m-%d")+ '/' + (form.cleaned_data['inboundpartialdate']).strftime("%Y-%m-%d")
            headers = {'X-RapidAPI-Key': settings.RAPIDAPI_API_KEY}
            api_response = requests.get(url, headers=headers)
            flights_json = api_response.json()
            main_api = 'http://api.openweathermap.org/data/2.5/weather?q='
            api_key = '&units=metric&appid=907d8c401b542c8e7ede79a3ddea8f1a'
            map  = 'https://maps.googleapis.com/maps/api/directions/json?origin="'+orgcity+'"&destination="'+destcity+'"&key=AIzaSyDohjPYxETfcjKzjHoiqYGenuirmd0jWg0'
            url1 = main_api + orgcity + api_key
            url2 = main_api + destcity + api_key
            hotel = 'http://api.hotwire.com/v1/search/hotel?apiKey=eew8fwafckbky8563xfyw6te&format=json&startdate='+start+'&enddate='+end+'&dest='+destcity+'&children=1&adults=2&rooms=1&limit=5'
            org_data = requests.get(url1).json()
            dest_data = requests.get(url2).json()
            hotel_data = requests.get(hotel).json()
            # print(hotel_data)
            hotel_json=[]
            amn_json=[]
            place_json=[]

            map_json = []
            map_data = requests.get(map).json()
            map_values = {
                "start": map_data['routes'][0]['legs'][0]['start_address'],
                "end": map_data['routes'][0]['legs'][0]['end_address'],
                "distance": map_data['routes'][0]['legs'][0]['distance']['text'],
                "duration": map_data['routes'][0]['legs'][0]['duration']['text'],
            }
            map_json.append(map_values)
            if (api_response.status_code == 200) & (org_data['cod']==200) & (dest_data['cod']== 200) & (hotel_data['StatusCode'] == "0"):
                print("success")
                places= hotel_data["MetaData"]["HotelMetaData"]["Neighborhoods"]
                for place in hotel_data["MetaData"]["HotelMetaData"]["Neighborhoods"]:
                    hotel_area = {
                        "city": place['City'],
                        "state": place['State'],
                        "country": place['Country'],
                        "code": place['Id'],
                        "centroid": place['Centroid'],
                        "name": place['Name'],
                    }
                    place_json.append(hotel_area)
                    # print(hotel_area)
                for amn in hotel_data["MetaData"]["HotelMetaData"]["Amenities"]:
                    hotel_amn={
                        "code":amn['Code'],
                        "description":amn['Description'],
                    }
                    amn_json.append(hotel_amn)
                for results in hotel_data['Result'][:5]:
                    hotel_values = {
                        "sub_total": results['SubTotal'],
                        "fee": results['TaxesAndFees'],
                        "total": results['TotalPrice'],
                        "hotel_codes": results['AmenityCodes'],
                        "nights": results['Nights'],
                        "rating": results['StarRating'],
                        "id": results['NeighborhoodId'],
                        "link": results['DeepLink'],
                    }
                    hotel_json.append(hotel_values)



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

                header = "Below are the Details for you Trip"
                th="th"
                context = {
                    'flights_data': flights_data,
                    'origin_weather': origin_weather,
                    'destination_weather': destination_weather,
                    'map_json': map_json,
                    'form': form,
                    'header': header,
                    'orgin': orgcity,
                    'destination': destcity,
                    "amenities": amn_json,
                    "places": places,
                    "hotel_json":hotel_json,
                    "start":start,
                    "end":end,
                    "place_json": place_json,
                    'zomato': requests.get(zomato_api, headers=zomato_header).json(),
                    'th': th,
                    }

                return render(request, self.template_name, context,)
            else:
                error = 'Make sure the difference between dates is less than 30Days'

                err= 'err'
                form = FlightsForm()
                context = {
                        'err': err,
                        'error' : error,
                        'form' : form,
                }
                print(context)
                return render(request, self.template_name,context)
        else:
            error = 'Make sure the difference between dates is less than 30Days'
            err = 'err',
            form = FlightsForm()
            context = {
                'err': err,
                'error': error,
                'form': form,
            }
            return render(request, self.template_name, context)



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
            weather_data = []
            forecast_data = []
            if (json_data['cod']==200) & (forecast['cod']== "200"):
                # print(forecast)
                # print(json_data)

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
                for ft in forecast['list']:
                    dates = ft['dt_txt']
                    forecast_date, forecast_time = dates.split(" ")
                    # print(forecast_date)
                    # print(forecast_time)
                    forecast_weather = {
                        'temp': ft['main']['temp'],
                        'description': ft['weather'][0]['description'],
                        'icon': ft['weather'][0]['icon'],
                        'date': forecast_date,
                        'time': forecast_time,
                        'dt': ft['dt_txt']
                        # 'temp': forecast['list'][0]['weather'][0]['description'],
                    }
                    # print(forecast_weather)
                    forecast_data.append(forecast_weather)
                # print(forecast_data)
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


class location(TemplateView):
    template_name = 'mytrip/location.html'

    def get(self, request):
        form = Location()
        return render(request, self.template_name, {'form': form})

    def post(self,request):
        form=Location(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                orgcity = form.cleaned_data['originplace']
                destcity = form.cleaned_data['destinationplace']
                map = 'https://maps.googleapis.com/maps/api/directions/json?origin="' + orgcity + '"&destination="' + destcity + '"&key=AIzaSyDohjPYxETfcjKzjHoiqYGenuirmd0jWg0'
                map_json = []
                map_data = requests.get(map).json()
                map_values = {
                    "start": map_data['routes'][0]['legs'][0]['start_address'],
                    "end": map_data['routes'][0]['legs'][0]['end_address'],
                    "distance": map_data['routes'][0]['legs'][0]['distance']['text'],
                    "duration": map_data['routes'][0]['legs'][0]['duration']['text'],
                }
                map_json.append(map_values)
                context = {
                    'map_json': map_json,
                    'form': form,
                 }
                return render(request, self.template_name, context)
            else:
                error = 'Please Check Details'
                form = CityForm()
                context = {
                    'error': error,
                    'form': form,
                }
                return render(request, self.template_name, context)

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
                th = "th"
                context = {
                    'cuisines':cuisines,
                    'data': requests.get(main_api, headers=header).json(),
                    'form': form,
                    'th': th,
                    }
                try:
                    context = {
                        'cuisines': cuisines,
                        'data': requests.get(main_api, headers=header).json(),
                        'form': form,
                        'th': th,
                    }
                except:
                    pass
                return render(request, self.template_name, context)


class hotels(TemplateView):
    template_name = 'mytrip/hotels.html'


    def get(self, request):
                form = Hotels()
                return render(request, self.template_name, {'form': form})



    def post(self, request):
        # if request.method == 'POST':
        form = Hotels(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            start = form.cleaned_data['indate'].strftime("%m/%d/%Y")
            end = form.cleaned_data['outdate'].strftime("%m/%d/%Y")
            # print(city, start, end)
            hotel = 'http://api.hotwire.com/v1/search/hotel?apiKey=eew8fwafckbky8563xfyw6te&format=json&startdate='+start+'&enddate='+end+'&dest='+city+'&children=1&adults=2&rooms=1&limit=5'
            hotel_data = requests.get(hotel).json()
            # print(hotel_data)
            hotel_json=[]
            amn_json=[]
            place_json=[]
            if hotel_data['StatusCode'] == "0":
                print("success")
                for place in hotel_data["MetaData"]["HotelMetaData"]["Neighborhoods"]:
                    hotel_area={
                        "city":place['City'],
                        "state": place['State'],
                        "country": place['Country'],
                        "code": place['Id'],
                        "centroid":place['Centroid'],
                        "name":place['Name'],
                    }
                    place_json.append(hotel_area)
                    # print(hotel_area)
                for amn in hotel_data["MetaData"]["HotelMetaData"]["Amenities"]:
                    hotel_amn={
                        "code":amn['Code'],
                        "description":amn['Description'],
                    }
                    amn_json.append(hotel_amn)
                for results in hotel_data['Result'][:5]:
                    hotel_values={
                        "sub_total": results['SubTotal'],
                        "fee": results['TaxesAndFees'],
                        "total":results['TotalPrice'],
                        "hotel_codes": results['AmenityCodes'],
                        "nights": results['Nights'],
                        "rating": results['StarRating'],
                        "id": results['NeighborhoodId'],
                        "link":results['DeepLink'],
                    }
                    hotel_json.append(hotel_values)
                th="th"
                context = {
                        "form": form,
                        "city": city,
                        "amenities": amn_json,
                        "hotel_json": hotel_json,
                        "start": start,
                        "end": end,
                        "place_json":place_json,
                        "th":th,

                    }

                return render(request, self.template_name, context, )
            else:
                msg="Make sure the difference between dates is less than 30Days"
                err = 'err'
                context={
                    "msg": msg,
                    "form":form,
                    'err': err,
                }
                return render(request, self.template_name, context, )
        else:
            error = 'Please Check the Details you entered'
            err='err'
            form = Hotels()
            context = {
                    'error' : error,
                    'form' : form,
                    'err':err,
            }
            return render(request, self.template_name,context)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserInterestSerializer

# List at the end of the views.py
# Lists all customers
class UserInterestList(APIView):

    def get(self,request):
        userinterest_json = UserInterest.objects.all()
        serializer = UserInterestSerializer(userinterest_json, many=True)
        return Response(serializer.data)
