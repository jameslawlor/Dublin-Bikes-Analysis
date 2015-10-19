import pandas as pd
import numpy as np
import scipy as sp
import sqlite3
import random
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

def get_dfs(station = None, path=os.getcwd()):
    """ Get all available databases of bikes and weather, return dict of { date : [bikes_dataframe, weather_dataframe] } 
    """
    df_dic = {}
    for db in os.listdir(path):
        if db.endswith(".db"):
            with sqlite3.connect(db) as con:
                if station: bikes = pd.read_sql_query("SELECT \"index\",\""+station+"\" FROM bikes", con)
                else:       bikes = pd.read_sql_query("SELECT * FROM bikes", con)
                weather = pd.read_sql_query("SELECT * FROM weather", con)
            # Only include full-day records, 2-minute intervals means 60*24/2 ~ 700 scrapes
            if len(bikes['index']) > 700:
                date = datetime.datetime.strptime( db.split("_")[0] , "%Y-%m-%d").date()
                # Fix wind speed values and cast temperatures to integers
                weather['Wind_Speed'] =  weather['Wind_Speed'].replace(to_replace = 'calm', value = 0)
                weather[['Temperature', 'Feels_Like','Wind_Speed']] = weather[['Temperature',  'Feels_Like' ,'Wind_Speed']].astype(int)
                #convert timestamp string to a datetime time object
                bikes = bikes.rename(columns = {'index' : 'Time'})
                for df in [bikes, weather]:
                    df['Time'] = pd.to_datetime(df['Time'].apply(lambda x : datetime.datetime.strptime(str(date) + ' ' + str(x),"%Y-%m-%d %H:%M:%S")))
                df_dic[str(date)] = [bikes,weather]

    return df_dic

def get_weather_types(dic):

    big_weather = pd.concat([dic[day][1] for day in dic])
    return np.unique(big_weather['Weather'])

def do_the_bins(big_df):
    """
    Calculates average weekday trends of general bikes usage. 
    Uses custom binning routine due to irregular timestamps in the scraped data
    """

    def t_since_midnight(t):
        # converts datetime object to integer seconds since midnight
        return t.hour*3600 + t.minute*60 + t.second

    # Create bins for the timestamps
    bins = pd.Series( [ x*120 for x in xrange(0,720)  ] )

    ts =  [datetime.datetime.utcfromtimestamp(x).time() for x in bins]

    for day in big_df:
        if datetime.datetime.strptime( day , "%Y-%m-%d").date().weekday()  <= 4:
            bikes = big_df[day][0]
            bikes['bins'] = np.digitize( bikes['Time'].apply(t_since_midnight) , bins)
            bikes['sum'] = bikes.drop(['Time','bins'], axis=1).sum(axis=1)
    
    all_bikes = pd.concat([dfs[day][0][['sum','bins']] for day in dfs if datetime.datetime.strptime( day , "%Y-%m-%d").date().weekday()  <= 4])
    grouped = all_bikes.groupby('bins')
    print grouped['sum'].describe()
    print grouped.mean()
    print grouped['sum'].agg([np.sum, np.mean, np.std, len])
    stats = grouped['sum'].agg([np.sum, np.mean, np.std, len])

    fig, ax = plt.subplots(1)
    ax.plot(ts, grouped['sum'].mean())
    ax.fill_between(ts, stats['mean'] - stats['std'], stats['mean'] + stats['std'], facecolor='blue', alpha=0.5)
    ax.grid()
    plt.show()
    stop

#    plt.plot( ts , grouped['sum'].mean())
#    plt.show()
    
    print all_bikes 

    return


if __name__ == "__main__":

    station = 'Pearse_Street'
    station = None

    # Get dataframes dictionary and remove API bug values        
    dfs = bug_remove(get_dfs(station))

    stats_df = do_the_bins(dfs)
    stop

    for str_date in dfs:
        [bikes, weather] = dfs[str_date]
        print bikes['Time'].head()

        if datetime.datetime.strptime( str_date , "%Y-%m-%d").date().weekday()  <= 4:
            print str_date
            plt.plot(bikes['Time'].apply(lambda x : x.time()), pd.rolling_mean(bikes.sum(axis=1) , 5) )
#            plt.plot(weather['Time'], weather['Weather'])
            plt.show()


