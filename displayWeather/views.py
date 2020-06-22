from django.shortcuts import render

# Create your views here.
import json
import datetime
import math
# urllib.request to make a request to api
import urllib.request
import calendar
import pytz


def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)).strftime('%I:%M:%p')
    return converted_time


def function_project(long, lat):
    TILE_SIZE = 256
    zoom = 3
    siny = math.sin(lat * math.pi / 180)

    siny = min(max(siny, -0.9999), 0.9999)

    x = int(TILE_SIZE * (0.5 + long / 360))
    y = int(TILE_SIZE * (0.5-math.log((1+siny)/(1-siny))/(4+math.pi)))

    scale = 1 << zoom
    x = math.floor(x*scale/TILE_SIZE)
    y = math.floor(y*scale/TILE_SIZE)
    return x, y


def getIcon(code):
    switcher = {
        "01d": "https://i.imgur.com/aWdrKUF.png",
        "01n": "https://i.imgur.com/aWdrKUF.png",
        "02d": "https://i.imgur.com/W24MNvS.png",
        "02n": "https://i.imgur.com/W24MNvS.png",
        "03d": "https://i.imgur.com/5VbkcyI.png",
        "03n": "https://i.imgur.com/5VbkcyI.png",
        "09d": "https://i.imgur.com/BFoHZgG.png",
        "09n": "https://i.imgur.com/BFoHZgG.png",
        "11d": "https://i.imgur.com/V0ySMFY.png",
        "11n": "https://i.imgur.com/V0ySMFY.png",
        "04d": "https://i.imgur.com/5VbkcyI.png",
        "04n": "https://i.imgur.com/5VbkcyI.png",
        "10d": "https://i.imgur.com/3XXE4VT.png",
        "10n": "https://i.imgur.com/3XXE4VT.png",
        "13d": "https://i.imgur.com/2euGRVm.png",
        "13n": "https://i.imgur.com/2euGRVm.png",
        "50d": "https://i.imgur.com/gIRJeKw.png",
        "50n": "https://i.imgur.com/gIRJeKw.png",
    }
    return switcher.get(code, "nothing")


def time_converterutc(date):

    local = pytz.timezone("Asia/Kolkata")
    naive = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    print(utc_dt)
    return utc_dt


def history(request):
    if request.method == 'POST':
        fromDate = request.POST['from']
        toDate = request.POST['to']

        fromDate = time_converterutc(fromDate)
        toDate = time_converterutc(toDate)
        data = {}
        return render(request, "displayWeather/history.html", data)


def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        try:
            forcast = urllib.request.urlopen(
                'http://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=aff312926088b9f269d078d6f388d5d3').read()

            data = json.loads(forcast)

            fiveDays = []

            for day in range(0, len(data['list']), 8):
                fiveDays.append(data['list'][day])

            long = data['city']['coord']['lon']
            lat = data['city']['coord']['lat']

            x, y = function_project(long, lat)

            day1icon = getIcon(fiveDays[0]['weather'][0]['icon'])
            day2icon = getIcon(fiveDays[1]['weather'][0]['icon'])
            day3icon = getIcon(fiveDays[2]['weather'][0]['icon'])
            day4icon = getIcon(fiveDays[3]['weather'][0]['icon'])
            day5icon = getIcon(fiveDays[4]['weather'][0]['icon'])

            a = datetime.datetime.today()
            numdays = 5
            dateList = []
            # print(a)
            print(a.strftime('%A'))
            for x in range(0, numdays):
                dateList.append(
                    (a + datetime.timedelta(days=x)).strftime('%A'))

            data = {
                "day1": dateList[0],
                "day2": dateList[1],
                "day3": dateList[2],
                "day4": dateList[3],
                "day5": dateList[4],


                "day1temp": str(round((fiveDays[0]['main']['temp']-273.15), 1)),
                "day2temp": str(round((fiveDays[1]['main']['temp']-273.15), 2)),
                "day3temp": str(round((fiveDays[2]['main']['temp']-273.15), 2)),
                "day4temp": str(round((fiveDays[3]['main']['temp']-273.15), 2)),
                "day5temp": str(round((fiveDays[4]['main']['temp']-273.15), 2)),

                "day1hum": str(fiveDays[0]['main']['humidity']),
                "day2hum": str(fiveDays[1]['main']['humidity']),
                "day3hum": str(fiveDays[2]['main']['humidity']),
                "day4hum": str(fiveDays[3]['main']['humidity']),

                "day1sunrise": time_converter(str(data['city']['sunrise'])),
                "day2sunrise": time_converter(str(data['city']['sunrise'])),
                "day3sunrise": time_converter(str(data['city']['sunrise'])),
                "day4sunrise": time_converter(str(data['city']['sunrise'])),
                "day5sunrise": time_converter(str(data['city']['sunrise'])),

                "day1sunset": time_converter(str(data['city']['sunset'])),
                "day2sunset": time_converter(str(data['city']['sunset'])),
                "day3sunset": time_converter(str(data['city']['sunset'])),
                "day4sunset": time_converter(str(data['city']['sunset'])),
                "day5sunset": time_converter(str(data['city']['sunset'])),

                "day1weather": str(fiveDays[0]['weather'][0]['description']),
                "day2weather": str(fiveDays[1]['weather'][0]['description']),
                "day3weather": str(fiveDays[2]['weather'][0]['description']),
                "day4weather": str(fiveDays[3]['weather'][0]['description']),
                "day5weather": str(fiveDays[4]['weather'][0]['description']),

                "day1windspeed": str(fiveDays[0]['wind']['speed']),
                "x": x,
                "y": y,

                "day1icon": day1icon,
                "day2icon": day2icon,
                "day3icon": day3icon,
                "day4icon": day4icon,
                "day5icon": day5icon,
            }
        except:
            data = {"error": "not a valid city name", }

    else:
        data = {}
    return render(request, "displayWeather/index.html", data)
