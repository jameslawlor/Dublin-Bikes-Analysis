#!/usr/bin/env python
# Dublin Bikes scraper
import pandas as pd
import requests
import time 
import json
import pywapi
import sqlite3
import os

def getStationData(dt):
    """
    Scrapes Dublin Bikes JSON station data, returns number of bikes, free stations and current time as a pandas dataframe
    """
    #grabs the current info for all Dublin Bikes from citybikes API
    json_data = requests.get("http://api.citybik.es/dublinbikes.json") 
    decoder = json.JSONDecoder()
    #decode the JSON data into a pandas dataframe structure
    station_data = pd.DataFrame(decoder.decode(json_data.content))               
    station_data['time'] = dt
 
    return station_data[['bikes','free','time']]

def getWeatherData(dt):
    """
    Scrapes weather.com for "Dublin's current in pandas dataframe
    """
    weather_result = pywapi.get_weather_from_weather_com("EIXX0014") 
    return pd.DataFrame([dt, str(weather_result['current_conditions']['text']), \
                             str(weather_result['current_conditions']['temperature'])])

def fileWrite(date, bikes, weather, form='sqlite'):
    """
    Write weather and station data to a CSV or sql db file
    """
    if form == 'CSV':
        bikes.to_csv('bikes_' + date + '.csv', header=False, mode="a")
        weather.to_csv('weather_' + date + '.csv', header=False, mode="a", index = False)
    elif form == 'sqlite':
        con = sqlite3.connect(date+'_bikes_and_weather.db')
        bikes.to_sql('bikes', con, if_exists='append')
        weather.to_sql('weather', con, if_exists='append', index = False)
    else:
        print 'Incompatible file type' 

if __name__ == "__main__":
 
    while True:
        try:
            # Define global datetime of scraping 
            now = time.strftime("%Y-%m-%d %H:%M:%S") 
            # Date
            todays_date = now.split()[0]             
    
            df_bikes = getStationData(now)
            df_weather = getWeatherData(now)
        
            fileWrite(now,df_bikes,df_weather)

            print "Data scraped successfully at " + now

        except:
            print "Connection Error, retrying in 120s"
            pass

        time.sleep(120)
