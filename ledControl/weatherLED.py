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
from LedMatrix import LedMatrix
import RPi.GPIO as GPIO

weatherData = ''
countryID = '6553047'
apiKey = '2a6b0bc577fb4cbfc7a48b69afcc3eec'

def changeIcon(matrix, oldIcon):
    weatherIcon = weatherData['weather'][0]['icon'].encode("utf-8")
    print(weatherIcon)
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
    for attempt in range(10):
        try:
            data = requests.get('http://api.openweathermap.org/data/2.5/weather?id={}&APPID={}'.format(countryID, apiKey))
        except requests.exceptions.RequestException as e:
            data = "error"
            print e
            print("retry in 10 seconds")
            time.sleep(10)
            continue
        break
    
    output = "error"
    if data != "error":
        binary = data.content
        output = json.loads(binary)
    return output

def button_showTemp(channel):
    temp = weatherData['main']['temp'] - 273.15
    temp = int(round(temp))
    print(temp)
    matrix.write(16711680, str(temp))
    changeIcon(matrix, 'unset')
    
def button_shutdown(channel):
    matrix.colorWipe()
    os.system('sudo shutdown -h now')
    
if __name__ == '__main__':
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    GPIO.add_event_detect(23,GPIO.FALLING,callback=button_showTemp, bouncetime = 300)  
    
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    GPIO.add_event_detect(24,GPIO.FALLING,callback=button_shutdown, bouncetime = 300)
    
    matrix = LedMatrix(1)
    currWeatherIcon = 'unset'
    try:
        while True:
            weatherData = getWeatherUpdate()
            if weatherData != "error":
                currWeatherIcon = changeIcon(matrix, currWeatherIcon)
            time.sleep(1800)
    except KeyboardInterrupt:
        matrix.colorWipe()
        GPIO.cleanup()
