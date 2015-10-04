#!/usr/bin/env python
# Dublin Bikes scraper 
# Based on code by Shane Lynn 24/03/2014 , @shane_a_lynn, http://www.shanelynn.ie
import pandas as pd
import requests
from time import sleep, strftime, gmtime
import json
 
dic_db = "lat_long_id_name.db"           
dic_csv = "lat_long_id_name.csv"        

def writeToCsv(data, filename):
    """
    Take the list of results and write as csv to filename.
    """
    data_frame = pd.DataFrame(data)
    trim_df = data_frame[['id','lat','lng','name']]
    trim_df.to_csv(filename, header=True, mode="w")
 
if __name__ == "__main__":
 
    decoder = json.JSONDecoder()
    station_json = requests.get("http://api.citybik.es/dublinbikes.json") #grabs the current info for all Dublin Bikes from citybikes API
    station_data = decoder.decode(station_json.content) 		      #decode the JSON data into a python readable form
    writeToCsv(station_data, dic_csv)	
