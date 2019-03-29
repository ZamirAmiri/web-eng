from django.http import HttpResponse
from django.shortcuts import render
import pymysql
# Create your views here.

from airports.models import Airports
from carriers.models import Carriers
from airports.models import AirportCarriers
from airports.models import Flights
from airports.models import MinutesDelayed
from airports.models import Delays
from airports.models import UpdateForm


import datetime

def index(request):
    airports = Airports.objects.all()

    context = {
        'title': 'Latest Posts',
        'airports': airports
    }

    return render(request, 'airports/index.html', context)


def calcAvgMedStd(delays):
    avg_cd = 0
    avg_la = 0
    late_la = []
    carrier_d = []
    for item in delays:
        avg_cd += (item.carrier_delay / len(delays))
        avg_la += (item.late_aircraft / len(delays))
        carrier_d.append(item.carrier_delay)
        late_la.append(item.late_aircraft)

    import statistics
    if len(late_la) <= 1:
        std_la = "N/A"
    else:
        std_la = statistics.stdev(late_la)

    if len(carrier_d) <= 1:
        std_cd = "N/A"
    else:
        std_cd = statistics.stdev(carrier_d)

    avg_cd = round(avg_cd)
    avg_la = round(avg_la)
    i = round(len(delays) / 2)
    item = delays[i]
    median_cd = item.carrier_delay
    delays = delays.order_by('late_aircraft')
    item = delays[i]
    median_la = item.late_aircraft

    json = {
        "avg_la": avg_la,
        "avg_cd": avg_cd,
        "median_cd": median_cd,
        "median_la": median_la,
        "std_la": std_la,
        "std_cd": std_cd
    }
    return json

def carriers(request,code):
    airport = Airports.objects.get(code = code)
    airport_carriers = AirportCarriers.objects.filter(airport = code)
    carrier = []

    delays = Delays.objects.filter(airport = code).order_by('carrier_delay')
    mem = calcAvgMedStd(delays)

    for item in airport_carriers:
        delays = Delays.objects.filter(airport=code, carrier = item.carrier).order_by('carrier_delay')
        carrier_code = item.carrier
        temp = calcAvgMedStd(delays)
        std_la = temp['std_la']
        if std_la == 'N/A':
            std_la = std_la
        else:
            std_la = round(std_la * 10) / 10

        std_cd = temp['std_cd']
        if std_cd == 'N/A':
            std_cd = std_cd
        else:
            std_cd = round(std_cd * 10) / 10

        carr = {
            "carrier": Carriers.objects.get(code = carrier_code),
            "avg_la": temp['avg_la'],
            "avg_cd": temp['avg_cd'],
            "median_cd": temp['median_cd'],
            "median_la": temp['median_la'],
            "std_la": std_la,
            "std_cd": std_cd
        }
        carrier.append(carr)

    context = {
        'airport': airport,
        'carriers': carrier,
        "avg_la": mem['avg_la'],
        "avg_cd": mem['avg_cd'],
        "median_cd": mem['median_cd'],
        "median_la": mem['median_la'],

        "std_la": mem['std_la'],
        "std_cd": mem['std_cd']
    }
    return render(request, 'airports/carriers.html', context)


def details(request, a_code, c_code):
    airport = Airports.objects.get(code = a_code)
    carrier = Carriers.objects.get(code = c_code)
    temp = Flights.objects.filter(airport = a_code, carrier = c_code).order_by('date')
    min_year = temp[0].date.year
    min_month = temp[0].date.month
    if min_month < 10:
        min_date = str(min_year) + "-0" + str(min_month)
    else:
        min_date = str(min_year) + "-" + str(min_month)
    max_year = temp[len(temp)-1].date.year
    max_month = temp[len(temp) - 1].date.month
    if max_month < 10:
        max_date = str(max_year) + "-0" + str(max_month)
    else:
        max_date = str(max_year) + "-" + str(max_month)

    context = {
        'airport': airport,
        'carrier': carrier,
        "min_date": min_date,
        "max_date": max_date
    }
    return render(request, 'airports/details.html', context)


