#!/usr/bin/env python
# Dublin Bikes scraper 
# Based on code by Shane Lynn 24/03/2014 , @shane_a_lynn, http://www.shanelynn.ie
import pandas as pd
import requests
from time import sleep, strftime, gmtime
import json
 
#Settings:
SAMPLE_TIME = 120                   # number of seconds between samples
CSV_FILE = "temp.csv"             # CSV file to save data in
 
def getData():
	"""
	 Modified version of Shane Lynn's code at http://www.shanelynn.ie/scraping-dublin-city-bikes-data-using-python/
	"""

	print "Scraping at " + strftime( "%H:%M:%S %d-%m-%Y ", gmtime())

	try:
	        decoder = json.JSONDecoder()
	        station_json = requests.get("http://api.citybik.es/dublinbikes.json") #grabs the current info for all Dublin Bikes from citybikes API
	        station_data = decoder.decode(station_json.content) 		      #decode the JSON data into a python readable form
	except:
       		return None

    	#remove unnecessary data - space saving
    	# we dont need latitude and longitude
#1	for ii in range(0, len(station_data)):
#1		del station_data[ii]['lat']
#1		del station_data[ii]['lng']
 
	return station_data


def writeToCsv(data, filename="output.csv"):
    """
    Take the list of results and write as csv to filename.
    """
    data_frame = pd.DataFrame(data)
    data_frame['time'] = strftime("%Y%m%d%H%M%S", gmtime())
    data_frame.to_csv(filename, header=True, mode="a")
 
if __name__ == "__main__":
 
    while True:
        data = getData()
        if data:
		writeToCsv(data, CSV_FILE)	
        sleep(SAMPLE_TIME)
