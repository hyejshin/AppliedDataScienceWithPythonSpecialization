%matplotlib notebook
import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np
import datetime

df2 = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
df2['Data_Value'] = df2['Data_Value'].apply(lambda x: x/10)

temp2015 = df2[(df2['Date'] >= '2015-01-01') & (df2['Date'] < '2016-01-01')]
temp2015H = temp2015[temp2015['Element']=='TMAX']
temp2015L = temp2015[temp2015['Element']=='TMIN']

df2 = df2[(df2['Date'] >= '2005-01-01') & (df2['Date'] < '2015-01-01') &
          (df2['Date'] != '2008-02-29') & (df2['Date'] != '2012-02-29')]

df2['Month'] = df2['Date'].apply(lambda x: pd.to_datetime(x).month)
df2['Day'] = df2['Date'].apply(lambda x: pd.to_datetime(x).day)

tempMax = df2[df2['Element']=='TMAX'].groupby(['Month', 'Day', 'Element']).agg({'Data_Value': ['max']})
tempMax.columns = ['temp']
tempMin = df2[df2['Element']=='TMIN'].groupby(['Month', 'Day', 'Element']).agg({'Data_Value': ['min']})
tempMin.columns = ['temp']

tempMaxData = tempMax['temp'].values.tolist()
tempMinData = tempMin['temp'].values.tolist()

plt.figure()
plt.plot(tempMaxData, '-', color='#EC7063', label='Maximum for the day between 2005-2014', alpha=0.8, zorder=0)
plt.plot(tempMinData, '-', color='#5499C7', label='Minimum for the day between 2005-2014', alpha=0.8, zorder=1)
plt.gca().fill_between(range(len(tempMaxData)), tempMinData, tempMaxData,
                  facecolor='lightgrey', alpha=0.5)

tempH2015X = []
tempH2015Y = []
date_format="%Y-%m-%d"
base = datetime.datetime.strptime('2015-01-01', date_format)
for date, temp in zip(temp2015H['Date'], temp2015H['Data_Value']):
    d = datetime.datetime.strptime(date, date_format)
    delta = d - base
    index = delta.days
    if temp > tempMaxData[index]:
        tempH2015Y += [temp]
        tempH2015X += [index+1]
plt.scatter(tempH2015X, tempH2015Y, s=3, c='#E74C3C', zorder=5, label='2015 temperature greater than 2005-2014 maximum')

tempL2015X = []
tempL2015Y = []
date_format="%Y-%m-%d"
base = datetime.datetime.strptime('2015-01-01', date_format)
for date, temp in zip(temp2015L['Date'], temp2015L['Data_Value']):
    d = datetime.datetime.strptime(date, date_format)
    delta = d - base
    index = delta.days
    if temp < tempMinData[index]:
        tempL2015Y += [temp]
        tempL2015X += [index+1]
plt.scatter(tempL2015X, tempL2015Y, s=3, c='#2471A3', zorder=5, label='2015 temperature less than 2005-2014 mininum')

    
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' ]
monthDay = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
monthDayMiddle = [x + 14 for x in monthDay]
plt.xticks(monthDayMiddle, months)
plt.yticks(np.arange(-40, 50, 10))

ax = plt.gca()
ax.set_ylabel('Temperature (Celsius)')
ax.set_title('Daily High and Low Temperature in Ohio Area')
plt.legend(loc='lower right', prop={'size': 7})