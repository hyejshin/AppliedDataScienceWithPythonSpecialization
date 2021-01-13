"""
Assignment 4
Description
In this assignment you must read in a file of metropolitan regions and associated sports teams from assets/wikipedia_data.html and answer some questions about each metropolitan region. Each of these regions may have one or more teams from the "Big 4": NFL (football, in assets/nfl.csv), MLB (baseball, in assets/mlb.csv), NBA (basketball, in assets/nba.csv or NHL (hockey, in assets/nhl.csv). Please keep in mind that all questions are from the perspective of the metropolitan region, and that this file is the "source of authority" for the location of a given sports team. Thus teams which are commonly known by a different area (e.g. "Oakland Raiders") need to be mapped into the metropolitan region given (e.g. San Francisco Bay Area). This will require some human data understanding outside of the data you've been given (e.g. you will have to hand-code some names, and might need to google to find out where teams are)!

For each sport I would like you to answer the question: what is the win/loss ratio's correlation with the population of the city it is in? Win/Loss ratio refers to the number of wins over the number of wins plus the number of losses. Remember that to calculate the correlation with pearsonr, so you are going to send in two ordered lists of values, the populations from the wikipedia_data.html file and the win/loss ratio for a given sport in the same order. Average the win/loss ratios for those cities which have multiple teams of a single sport. Each sport is worth an equal amount in this assignment (20%*4=80%) of the grade for this assignment. You should only use data from year 2018 for your analysis -- this is important!

Notes
Do not include data about the MLS or CFL in any of the work you are doing, we're only interested in the Big 4 in this assignment.
I highly suggest that you first tackle the four correlation questions in order, as they are all similar and worth the majority of grades for this assignment. This is by design!
It's fair game to talk with peers about high level strategy as well as the relationship between metropolitan areas and sports teams. However, do not post code solving aspects of the assignment (including such as dictionaries mapping areas to teams, or regexes which will clean up names).
There may be more teams than the assert statements test, remember to collapse multiple teams in one city into a single value!
"""

