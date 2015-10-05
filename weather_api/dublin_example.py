import pywapi

weather_result = pywapi.get_weather_from_yahoo("EIXX0014")
weather_result = pywapi.get_weather_from_weather_com("EIXX0014")
for line in weather_result['current_conditions']:
    print line
#print weather_result['condition']['text']
#print weather_result['condition']['temp']

