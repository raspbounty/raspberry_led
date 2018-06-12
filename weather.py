# -*- coding: utf-8 -*-
import json 
import requests
from pprint import pprint
import time
from datetime import datetime
from datetime import timedelta
import urllib
import sys, os


enterCountryName = False
newCountryName = False
testForCountryChange = False
TOKEN = "278626847:AAEtEZYw0ka6x6FJEttLYRem5gSVfl5AxBg"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
aachenID = '6553047'
countryID = aachenID
apiKey = '2a6b0bc577fb4cbfc7a48b69afcc3eec'
windTransl = ["wind", "wind", "viento"]
tempTransl = ["temperature", "temperatur", "temperatura"]
sunTransl = ["sun", "sonne", "sol"]
countryTransl = ["country"]

tempSentenceTransl = ['Current Temperatur is {}°C. Todays minimum temperature is {}°C and maximum temperature is {}°C.',
                      'Die aktuelle temperatur ist{}°C. Das heutige minimum ist {}°C und das heutige maximum {}°C',
                      'La temperatura actual es {}°C. La temperatura mínima de hoy es {}°C y la temperatura máxima es {}°C.']
sunSentenceTransl = ['The sunrise is at {} and the sunset at {}',
                      'Der Sonnenaufgang ist um {} und der Sonnenuntergang um {}',
                      'El amanecer está en {} y el atardecer en {}']
windSentenceTransl = ['The wind comes from {} with {}m/s.',
                     'Der Wind kommt von {} mit einer Geschwindigkeit von {}m/s}',
                     'El viento viene de {} con {}m/s.']


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
   
def getWeatherUpdate():
    data = requests.get('http://api.openweathermap.org/data/2.5/weather?id={}&APPID={}'.format(aachenID, apiKey))
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

def getWindDirection(degrees):
    direction = "Error"
    if (degrees >= 348.75 and degrees < 360) and (degrees >= 0 and degrees < 11.25) :
        direction = "N"
    elif degrees >= 11.25 and degrees < 33.75:
        direction = "NNE"
    elif degrees >= 33.75 and degrees < 56.25:
        direction = "NE"
    elif degrees >= 56.25 and degrees < 78.75:
        direction = "ENE"
    elif degrees >= 78.75 and degrees < 101.25:
        direction = "E"
    elif degrees >= 101.25 and degrees < 123.75:
        direction = "ESE"
    elif degrees >= 123.75 and degrees < 146.25:
        direction = "SE"
    elif degrees >= 146.25 and degrees < 168.75:
        direction = "SSE"
    elif degrees >= 168.75 and degrees < 191.25:
        direction = "S"
    elif degrees >= 191.25 and degrees < 213.75:
        direction = "SSW"
    elif degrees >= 213.75 and degrees < 236.25:
        direction = "SW"
    elif degrees >= 236.25 and degrees < 258.75:
        direction = "WSW"
    elif degrees >= 258.75 and degrees < 281.25:
        direction = "W"
    elif degrees >= 281.25 and degrees < 303.75:
        direction = "WNW"
    elif degrees >= 303.75 and degrees < 326.25:
        direction = "NW"
    elif degrees >= 326.25 and degrees < 348.75:
        direction = "NNW"
    return direction
   
def reply(updates, weatherData):
    global testForCountryChange
    global newCountryName
    global enterCountryName
    for update in updates["result"]:
        try:
            chat = update["message"]["chat"]["id"]
            text = update["message"]["text"].lower()
            if testForCountryChange:
                testForCountryChange = False
                if text == "yes":
                    newCountryName = True
                    send_message('type the name of the country', chat)
                else:
                    send_message('current country will not be changed', chat)
            elif newCountryName:
                newCountryName = False
                
                with open('city.list.json') as f:
                    data = json.load(f)
                
                resultCountry = []
                resultIDs = []
                for country in data:
                    if text.lower() in country["name"].lower():
                        resultCountry.append(country["name"])
                        resultIDs.append(country["id"])
                if len(resultCountry) == 0:
                    send_message('Country not found. Current country will not be changed', chat)
                elif len(resultCountry) == 1:
                    send_message('Country changed to {}'.format(resultCountry[0]), chat)
                    countryID = resultIDs[0]
                else:
                    enterCountryName = True
                    send_message('More than one match found. Please enter one of the following countries to change. {}'.format(" ".join(str(x) for x in resultCountry)), chat)
            elif enterCountryName:
                with open('city.list.json') as f:
                    data = json.load(f)
                
                resultCountry = []
                resultIDs = []
                for country in data:
                    if text.lower() == country["name"].lower():
                        send_message('Country changed to {}'.format(country['name']), chat)
                        countryID = country['id']
                        enterCountryName = False
                
                if enterCountryName:
                    send_message('Country not found. Current country will not be changed', chat)
                    enterCountryName = False
                
            elif text in tempTransl:
                languageIndex = tempTransl.index(text)
                
                temp = round(weatherData['main']['temp'] - 273.15, 2)
                maxTemp = round(weatherData['main']['temp_max'] - 273.15, 2)
                minTemp = round(weatherData['main']['temp_min'] - 273.15, 2)
                
                send_message(tempSentenceTransl[languageIndex].format(temp, minTemp, maxTemp), chat)
            elif text in windTransl:
                languageIndex = windTransl.index(text)
                
                degrees = weatherData['wind']['deg']
                windDirection = getWindDirection(degrees)
                
                send_message(windSentenceTransl[languageIndex].format(windDirection, weatherData['wind']['speed']), chat)
            elif text in sunTransl:
                languageIndex = sunTransl.index(text)
                
                sunset = weatherData['sys']['sunset']
                sunsetDatetime = datetime.fromtimestamp(int(sunset))
                sunsetTimestring = '{:%H:%M}'.format(sunsetDatetime)
                
                sunrise = weatherData['sys']['sunrise']
                sunriseDatetime = datetime.fromtimestamp(int(sunrise))
                sunriseTimestring = '{:%H:%M}'.format(sunriseDatetime)
                
                send_message(sunSentenceTransl[languageIndex].format(sunriseTimestring, sunsetTimestring), chat)
            elif text in countryTransl:
                testForCountryChange = True
                send_message('current country is {} \n Would you like to change the country? yes-no'.format(weatherData['name']), chat)
            else:
                send_message('unknown command', chat)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
   
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)
   
def main():
    last_update_id = None
    weatherData = getWeatherUpdate()
    lastWeatherUpdate = datetime.now()
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            diff = lastWeatherUpdate - datetime.now()
            timediff = diff.total_seconds()
            if timediff > 3600:
                weatherData = getWeatherUpdate()
                lastWeatherUpdate = datetime.now()
            last_update_id = get_last_update_id(updates) + 1
            reply(updates, weatherData)
        time.sleep(0.5)

if __name__ == '__main__':
    main()
