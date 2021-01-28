
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

%matplotlib notebook

# https://www.coolweather.net/cityclimate/Seattle_climate_records.htm

maxTemp =  [45.0, 49.0, 52.2, 57.4, 64.2, 69.4, 75.3, 74.8, 69.4, 59.3, 50.5, 45.4]
minTemp = [35.1, 36.7, 38.2, 41.3, 46.5, 51.4, 54.8, 55.0, 51.5, 45.4, 39.6, 35.9]
precipitation = [5.77, 3.92, 3.73, 2.54, 1.74, 1.45, 0.74, 1.10, 1.77, 3.48, 6.15, 5.81]
xvals = range(1, 13)

plt.figure()
ax = plt.gca()
ax.set_xlabel('Date')
ax.set_title('Seattle Weather during 1948 - 2010')
    
plt.bar(xvals, precipitation, width=0.6, color='#5DADE2', alpha=0.7, zorder=5);
plt.yticks(np.arange(8))
ax.set_ylabel('Precipitation (inch)')

ax2 = ax.twinx()
ax2.set_ylabel('Temperature (Fahrenheit)')
ax2.plot(xvals, maxTemp, '-o', label='maxTemp', color='#C0392B', zorder=1);
ax2.plot(xvals, minTemp, '-o', label='minTemp', color='#2471A3', zorder=2);
plt.legend(loc='upper left', prop={'size': 9})

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' ]
plt.xticks(xvals, months);