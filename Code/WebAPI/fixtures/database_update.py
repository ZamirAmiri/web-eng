import json
import os
import pymysql


# read JSON file which is in the next parent folder

file = os.path.abspath('C:/Users/Zamir/Programming/WE/WebAPI/fixtures') + "/airlines.json"
json_data = open(file).read()
json_obj = json.loads(json_data)


# connect to MySQL
con = pymysql.connect(host='localhost', user='root', passwd='', db='web_eng')
cursor = con.cursor()

# parse json data to SQL insert
for item in enumerate(json_obj):

    airport = item[1]['airport']
    code = airport['code']
    name = airport['name']
    airport_query = """INSERT INTO airports_airports (`code`, `name`)
                 VALUES (%s, %s)  
                 ON DUPLICATE KEY UPDATE
                 `code` = VALUES(`code`)"""
    cursor.execute(airport_query, (code, name))

    carrier = item[1]['carrier']
    code = carrier['code']
    name = carrier['name']
    carrier_query = """INSERT INTO carriers_carriers (`code`, `name`)
                 VALUES (%s, %s)  
                 ON DUPLICATE KEY UPDATE
                 `code` = VALUES(`code`)"""
    cursor.execute(carrier_query, (code, name))

    airport = item[1]['airport']
    airportCode = airport['code']
    carrier = item[1]['carrier']
    carrierCode = carrier['code']
    airportCarrier_query = """INSERT INTO airports_airportcarriers (`airport`, `carrier`)
                                VALUES (%s, %s)
                                 ON DUPLICATE KEY UPDATE
                                  `airport` = VALUES(`airport`)"""
    cursor.execute(airportCarrier_query, (airportCode, carrierCode))

    time = item[1]['time']
    year = time['year']
    month = time['month']
    date = str(year) + '-' + str(month) + '-1'
    statistics = item[1]['statistics']
    flights = statistics['flights']
    delays = statistics['# of delays']
    minutes_delayed = statistics['minutes delayed']
    ##Flights
    cancelled = flights['cancelled']
    on_time = flights['on time']
    total = flights['total']
    delayed = flights["delayed"]
    diverted = flights["diverted"]

    airportCarrier_query = """INSERT INTO `airports_flights`
    (`airport`, `carrier`, `date`, `cancelled`, `on_time`, `total`, `delayed`, `diverted`)
     VALUES
      (%s,%s,%s,%s,%s,%s,%s,%s)
      ON DUPLICATE KEY UPDATE
          `airport` = VALUES(`airport`)"""
    cursor.execute(airportCarrier_query, (airportCode, carrierCode, date, cancelled, on_time, total, delayed, diverted))

    ##num of delays
    late_aircraft   = delays['late aircraft']
    weather         = delays['weather']
    security        = delays['security']
    nas             = delays["national aviation system"]
    carrier_delay   = delays["carrier"]

    airportCarrier_query = """INSERT INTO 
        `airports_delays`(`airport`, `carrier`, `date`, `late_aircraft`, `weather`, `security`, `nas`, `carrier_delay`) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE `airport` = VALUES(`airport`)"""
    cursor.execute(airportCarrier_query, (airportCode, carrierCode, date, late_aircraft, weather, security, nas, carrier_delay))

    #minutes delayed
    late_aircraft = minutes_delayed['late aircraft']
    weather = minutes_delayed['weather']
    carrier_delay = minutes_delayed["carrier"]
    security = minutes_delayed['security']
    total = minutes_delayed['total']
    nas = minutes_delayed["national aviation system"]

    airportCarrier_query = """INSERT INTO 
            `airports_minutesdelayed`(`airport`, `carrier`, `date`, `late_aircraft`, `weather`, `carrier_delay`, `security`, `total`, `nas`) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE `airport` = VALUES(`airport`)"""
    cursor.execute(airportCarrier_query, (airportCode, carrierCode, date, late_aircraft, weather, carrier_delay, security, total, nas))


con.commit()
con.close()