def monthly(request, a_code, c_code, month, year):
    date = datetime.datetime(int(year),int(month),1)
    flight = Flights.objects.get(airport=a_code,carrier=c_code,date=date)
    flights_total = Flights.objects.filter(airport=a_code, carrier=c_code)
    mdasm = MinutesDelayed.objects.get(airport=a_code, carrier=c_code, date=date)
    total_mdasm = MinutesDelayed.objects.filter(airport=a_code, carrier=c_code)
    total_cdasc = 0                 # total_carrierdelay_airport_specific_carrier
    total_cdasla = 0                # total_carrierdelay_airport_specific_late_aircraft
    total_cdas_weather = 0
    total_cdas_security = 0
    total_cdas_nas = 0
    total_cdas_total = 0

    md = MinutesDelayed.objects.filter(carrier = c_code, date = date)
    total_md = MinutesDelayed.objects.filter(carrier = c_code)

    total_md_carrier_delay = 0
    total_md_late_aircraft = 0
    total_md_weather = 0
    total_md_security = 0
    total_md_nas = 0
    total_md_total = 0

    md_la = 0
    md_cd = 0
    md_weather = 0
    md_security = 0
    md_nas = 0
    md_total = 0

    for item in md:
        md_la += item.late_aircraft
        md_cd += item.carrier_delay
        md_weather += item.weather
        md_security += item.security
        md_nas += item.nas
        md_total += item.total

    for item in total_md:
        total_md_carrier_delay += item.carrier_delay
        total_md_late_aircraft += item.late_aircraft
        total_md_weather += item.weather
        total_md_security += item.security
        total_md_nas += item.nas
        total_md_total += item.total

    for item in total_mdasm:
        total_cdasc += item.carrier_delay
        total_cdasla += item.late_aircraft
        total_cdas_weather +=item.weather
        total_cdas_security += item.security
        total_cdas_nas += item.nas
        total_cdas_total += item.total

    total_on_time = 0
    total_delayed = 0
    total_cancelled = 0
    for f in flights_total:
        total_cancelled += f.cancelled
        total_delayed   += f.delayed
        total_on_time   += f.on_time

    context = {
        'total_cancelled':  total_cancelled,
        'total_delayed':    total_delayed,
        'total_on_time':    total_on_time,
        'flight':           flight,
        "cdasm":            mdasm,
        "total_cdasc":      total_cdasc,
        "total_cdasla":     total_cdasla,
        "total_cdas_weather": total_cdas_weather,
        "total_cdas_security": total_cdas_security,
        "total_cdas_nas": total_cdas_nas,
        "total_cdas_total": total_cdas_total,
        "total_md_la": total_md_late_aircraft,
        "total_md_cd": total_md_carrier_delay,
        "total_md_weather": total_md_weather,
        "total_md_security": total_md_security,
        "total_md_nas": total_md_nas,
        "total_md_total": total_md_total,
        "md_cd": md_cd,
        "md_la": md_la,
        "md_weather": md_weather,
        "md_security": md_security,
        "md_nas": md_nas,
        "md_total": md_total
    }

    return render(request, 'airports/monthly.html', context)


def options(request, a_code, c_code, month, year):
    date = datetime.datetime(int(year), int(month), 1)
    flight = Flights.objects.get(airport=a_code, carrier=c_code, date=date)

    context = {
        "airport_code": a_code,
        "carrier_code": c_code,
        "month": month,
        "year": year,
        "flight": flight
    }

    return render(request, "airports/options.html", context)


def delete(request, a_code, c_code, id):
    # connect to MySQL
    con = pymysql.connect(host='localhost', user='root', passwd='', db='web_eng')
    cursor = con.cursor()

    if request.method == "POST":

        context = {
            "airport_code": a_code,
            "carrier_code": c_code
        }

        query = """DELETE FROM `airports_flights` WHERE `id`= %s"""
        cursor.execute(query, int(id))
        print("sono qui")

    con.commit()
    con.close()

    return render(request, "airports/finish.html", context)


def update(request, a_code, c_code, id):
    # connect to MySQL
    con = pymysql.connect(host='localhost', user='root', passwd='', db='web_eng')
    cursor = con.cursor()

    if request.method == "POST":
        arg_request = {

            'airport_code': a_code,
            'carrier_code': c_code,
            'id': int(id),
            'cancelled': int(request.POST.get('Cancelled')),
            'on_time': int(request.POST.get('On time')),
            'total': 0,
            'delayed': int(request.POST.get('Delayed')),
            'diverted': int(request.POST.get('Diverted'))

        }

        arg_request['total'] = arg_request['cancelled'] + arg_request['on_time'] + arg_request['delayed'] + arg_request['diverted']

        on_time = arg_request['on_time']
        total = arg_request['total']
        delayed = arg_request['delayed']
        diverted = arg_request['diverted']
        id = arg_request['id']
        cancelled = arg_request['cancelled']

        query = """UPDATE `airports_flights` SET `cancelled`= '%s',`on_time`= '%s',`total`= '%s',`delayed`= '%s',
                                `diverted`= '%s' WHERE `id` = '%s'"""

        cursor.execute(query, (cancelled, on_time, total, delayed, diverted, id))

        con.commit()
        con.close()

    return render(request,"airports/finish.html",arg_request)
