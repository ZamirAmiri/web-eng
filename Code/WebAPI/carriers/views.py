from django.shortcuts import render
from .models import Carriers
from airports.models import AirportCarriers, Airports
# Create your views here.

def index(request):
    carriers = Carriers.objects.all()

    context = {
        'title': 'Carriers',
        'carriers': carriers
    }

    return render(request, 'carriers/index.html', context)

def airports(request,code):
    carrier = Carriers.objects.get(code = code)
    airport_carriers = AirportCarriers.objects.filter(carrier = code)
    print("print: " , len(airport_carriers))
    airport = []

    for item in airport_carriers:
        airport.append(Airports.objects.get(code = item.airport))



    context = {
        'carrier': carrier,
        'airports': airport
    }
    return render(request, 'carriers/airports.html', context)