#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json 
import requests
from pprint import pprint
import time
from datetime import datetime
from datetime import timedelta
import urllib
import sys, os
import LedMatrix

countryID = '6553047'
apiKey = '2a6b0bc577fb4cbfc7a48b69afcc3eec'

def changeIcon(matrix, weatherData, oldIcon):
    weatherIcon = weatherData['weather'][0]['icon'].encode("utf-8")
    print(weathericon)
    if weatherIcon != oldIcon:
        iconString = 'error'
        if weatherIcon == '01d' or weatherIcon == '01n':
            iconString = 'clear_sky'
        elif weatherIcon == '02d' or weatherIcon == '02n':
            iconString = 'few_clouds'
        elif weatherIcon == '03d' or weatherIcon == '03n':
            iconString = 'scattered_clouds'
        elif weatherIcon == '04d' or weatherIcon == '04n':
            iconString = 'broken_clouds'
        elif weatherIcon == '09d' or weatherIcon == '09n':
            iconString = 'shower_rain'
        elif weatherIcon == '10d' or weatherIcon == '10n':
            iconString = 'rain'
        elif weatherIcon == '11d' or weatherIcon == '11n':
            iconString = 'thunderstorm'
        elif weatherIcon == '13d' or weatherIcon == '13n':
            iconString = 'snow'
        elif weatherIcon == '50d' or weatherIcon == '50n':
            iconString = 'mist'
        matrix.showIcon(iconString)
        print(iconString)
    return weatherIcon

def getWeatherUpdate():
    data = requests.get('http://api.openweathermap.org/data/2.5/weather?id={}&APPID={}'.format(countryID, apiKey))
    binary = data.content
    output = json.loads(binary)
    '''
    output = {u'base': u'stations',
            u'clouds': {u'all': 90},
            u'cod': 200,
            u'coord': {u'lat': 50.75, u'lon': 6.24},
            u'dt': 1528023300,
            u'id': 3247448,
            u'main': {u'humidity': 64,
                    u'pressure': 1019,
                    u'temp': 294.64,
                    u'temp_max': 296.15,
                    u'temp_min': 293.15},
            u'name': u'St\xe4dteregion Aachen',
            u'sys': {u'country': u'DE',
                    u'id': 5205,
                    u'message': 0.0065,
                    u'sunrise': 1527996342,
                    u'sunset': 1528054883,
                    u'type': 1},
            u'visibility': 10000,
            u'weather': [{u'description': u'overcast clouds',
                        u'icon': u'04d',
                        u'id': 804,
                        u'main': u'Clouds'}],
            u'wind': {u'deg': 360, u'speed': 2.1}}
            '''
    return output

if __name__ == '__main__':
    matrix = LedMatrix(1)
    currWeatherIcon
    try:
        while True:
            weatherData = getWeatherUpdate()
            currWeatherIcon = changeIcon(matrix, weatherData, currWeatherIcon)
            time.sleep(1800)
    except KeyboardInterrupt:
        matrix.colorWipe(Color(0, 0, 0), 10)
