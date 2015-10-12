import pandas as pd
import numpy as np
import scipy as sp
import sqlite3
import os
import time
import datetime
import matplotlib.pylab as plt

def bug_remove(df):
    """ Removes erroneous values from bug in CityBikes API - Each station has a 'default' value of bikes that the API"""   
    """ frequently and incorrectly returns throughout the day, so we remove the mode from each data set              """
    
    # DublinBikes does not allow removal of bikes between 00:30 and 05:00 so exclude this data then work with the modal value
    time_cutoff = datetime.time(5,00)           
    trim_df = df[ df['Time'] > time_cutoff]

    # First we replace all instances of modal value with 'NaN' using pandas "replace" function and a dictionary.
    # dic of dics going as { col_name_a : { mode_of_col_a : 'NaN' } , col_name_b : { ... }} fed into replace
    dic = {}
    for val in df.drop(['Time'],axis=1).columns:
        dic[val] = { trim_df[val].mode().loc[0] : np.nan  }
    df = df.replace(dic)

    # Now fill in the NaN values by backfilling and frontfilling just to make sure
    return (df.fillna(method = 'ffill',axis = 0)).fillna(method='bfill',axis=0) 

if __name__ == "__main__":

    # Grab the daily data in this directory
    for db in os.listdir(os.getcwd()):
        if db.endswith(".db"):
            with sqlite3.connect(db) as con:
                df_bikes = pd.read_sql_query("SELECT * FROM bikes", con)
                df_weather = pd.read_sql_query("SELECT * FROM weather", con)
            date = datetime.datetime.strptime( db.split("_")[0] , "%Y-%m-%d").date()

            #convert timestamp string to a datetime time object
            df_bikes = df_bikes.rename(columns = {'index' : 'Time'})
            for df in [df_bikes, df_weather]:
                df['Time'] = df['Time'].apply(lambda x : datetime.datetime.strptime(str(x),"%H:%M:%S").time())
        
            df_bikes = bug_remove(df_bikes)
            #print df_bikes
            # If weekday
            if date.weekday() < 5:
#                print df_bikes
                station = 'Pearse_Street'
                pbh = df_bikes[['Time',station]]
                plt.plot(pbh['Time'],pbh[station],'rx')
    plt.show()
