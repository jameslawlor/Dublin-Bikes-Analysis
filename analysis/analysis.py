import pandas as pd
import numpy as np
import scipy as sp
import sqlite3
import os
import time
import datetime
import matplotlib.pylab as plt

def bug_remove(dfs):
    """ Removes erroneous values from bug in CityBikes API - Each station has a 'default' value of bikes that the API"""   
    """ frequently and incorrectly returns throughout the day, so we remove the mode from each data set              """
    
    # Work with a df of all the bikes data to ensure we remove the errorneous value - doing it on a daily basis does not always work
    big_df = pd.concat([dfs[day][0] for day in dfs])

    # First we replace all instances of modal value with 'NaN' using pandas "replace" function and a dictionary.
    # dic of dics going as { col_name_a : { mode_of_col_a : 'NaN' } , col_name_b : { ... }} fed into replace
    dic = {}
    for val in big_df.drop(['Time'],axis=1).columns:
        dic[val] = { big_df[val].mode().loc[0] : np.nan  }

    # Apply changes to our dataframes, and fill NaNs with front and backfilling to cover all possible NaN positions 
    for key in dfs:
        dfs[key][0] = dfs[key][0].replace(dic)
        dfs[key][0] = (dfs[key][0].fillna(method = 'ffill',axis = 0)).fillna(method='bfill',axis=0)

    return dfs

def get_dfs(path=os.getcwd()):
    """ Get all available databases of bikes and weather, return dict of { date : [bikes_dataframe, weather_dataframe] } 
    """
    df_dic = {}
    for db in os.listdir(path):
        if db.endswith(".db"):
            with sqlite3.connect(db) as con:
                bikes = pd.read_sql_query("SELECT * FROM bikes", con)
                weather = pd.read_sql_query("SELECT * FROM weather", con)
            date = datetime.datetime.strptime( db.split("_")[0] , "%Y-%m-%d").date()

            #convert timestamp string to a datetime time object
            bikes = bikes.rename(columns = {'index' : 'Time'})
            for df in [bikes, weather]:
                df['Time'] = df['Time'].apply(lambda x : datetime.datetime.strptime(str(x),"%H:%M:%S").time())

            df_dic[str(date)] = [bikes,weather]

    return df_dic

if __name__ == "__main__":

    # Get dataframes dictionary and remove API bug values        
    dfs = bug_remove(get_dfs())

    for str_date in dfs:
        date = datetime.datetime.strptime( str_date , "%Y-%m-%d").date()
        bikes = dfs[str_date][0]
        weather = dfs[str_date][1]
        if date.weekday() >= 0:
            plt.plot(bikes['Time'], bikes.sum(axis=1))
    plt.show()
#
#            print df_bikes.sum(axis = 1)
##            stop
#
#            if date.weekday() == 0:
#                plt.plot(df_bikes['Time'], df_bikes.sum(axis = 1), 'b')                
#            if date.weekday() == 4:
#                plt.plot(df_bikes['Time'], df_bikes.sum(axis = 1), 'r')                

#            weather_types = np.unique(df_weather['Weather'])

            # If Mon-Fri 
#            if date.weekday() < 5:
#                station = 'Pearse_Street'
#                pbh = df_bikes[['Time',station]]
#                plt.plot(pbh['Time'],pbh[station],'rx')
#    plt.show()
