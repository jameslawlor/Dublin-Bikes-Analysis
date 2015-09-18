#!/usr/bin/env python
# Dublin Bikes scraper
import pandas as pd
import requests
from time import sleep, strftime
import json
import pywapi
import sqlite3
import os

t = 120                        # number of seconds between samples

def getData():

    decoder = json.JSONDecoder()
    json_data = requests.get("http://api.citybik.es/dublinbikes.json") #grabs the current info for all Dublin Bikes from citybikes API
    station_data = decoder.decode(json_data.content)               #decode the JSON data into a python readable form
        
    return station_data

if __name__ == "__main__":
 
    while True:

        weather_result = pywapi.get_weather_from_weather_com("EIXX0014") 
        weather_now = str(weather_result['current_conditions']['text']) 
        temp_now = str(weather_result['current_conditions']['temperature'])

        df = pd.DataFrame(getData())
        df['time'] = strftime("%Y-%m-%d %H:%M:%S") # Add timestamp of the sample
        df['weather'] = weather_now
        df['temperature'] = temp_now

        today = strftime("%Y-%m-%d") # We will store data daily
        df[['bikes','free','time','weather','temperature']].to_csv('bikes_'+today+'.csv', header=False, mode="a")     # Write to CSV

        con = sqlite3.connect('bikes_'+today+'.db')
        df[['bikes','free','time','weather','temperature']].to_sql('bikes', con, if_exists='append')
        print "Data scraped: " + strftime( "%H:%M:%S %d-%m-%Y ")
        sleep(t)

