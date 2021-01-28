%matplotlib notebook

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])
df

df['mean'] = df.mean(axis=1)
df['std'] = df.std(axis=1)

df['sem'] = df.sem(axis=1)
df['yerr'] = df['sem']*4 

df['i_min'] = df['mean'] - df['yerr']
df['i_max'] = df['mean'] + df['yerr']

df[['mean', 'std', 'sem', 'yerr', 'i_min', 'i_max']]


plt.figure()

# xvals = range(len(df['mean']))
# plt.xticks(xvals, df.index)
# plt.bar(xvals, df['mean'], width=0.6)

max_color='#C0392B'
min_color='#2471A3'
default_color='grey'

class Cursor(object):
    def __init__(self, ax, df, bars):
        self.ax = ax
        self.df=df
        self.bars=bars
        self.hl = ax.axhline(color='#F1948A')

    def mouse_move(self, event):
        if not event.inaxes:
            return
        x, y = event.xdata, event.ydata
        self.hl.set_ydata(y)
        for index, row in self.df.iterrows():
            if row['i_max']<y:
                self.bars[self.df.index.get_loc(index)].set_color(min_color)
            elif row['i_min']>y:
                self.bars[self.df.index.get_loc(index)].set_color(max_color)
            else:
                self.bars[self.df.index.get_loc(index)].set_color(default_color)
        plt.draw()
        
ax = df['mean'].plot.bar(yerr=df['yerr'])

x = plt.gca().xaxis
for item in x.get_ticklabels():
    item.set_rotation(0)
    
bars = ax.get_children()[1:5]

cursor = Cursor(ax, df, bars)
plt.connect('motion_notify_event', cursor.mouse_move)