#import scipy.misc.imshow as imshow
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread
import pandas as pd

#d = open('../bikes.csv','r').readlines()
#for line in d:
#    print line.split(',')

def get_station_df():
    df = pd.read_csv('lat_long_id_name.csv')
    df = df[df.columns[1:]]
    df[['lat']] = (df[['lat']]).astype(float) / 10**6
    df[['lng']] = (df[['lng']]).astype(float) / 10**6
    return df

station_df = get_station_df()
print station_df[['lat']]
img = imread("map.png")
#ar = (bb[1]-bb[0])/(bb[3]-bb[2])
ar = 1265.0/893.0   # run cmd: $file map.png
bb = [ -6.3504, -6.2189, 53.3206, 53.3761]
plt.imshow(img,zorder=0, extent=bb, aspect = ar)
plt.plot(station_df[['lng']], station_df[['lat']], 'ro')
plt.show()
