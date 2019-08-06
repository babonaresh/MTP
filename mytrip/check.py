from django.http import JsonResponse
import requests


def post(self, request):
    data = {}
    # if request.method == 'POST':
    # form = FlightsForm(request.POST)
    # if form.is_valid():
    origin = "ORD"
    destination = "SFO"
    out= "2019-08-02"
    inb = "2019-08-08"
    url = 'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/USD/en-US/' + origin + '/' + destination + '/' + out + '/' + inb
    headers = {'X-RapidAPI-Key': settings.RAPIDAPI_API_KEY}
    api_response = requests.get(url, headers=headers)
    flights_json = api_response.json()
    print(flight_json)
    if api_response.status_code == 200:
            # form = FlightsForm()
        header = "Below are the Details for you Trip"
        for quote in flights_json.Quotes:
            carrierid_out = quote.OutboundLeg.CarrierIDs
            carrierid_in = quote.InboundLeg.CarrierIDs
            print(carrierid_in)
            print(carrierid_out)
        context = {
                'origin': origin,
                'destination': destination,
                'data': api_response.json(),
                # 'form': form,
                'header': header,
            }
        print(context)
        # return render(request, self.template_name, context)
    else:
        error = 'Please Check the Details you entered'
            # form = FlightsForm()
            # context = {
            #     'error': error,
            #     'form': form,
            # }
            # return render(request, self.template_name, context)
        print(error)