import pandas as pd
import numpy as np
import scipy as sp
import os
import time
import datetime
import matplotlib.pylab as plt
from matplotlib import dates

#paths = ["mean_and_std_2015-09-25_to_2015-10-20_weekdays.dat","mean_and_std_2015-09-25_to_2015-10-20_weekends.dat"]

paths = ["mean_and_std_2015-09-25_to_2015-10-20_weekdays.dat"]

for i, path in enumerate(paths):

    df = pd.read_csv(path, index_col = 0)
    ts = list(df['time'].apply(lambda x : datetime.datetime.strptime(x, "%H:%M:%S")))
    # Make a plot
    df = pd.rolling_mean(df[['mean','std']], window=5, min_periods=1)
#    print pd.rolling_mean(df[['mean','std']].resample("1D", fill_method="ffill"), window=3, min_periods=1)

    df['mean'] = df['mean'].apply(lambda x: np.max(df['mean']) - x )


    plt.figure(figsize=(10, 7.5))    

    # Remove the plot frame lines.
    ax = plt.subplot(111)    
    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(False)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False)    
    ax.get_xaxis().tick_bottom()    
    ax.get_yaxis().tick_left()    

    plt.ylabel("Bikes in use", fontsize=15)  
    plt.title("DublinBikes average weekday usage", fontsize=22)  

    plt.xlabel("\nData source: CityBikes http://api.citybik.es/ | " 
           "Author: James Lawlor @lawlorino", fontsize=10)


    ax.plot(ts, df['mean'], color='black')
    ax.fill_between(ts, df['mean'] - df['std'], df['mean'] + df['std'], facecolor='blue', alpha=0.1)
#    ax.grid()
    plt.xlim(ts[0],ts[-1])
   # plt.ylim(0, np.max(df['mean'] + df['std']) + 100)
    ax.set_ylim(bottom = 0) 
    ax.xaxis.set_major_locator(dates.HourLocator(interval=2))
    hfmt = dates.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(hfmt)

plt.show()