# Question 1
"""
For this question, calculate the win/loss ratio's correlation with the population of the city
 it is in for the NHL using 2018 data.
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nhl_df=pd.read_csv("assets/nhl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

def refactorCityData():
    city = cities
    city.rename(columns={'Population (2016 est.)[8]':'Population'}, inplace=True)
    city['NHL']=cities['NHL'].apply(cleanUp)
    city = cities[(cities['NHL'] != '—') & (cities['NHL'] != '')]
    return city[['Metropolitan area', 'Population', 'NHL']]

def refactorNHLData():
    nhl = nhl_df
    nhl = nhl[~nhl.team.str.contains('Division')]
    nhl['team'] = nhl['team'].apply(lambda x: x.replace('*', ''))
    nhl = nhl[nhl['year'] == 2018]
    nhl.drop(['GP', 'OL', 'PTS', 'PTS%', 'GF', 'GA', 'SRS', 'SOS', 'RPt%', 'ROW', 'year', 'League'], axis=1, inplace=True)
    nhl['Metropolitan area']=nhl.team.str.replace(r'\s\b(\w+)$','')
    nhl['team'] = nhl['team'].apply(getTeamName)
    nhl.loc[nhl['team']=='Leafs', 'Metropolitan area'] = 'Toronto'
    nhl.loc[nhl['Metropolitan area']=='Toronto', 'team'] = 'Maple Leafs'
    nhl.loc[nhl['team']=='Wings', 'Metropolitan area'] = 'Detroit'
    nhl.loc[nhl['Metropolitan area']=='Detroit', 'team'] = 'Red Wings'
    nhl.loc[nhl['team']=='Jackets', 'Metropolitan area'] = 'Columbus'
    nhl.loc[nhl['Metropolitan area']=='Columbus', 'team'] = 'Blue Jackets'
    nhl.loc[nhl['team']=='Knights', 'Metropolitan area'] = 'Las Vegas'
    nhl.loc[nhl['Metropolitan area']=='Las Vegas', 'team'] = 'Golden Knights'
    nhl.loc[nhl['Metropolitan area']=='Tampa Bay', 'Metropolitan area'] = 'Tampa Bay Area'
    nhl.loc[nhl['Metropolitan area']=='New York', 'Metropolitan area'] = 'New York City'
    nhl.loc[nhl['Metropolitan area']=='New Jersey', 'Metropolitan area'] = 'New York City'
    nhl.loc[nhl['Metropolitan area']=='Dallas', 'Metropolitan area'] = 'Dallas–Fort Worth'
    nhl.loc[nhl['Metropolitan area']=='Washington', 'Metropolitan area'] = 'Washington, D.C.'
    nhl.loc[nhl['Metropolitan area']=='Minneapolis', 'Metropolitan area'] = 'Minneapolis–Saint Paul'
    nhl.loc[nhl['Metropolitan area']=='Colorado', 'Metropolitan area'] = 'Denver'
    nhl.loc[nhl['Metropolitan area']=='Florida', 'Metropolitan area'] = 'Miami–Fort Lauderdale'
    nhl.loc[nhl['Metropolitan area']=='Washington', 'Metropolitan area'] = 'Washington, D.C.'
    nhl.loc[nhl['Metropolitan area']=='Arizona', 'Metropolitan area'] = 'Phoenix'
    nhl.loc[nhl['Metropolitan area']=='Carolina', 'Metropolitan area'] = 'Raleigh'
    nhl.loc[nhl['Metropolitan area']=='San Jose', 'Metropolitan area'] = 'San Francisco Bay Area'
    nhl.loc[nhl['Metropolitan area']=='Minnesota', 'Metropolitan area'] = 'Minneapolis–Saint Paul'
    nhl.loc[nhl['Metropolitan area']=='Anaheim', 'Metropolitan area'] = 'Los Angeles'
    return nhl

def cleanUp(x):
    word = re.findall('\[note\s[\d]*\]', x)
    if len(word) > 0:
        x = x.replace(word[0], '')
    return x.strip()

def getTeamName(x):
    word = re.findall(r'\b(\w+)$', x)
    return word[0]

def nhl_correlation(): 
    city = refactorCityData()
    nhl = refactorNHLData()
    data = pd.merge(city, nhl[['W', 'L', 'Metropolitan area']], how='left', on='Metropolitan area')
    data = data.set_index(['Metropolitan area'])
    data.columns = ['Population', 'team', 'W', 'L']
    data['Population'] = pd.to_numeric(data['Population'])
    data['W'] = pd.to_numeric(data['W'])
    data['L'] = pd.to_numeric(data['L'])
    data['ratio'] = pd.to_numeric(data['W']/(data['W']+data['L']))

    data = data.groupby(['Metropolitan area', 'Population', 'team']).mean()
    data.reset_index(inplace=True)
    
    population_by_region = data['Population'] # pass in metropolitan area population from cities
    win_loss_by_region = data['ratio'] # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


nhl_correlation()



# Question 2
"""
For this question, calculate the win/loss ratio's correlation with the population of the city
 it is in for the NBA using 2018 data.
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nba_df=pd.read_csv("assets/nba.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

def refactorTeamNameNBA(x):
    x =  x.replace('*', '')
    word = re.findall('\([\d]+\)', x)
    if len(word) > 0:
        x = x.replace(word[0], '')
    return x.strip()

def getTeamName(x):
    word = re.findall(r'\b(\w+)$', x)
    return word[0]

def refactorCityDataNBA():
    city = cities
    city['NBA']=cities['NBA'].apply(cleanUp)
    city = cities[(cities['NBA'] != '—') & (cities['NBA'] != '')]
    city.rename(columns={'Population (2016 est.)[8]':'Population', 'NBA':'team'}, inplace=True)
    return city[['Metropolitan area', 'Population', 'team']]

def refactorNBAData():
    nba = nba_df
    nba = nba[~nba.team.str.contains('Division')]
    nba['team'] = nba['team'].apply(refactorTeamNameNBA)
    nba = nba[nba['year'] == 2018]
    nba = nba[['team', 'W', 'L']]
    nba['Metropolitan area']=nba.team.str.replace(r'\s\b(\w+)$','')
    nba['team'] = nba['team'].apply(getTeamName)
    nba.loc[nba['Metropolitan area']=='New York', 'Metropolitan area'] = 'New York City'
    nba.loc[nba['Metropolitan area']=='Brooklyn', 'Metropolitan area'] = 'New York City'
    nba.loc[nba['Metropolitan area']=='Golden State', 'Metropolitan area'] = 'San Francisco Bay Area'
    nba.loc[nba['Metropolitan area']=='Dallas', 'Metropolitan area'] = 'Dallas–Fort Worth'
    nba.loc[nba['Metropolitan area']=='Washington', 'Metropolitan area'] = 'Washington, D.C.'
    nba.loc[nba['Metropolitan area']=='Minnesota', 'Metropolitan area'] = 'Minneapolis–Saint Paul'
    nba.loc[nba['Metropolitan area']=='Miami', 'Metropolitan area'] = 'Miami–Fort Lauderdale'
    nba.loc[nba['Metropolitan area']=='Indiana', 'Metropolitan area'] = 'Indianapolis'
    nba.loc[nba['Metropolitan area']=='Utah', 'Metropolitan area'] = 'Salt Lake City'
    nba.loc[nba['Metropolitan area']=='Portland Trail', 'Metropolitan area'] = 'Portland'
    return nba

def nba_correlation():
    city = refactorCityDataNBA()
    nba = refactorNBAData()
    data = pd.merge(city, nba[['W', 'L', 'Metropolitan area']], how='left', on='Metropolitan area')
    data.columns = ['Metropolitan area', 'Population', 'team', 'W', 'L']
    data['Population'] = pd.to_numeric(data['Population'])
    data['W'] = pd.to_numeric(data['W'])
    data['L'] = pd.to_numeric(data['L'])
    data['ratio'] = pd.to_numeric(data['W']/(data['W']+data['L']))

    data = data.groupby(['Metropolitan area', 'Population', 'team']).mean()
    data.reset_index(inplace=True)
    
    population_by_region = data['Population'] # pass in metropolitan area population from cities
    win_loss_by_region = data['ratio'] # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]

nba_correlation()



# Question 3
"""
For this question, calculate the win/loss ratio's correlation with the population of the city 
it is in for the MLB using 2018 data.
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import re

mlb_df=pd.read_csv("assets/mlb.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

def refactorTeamNameMLB(x):
    x =  x.replace('*', '')
    word = re.findall('\([\d]+\)', x)
    if len(word) > 0:
        x = x.replace(word[0], '')
    return x.strip()

def getTeamName(x):
    word = re.findall(r'\b(\w+)$', x)
    return word[0]

def refactorCityDataMLB():
    city = cities
    city['MLB']=cities['MLB'].apply(cleanUp)
    city = cities[(cities['MLB'] != '—') & (cities['MLB'] != '')]
    city.rename(columns={'Population (2016 est.)[8]':'Population', 'MLB':'team'}, inplace=True)
    return city[['Metropolitan area', 'Population', 'team']]

def refactorMLBData():
    mlb = mlb_df
    mlb = mlb[~mlb.team.str.contains('Division')]
    mlb['team'] = mlb['team'].apply(refactorTeamNameMLB)
    mlb = mlb[mlb['year'] == 2018]
    mlb = mlb[['team', 'W', 'L']]
    mlb['Metropolitan area']=mlb.team.str.replace(r'\s\b(\w+)$','')
    mlb['team'] = mlb['team'].apply(getTeamName)
    mlb.loc[mlb['Metropolitan area']=='Boston Red', 'team'] = 'Red Sox'
    mlb.loc[mlb['team']=='Red Sox', 'Metropolitan area'] = 'Boston'
    mlb.loc[mlb['Metropolitan area']=='Chicago White', 'team'] = 'White Sox'
    mlb.loc[mlb['team']=='White Sox', 'Metropolitan area'] = 'Chicago'
    mlb.loc[mlb['team']=='Jays', 'Metropolitan area'] = 'Toronto'
    mlb.loc[mlb['Metropolitan area']=='Toronto', 'team'] = 'Blue Jays'
    mlb.loc[mlb['Metropolitan area']=='New York', 'Metropolitan area'] = 'New York City'
    mlb.loc[mlb['Metropolitan area']=='San Francisco', 'Metropolitan area'] = 'San Francisco Bay Area'
    mlb.loc[mlb['Metropolitan area']=='Oakland', 'Metropolitan area'] = 'San Francisco Bay Area'
    mlb.loc[mlb['Metropolitan area']=='Texas', 'Metropolitan area'] = 'Dallas–Fort Worth'
    mlb.loc[mlb['Metropolitan area']=='Washington', 'Metropolitan area'] = 'Washington, D.C.'
    mlb.loc[mlb['Metropolitan area']=='Minnesota', 'Metropolitan area'] = 'Minneapolis–Saint Paul'
    mlb.loc[mlb['Metropolitan area']=='Miami', 'Metropolitan area'] = 'Miami–Fort Lauderdale'
    mlb.loc[mlb['Metropolitan area']=='Colorado', 'Metropolitan area'] = 'Denver'
    mlb.loc[mlb['Metropolitan area']=='Arizona', 'Metropolitan area'] = 'Phoenix'
    mlb.loc[mlb['Metropolitan area']=='Tampa Bay', 'Metropolitan area'] = 'Tampa Bay Area'
    mlb.loc[mlb['Metropolitan area']=='Phillies', 'Metropolitan area'] = 'Philadelphia'
    mlb.loc[mlb['Metropolitan area']=='Tampa Bay', 'Metropolitan area'] = 'Tampa Bay Area'
    return mlb

def mlb_correlation(): 
    city = refactorCityDataMLB()
    mlb = refactorMLBData()
    data = pd.merge(city, mlb[['W', 'L', 'Metropolitan area']], how='left', on='Metropolitan area')
    data.columns = ['Metropolitan area', 'Population', 'team', 'W', 'L']
    data['Population'] = pd.to_numeric(data['Population'])
    data['W'] = pd.to_numeric(data['W'])
    data['L'] = pd.to_numeric(data['L'])
    data['ratio'] = pd.to_numeric(data['W']/(data['W']+data['L']))

    data = data.groupby(['Metropolitan area', 'Population', 'team']).mean()
    data.reset_index(inplace=True)
    
    population_by_region = data['Population'] # pass in metropolitan area population from cities
    win_loss_by_region = data['ratio'] # pass in win/loss ratio from mlb_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
    return data


mlb_correlation()



# Question 4
"""
For this question, calculate the win/loss ratio's correlation with the population of the city
 it is in for the NFL using 2018 data.
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nfl_df=pd.read_csv("assets/nfl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

def refactorTeamName(x):
    x =  x.replace('*', '')
    x =  x.replace('+', '')
#     word = re.findall('\([\d]+\)', x)
#     if len(word) > 0:
#         x = x.replace(word[0], '')
    return x.strip()

def getTeamName(x):
    word = re.findall(r'\b(\w+)$', x)
    return word[0]

def refactorCityDataNFL():
    city = cities
    city['NFL']=cities['NFL'].apply(cleanUp)
    city = cities[(cities['NFL'] != '—') & (cities['NFL'] != '')]
    city.rename(columns={'Population (2016 est.)[8]':'Population', 'NFL':'team'}, inplace=True)
    return city[['Metropolitan area', 'Population', 'team']]

def refactorNFLData():
    nfl = nfl_df
    nfl = nfl[~nfl.team.str.contains('FC')]
    nfl['team'] = nfl['team'].apply(refactorTeamName)
    nfl = nfl[nfl['year'] == 2018]
    nfl = nfl[['team', 'W', 'L']]
    nfl['Metropolitan area']=nfl.team.str.replace(r'\s\b(\w+)$','')
    nfl['team'] = nfl['team'].apply(getTeamName)
    nfl.loc[nfl['Metropolitan area']=='New York', 'Metropolitan area'] = 'New York City'
    nfl.loc[nfl['Metropolitan area']=='San Francisco', 'Metropolitan area'] = 'San Francisco Bay Area'
    nfl.loc[nfl['Metropolitan area']=='Dallas', 'Metropolitan area'] = 'Dallas–Fort Worth'
    nfl.loc[nfl['Metropolitan area']=='Washington', 'Metropolitan area'] = 'Washington, D.C.'
    nfl.loc[nfl['Metropolitan area']=='Minnesota', 'Metropolitan area'] = 'Minneapolis–Saint Paul'
    nfl.loc[nfl['Metropolitan area']=='Miami', 'Metropolitan area'] = 'Miami–Fort Lauderdale'
    nfl.loc[nfl['Metropolitan area']=='Tampa Bay', 'Metropolitan area'] = 'Tampa Bay Area'
    nfl.loc[nfl['Metropolitan area']=='New England', 'Metropolitan area'] = 'Boston'
    nfl.loc[nfl['Metropolitan area']=='Arizona', 'Metropolitan area'] = 'Phoenix'
    nfl.loc[nfl['Metropolitan area']=='Tennessee', 'Metropolitan area'] = 'Nashville'
    nfl.loc[nfl['Metropolitan area']=='Carolina', 'Metropolitan area'] = 'Charlotte'
    nfl.loc[nfl['Metropolitan area']=='Oakland', 'Metropolitan area'] = 'San Francisco Bay Area'
    return nfl

def nfl_correlation(): 
    city = refactorCityDataNFL()
    nfl = refactorNFLData()
    data = pd.merge(city, nfl[['W', 'L', 'Metropolitan area']], how='left', on='Metropolitan area')
    data.columns = ['Metropolitan area', 'Population', 'team', 'W', 'L']
    data['Population'] = pd.to_numeric(data['Population'])
    data['W'] = pd.to_numeric(data['W'])
    data['L'] = pd.to_numeric(data['L'])
    data['ratio'] = pd.to_numeric(data['W']/(data['W']+data['L']))

    data = data.groupby(['Metropolitan area', 'Population', 'team']).mean()
    data.reset_index(inplace=True)
    
    population_by_region = data['Population'] # pass in metropolitan area population from cities
    win_loss_by_region = data['ratio'] # pass in win/loss ratio from nfl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
    assert len(population_by_region) == 29, "Q4: There should be 29 teams being analysed for NFL"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]

nfl_correlation()



# Question 5
"""
In this question I would like you to explore the hypothesis that given that an area has two sports teams 
in different sports, those teams will perform the same within their respective sports. 
How I would like to see this explored is with a series of paired t-tests (so use ttest_rel) 
between all pairs of sports. Are there any sports where we can reject the null hypothesis? 
Again, average values where a sport has multiple teams in one region. 
Remember, you will only be including, for each sport, cities which have teams engaged in that sport, 
drop others as appropriate. This question is worth 20% of the grade for this assignment.
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import re

mlb_df=pd.read_csv("assets/mlb.csv")
nhl_df=pd.read_csv("assets/nhl.csv")
nba_df=pd.read_csv("assets/nba.csv")
nfl_df=pd.read_csv("assets/nfl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

def nhl_data(): 
    city = refactorCityData()
    nhl = refactorNHLData()
    data = pd.merge(city, nhl[['W', 'L', 'Metropolitan area']], how='left', on='Metropolitan area')
    data = data.set_index(['Metropolitan area'])
    data.columns = ['Population', 'team', 'W', 'L']
    data['Population'] = pd.to_numeric(data['Population'])
    data['W'] = pd.to_numeric(data['W'])
    data['L'] = pd.to_numeric(data['L'])
    data['NHL'] = pd.to_numeric(data['W']/(data['W']+data['L']))
    data = data.groupby(['Metropolitan area', 'Population', 'team']).mean()
    data.reset_index(inplace=True)
    return data[['Metropolitan area', 'NHL']]

def nba_data():
    city = refactorCityDataNBA()
    nba = refactorNBAData()
    data = pd.merge(city, nba[['W', 'L', 'Metropolitan area']], how='left', on='Metropolitan area')
    data.columns = ['Metropolitan area', 'Population', 'team', 'W', 'L']
    data['Population'] = pd.to_numeric(data['Population'])
    data['W'] = pd.to_numeric(data['W'])
    data['L'] = pd.to_numeric(data['L'])
    data['NBA'] = pd.to_numeric(data['W']/(data['W']+data['L']))
    data = data.groupby(['Metropolitan area', 'Population', 'team']).mean()
    data.reset_index(inplace=True)
    return data[['Metropolitan area', 'NBA']]

def mlb_data(): 
    city = refactorCityDataMLB()
    mlb = refactorMLBData()
    data = pd.merge(city, mlb[['W', 'L', 'Metropolitan area']], how='left', on='Metropolitan area')
    data.columns = ['Metropolitan area', 'Population', 'team', 'W', 'L']
    data['Population'] = pd.to_numeric(data['Population'])
    data['W'] = pd.to_numeric(data['W'])
    data['L'] = pd.to_numeric(data['L'])
    data['MLB'] = pd.to_numeric(data['W']/(data['W']+data['L']))
    data = data.groupby(['Metropolitan area', 'Population', 'team']).mean()
    data.reset_index(inplace=True)
    return data[['Metropolitan area', 'MLB']]
    
def nfl_data(): 
    city = refactorCityDataNFL()
    nfl = refactorNFLData()
    data = pd.merge(city, nfl[['W', 'L', 'Metropolitan area']], how='left', on='Metropolitan area')
    data.columns = ['Metropolitan area', 'Population', 'team', 'W', 'L']
    data['Population'] = pd.to_numeric(data['Population'])
    data['W'] = pd.to_numeric(data['W'])
    data['L'] = pd.to_numeric(data['L'])
    data['NFL'] = pd.to_numeric(data['W']/(data['W']+data['L']))
    data = data.groupby(['Metropolitan area', 'Population', 'team']).mean()
    data.reset_index(inplace=True)
    return data[['Metropolitan area', 'NFL']]
    
def sports_team_performance():
    nba = nba_data()
    nfl = nfl_data()
    df = pd.merge(nba, nfl, how='outer', on='Metropolitan area')
    mlb = mlb_data()
    df = pd.merge(df, mlb, how='outer', on='Metropolitan area')
    nhl = nhl_data()
    df = pd.merge(df, nhl, how='outer', on='Metropolitan area')

    # Note: p_values is a full dataframe, so df.loc["NFL","NBA"] should be the same as df.loc["NBA","NFL"] and
    # df.loc["NFL","NFL"] should return np.nan
    sports = ['NFL', 'NBA', 'NHL', 'MLB']
    p_values = pd.DataFrame({k:np.nan for k in sports}, index=sports)
    
    for a in sports:
        for b in sports:
            if(a != b):
                temp = df[[a, b]].dropna()
                p_values.loc[a, b] = stats.ttest_rel(temp[a], temp[b])[1]
    
    assert abs(p_values.loc["NBA", "NHL"] - 0.02) <= 1e-2, "The NBA-NHL p-value should be around 0.02"
    assert abs(p_values.loc["MLB", "NFL"] - 0.80) <= 1e-2, "The MLB-NFL p-value should be around 0.80"
    return p_values

sports_team_performance()

