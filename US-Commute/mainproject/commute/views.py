from django.http import HttpResponse
from django.shortcuts import render
from newsapi import NewsApiClient
from datetime import datetime, timedelta
import requests, json
import pytz
import csv
import linecache
import yfinance as yf

newsapi = NewsApiClient(api_key='e4ea66f304bf470b8dbde6c4dcf6f2cf')
stateList = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"];
capStates = ["ALABAMA","ALASKA","ARIZONA","ARKANSAS","CALIFORNIA","COLORADO","CONNECTICUT","DELAWARE","FLORIDA","GEORGIA","HAWAII","IDAHO","ILLINOIS","INDIANA","IOWA","KANSAS","KENTUCKY","LOUISIANA","MAINE","MARYLAND","MASSACHUSETTS","MICHIGAN","MINNESOTA","MISSISSIPPI","MISSOURI","MONTANA","NEBRASKA","NEVADA","NEW HAMPSHIRE","NEW JERSEY","NEW MEXICO","NEW YORK","NORTH CAROLINA","NORTH DAKOTA","OHIO","OKLAHOMA","OREGON","PENNSYLVANIA","RHODE ISLAND","SOUTH CAROLINA","SOUTH DAKOTA","TENNESSEE","TEXAS","UTAH","VERMONT","VIRGINIA","WASHINGTON","WEST VIRGINIA","WISCONSIN","WYOMING"];

timeZones = [0,4,2,1,3,2,0,0,0,0,6,2,1,0,1,1,0,1,0,0,0,0,1,1,1,2,1,3,0,0,2,0,0,1,0,1,3,0,0,0,1,1,1,2,0,0,3,0,1,2]

def findState(state):
    if(state.upper() in capStates):
        state = stateList[capStates.index(state.upper())]
    elif(state.upper() == "NEWHAMPSHIRE"):
        state = "New Hampshire"
    elif(state.upper() == "NEWJERSEY"):
        state = "New Jersey"
    elif(state.upper() == "NEWYORK"):
        state = "New York"
    elif(state.upper() == "NEWMEXICO"):
        state = "New Mexico"
    elif(state.upper() == "NORTHCAROLINA"):
        state = "North Carolina"
    elif(state.upper() == "NORTHDAKOTA"):
        state = "North Dakota"
    elif(state.upper() == "RHODEISLAND"):
        state = "Rhode Island"
    elif(state.upper() == "SOUTHCAROLINA"):
        state = "South Carolina"
    elif(state.upper() == "SOUTHDAKOTA"):
        state = "South Dakota"
    elif(state.upper() == "WESTVIRGINIA"):
        state = "West Virginia"
    else:
        state = "none"

    return state
        

def getStocks(symbol):
    try:
        ticker = yf.Ticker(symbol)
        todays_data = ticker.history(period='1d')
        return round(todays_data['Close'][0],2)
    except:
        return "placeholder"

def getDate(state):
    timeOffSet = timeZones[stateList.index(state)]
    currentDate = datetime.utcnow()
    currentDate = currentDate - timedelta(hours = 4 + timeOffSet, minutes=0)
    
    return currentDate

def getMap(state):
    stateNum = stateList.index(state)
    mapURL = linecache.getline('static\FlagLinks.txt',stateNum+1)
    
    return mapURL

def getInfo(state):
    fullText = []
    stateLoc = 0
    with open("static\StateFacts.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            fullText.append(row)

    for i in range(len(fullText)):
        if(fullText[i][0] == state):
            stateLoc = i
    return fullText[stateLoc]

def getNews(state):

    headlines = newsapi.get_everything(state + " News", sort_by="relevancy", language="en", page_size=3)

    allNews = [[headlines['articles'][0]['title'], headlines['articles'][0]['source']['name'] + " - ", headlines['articles'][0]['url']],
               [headlines['articles'][1]['title'], headlines['articles'][1]['source']['name'] + " - ", headlines['articles'][1]['url']],
               [headlines['articles'][2]['title'], headlines['articles'][2]['source']['name'] + " - ", headlines['articles'][2]['url']]]
    
    return allNews

def toFahrenheit(temp):
    return round(((temp - 273.15) * (9 / 5)) + 32, 2)

def getWeather(state):
    
    apikey = "1d0bf89b149aa3ee043cc8c8790c6387"
    baseurl = "http://api.openweathermap.org/data/2.5/weather?"
    indexUrl = baseurl + "appid=" + apikey + "&q=" + state
    response = requests.get(indexUrl)
    x = response.json()
 
    y = x["main"]
    current_temperature = int(y["temp"])
    current_temperature = toFahrenheit(current_temperature)
    feels_like = int(y["feels_like"])
    feels_like = toFahrenheit(feels_like)
    current_humidity = y["humidity"]

    y = x["weather"]
    weather_description = y[0]["description"]

    city_location = x["name"]

    totalWeather = [current_temperature, current_humidity, weather_description, city_location, feels_like]
    
    return totalWeather

def index(request, givenState):
    state = findState(givenState)
    
    if(state != "none"):
        totalNews = getNews(state)
        totalWeather = getWeather(state)
        stateInfo = getInfo(state)
        
        entries = {"state":state,
                   "date":getDate(state),
                   "mapLoc":getMap(state),
                   "stateLink": "Flags/" + state + ".png",
                   "population":stateInfo[1],"capital":stateInfo[3],
                   "TSLAstock":getStocks("TSLA"), "AAPLstock":getStocks("AAPL"), "AMZNstock":getStocks("AMZN"),
                   "WMTstock":getStocks("WMT"), "XOMstock":getStocks("XOM"),
                   "weatherTemp":totalWeather[0], "weatherHum":totalWeather[1], "weatherDesc":totalWeather[2],
                   "weatherLoc":totalWeather[3], "weatherFeel":totalWeather[4],
                   "news1Title":totalNews[0][0], "news1Src":totalNews[0][1], "news1Link":totalNews[0][2],
                   "news2Title":totalNews[1][0], "news2Src":totalNews[1][1], "news2Link":totalNews[1][2],
                   "news3Title":totalNews[2][0], "news3Src":totalNews[2][1], "news3Link":totalNews[2][2],
        }
        
        return render(request, 'index.html', entries)
    else:
        return render(request, 'error.html')

def home(request):
    return render(request, 'home.html')
    
