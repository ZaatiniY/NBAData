from plotly import graph_objects as go
import pandas as pd 
import numpy as np 
from os import listdir

#self.siteTableIDs = ["per_poss-team","advanced-team","shooting-team"]
#readAllCSVs takes a list of file paths, and returns all the information
#parameters:
#   folders (list) - contains the set of file paths that will be parsed through to grab the CSV sheets
#returns - DFs (dict) - containing all dfs for playoff/regular season information ddd
def readAllCSVs(folders):
    DFs = []
    csvNames = []
    for path in folders:
        for x in listdir(path):
            csvNames.append(x)
        print(f'this is number of csvs in folder- {len(csvNames)}')
        for csv in csvNames:
            fullFilePath = path + '\\' + csv
            DFs.append(pd.read_csv(fullFilePath, encoding = 'utf-8',index_col = 0))
            csvNames = []
    print(len(DFs))
    return turnDFListToDict(DFs)
#Very silly lol - taking list from readAllCSVs and making it a dictionary for readability
def turnDFListToDict(dfs):
    dfDict = {
        'adv_p' : dfs[0],
        'per_p' : dfs[1],
        'sho_p' : dfs[2],
        'adv_r' : dfs[3],
        'per_r' : dfs[4],
        'sho_r' : dfs[5],
    }
    return dfDict


#data to be grabbed in ORCompTrend()
#parameters:
#   dfs (dict) - Takes the dfs dict used for all data analysis 
#returns: ortgData (dataframe) - dataframe containing the playoff teams with their yearly playoff/reg season ORtgs
def getOffensiveRatingData(dfs):
    regadv = dfs['adv_r']
    playadv = dfs['adv_p']
    regAdvSubset = regadv[['Team','ORtg','Season Year']]
    playAdvSubset = playadv[['Tm','ORtg','Season Year']]
    regAdvSubset.rename(columns = {'ORtg':'ORtg_reg'},inplace = True)
    playAdvSubset.rename(columns = {'Tm':'Team','ORtg':'ORtg_pla'},inplace = True)
    ortgData = pd.merge(regAdvSubset,playAdvSubset, how= 'inner', on = ['Team','Season Year'])
    ortgData = ortgData.fillna(value=np.nan)
    ortgData = ortgData.dropna(axis = 0)
    ortgData['Season Year'] = ortgData['Season Year'].astype(str) 
    return ortgData

def insertORDeltaColumns(df):

    pAndrDelta = [df['ORtg_reg'][x] -df['ORtg_pla'][x] for x in range(len(df['ORtg_pla'].tolist()))]
    return(pAndrDelta)

def ORCompTrend(dfs):
    ORData = getOffensiveRatingData(dfs)
    input(insertORDeltaColumns(ORData))
    fig = go.Figure()
    pointLabel = [ORData['Team'].tolist()[x] + ' '+ ORData['Season Year'].tolist()[x] for x in range(len(ORData['Team'].tolist()))]
    fig.add_trace(
        go.Scatter(
            x = ORData['ORtg_reg'],
            y = ORData['ORtg_pla'],
            name = "Relative Playoff and Regular Season Shooting",
            text = pointLabel,
            mode = 'markers'
        )
    )
    fig.add_shape(
        type = "line",
        yref="y1",
        xref="x1",
        xsizemode="scaled",
        ysizemode="scaled",
        x0=0,
        y0=0,
        x1=200,
        y1=200,
        line_dash="dot"
    )
    fig.update_xaxes(title = {'text':'Regular Season ORtg'},range = [100,125], color = "black",showgrid = False,griddash = 'solid',gridcolor= 'black')
    fig.update_yaxes(title = {'text':'Playoff Season ORtg'},range = [100,125], color = "black",showgrid = False,griddash = 'solid',gridcolor= 'black')
    fig.update_layout(title = {'text':'Playoff Team Offensive Ratings By Season'}, plot_bgcolor = "white")
    fig.show()





folders = ['C:\\Users\\Yaser\\OneDrive\\Documents\\Projects\\NBAData\\NBADataSets\\2002+\\Playoff','C:\\Users\\Yaser\\OneDrive\\Documents\\Projects\\NBAData\\NBADataSets\\2002+\\Regular']
dfs = readAllCSVs(folders)
ORCompTrend(dfs)