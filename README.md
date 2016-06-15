## Synopsis

This project aims to analyse trends in the usage of Dublin Bikes, a public bike rental scheme in Dublin, Ireland, using some Python scripts to scrape the API data, save to SQL format, and then later plot this data. 
Example output can be found in analysis/example.png


## Code Example



## Motivation

I'm a long-term subscriber of Dublin Bikes and wanted to find out when I can reasonably expect there to be bikes available at the station nearest my house.
Real-time data is available (see http://www.dublinbikes.ie/All-Stations/Station-map or the smartphone app) but this isn't useful for planning future journeys or finding how
the usage changes throughout the day or across many days.
By capturing and saving this information over a long period of time it's possible to build up a clearer picture of when the busy and quiet times for different stations are.
Fluctations are also likely dependent on how bad the weather is, which we know a lot about in Dublin, and this data is saved also.

## Installation

Simply fork/clone the repo, data scraping is in the /data/ folder and analysis programs are in /analysis/.
Requires the following python packages (most can be installed via 'pip'): pandas, json, pywapi (a weather API) and sqlite3.


## Usage

Data for the number of bikes at a station is scraped in real-time for each station in the city, along with current weather information for Dublin, using the short python program found at /data/my_bikes.py.
This data is saved to a sql database using a naming scheme of YYYY-MM-DD_bikes_and_weather.db which contains separate tables for the bikes and weather data.
Data is arranged in rows by timestamp of the scraping, and columns are either the station name in table 'bikes' or weather information in table 'weather' (more specifically, |weather text description| Temperature | Effective Temp. | Wind Speed |).

## Analysis

Some munging and preparation for plotting is done in analysis/analysis.py.
 When this script runs the data in the specified date ranges and stations is processed and output into a CSV file or a plot if required.
 The script make_nice_plots.py can then be run which generates a 'nicer' looking plot which can then be saved.
 An example of this output can be found at analysis/example.png which shows the average total usage over the weekdays in one week.
