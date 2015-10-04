import matplotlib.pylab as plt
from datetime import datetime
import pandas as pd
import numpy as np

fin = open('bikes.csv','r')

names = []
times = []

for line in fin.readlines():
	name = line.split(",")[5]
	time = datetime.strptime(line.split(",")[-1][:-1],"%Y%m%d%H%M%S")
	if name not in names: names += [name]
	if time not in times: times += [time]

df = pd.DataFrame(index = times, columns = names)

for line in open('bikes.csv','r').readlines():
	name = line.split(",")[5]
	time = datetime.strptime(line.split(",")[-1][:-1],"%Y%m%d%H%M%S")
	bikes = int(line.split(",")[1])	
	free = int(line.split(",")[2])	
	df[name][time] =  bikes 
df["sum"] = df.sum(axis = 1).astype(float)
max_bikes = df["sum"].max()
df["usage"] = 100.0*df["sum"]/max_bikes
#print df["Portobello Harbour"]['2015-07-30 09:53:47']

# DF of rolling average data
means = pd.rolling_mean(df, window=20).shift(-10)
print means
for name in names:
	means[name + " rate of change"] = means[name].diff()

plt.figure()
##df["Portobello Harbour"].plot()
#for name in names[:10]:
#	df[name].plot()
#means["Portobello Harbour"].plot() 
#means["Charlemont Place"].plot() 
#means["Pearse Street"].plot() 
means["St. James Hospital (Central)"].plot() 
means["South Dock Road"].plot() 


#means["Exchequer Street"].plot() 
#means["Molesworth Street"].plot() 

#means["Portobello Harbour rate of change"].plot() 
#means["Charlemont Place rate of change"].plot() 
#means["Pearse Street rate of change"].plot() 
#means["Molesworth Street rate of change"].plot() 
plt.show()
