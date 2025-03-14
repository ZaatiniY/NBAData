from plotly import graph_objects as go
import pandas as pd 
import numpy as np 
from os import listdir
from plotly.subplots import make_subplots

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

#insertORDeltaColumns gives new columns that reprsent the delta betweenregular season and playoff performance
def insertORDeltaColumns(df):
    df["ortgD_scaler"] = (df['ORtg_pla']-df['ORtg_reg'])
    df["ortgD_ratio"] = ((df['ORtg_pla']-df['ORtg_reg'])/df['ORtg_reg'])*100 #multiplied by 100 as a scaler for better visibility of the data
    return(df)

def ORCompPlots(dfs):
    ORData = getOffensiveRatingData(dfs)
    #input(insertORDeltaColumns(ORData))
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




def ORFactorsPlots(dfs):
    ORData = getOffensiveRatingData(dfs)
    ORData = insertORDeltaColumns(ORData)
    pointLabel = [ORData['Team'].tolist()[x] + ' '+ ORData['Season Year'].tolist()[x] for x in range(len(ORData['Team'].tolist()))]
    fig = make_subplots(
        rows = 2,cols = 2,
    )

    input(dfs['sho_r']['Season Year']) #testing that the year column is printing properly 
    relevantYears = uniqueYears(dfs['sho_r']['Season Year'].tolist())
    figButtons = assignYearButtons(relevantYears)
    input(f"this is your buttons options - {figButtons}")
    fig.update_layout(updatemenus = [dict(active = 0,buttons = figButtons)])
    for year in relevantYears:
        traceVisibility = False #EDIT - change so that in year 1 the visibility is TRUE;will avoid bug where the first year that shows up in button options has ALL the data shown 
        fig = addTwoPtAttemptTrace(fig,dfs['sho_r'],ORData,pointLabel,year,traceVisibility)
        #fig = addTwoPtAssistTrace(fig,dfs['sho_r'],ORData,pointLabel,year,traceVisibility)
        #fig = addThrPtAttemptTrace(fig,dfs['sho_r'],ORData,pointLabel,year,traceVisibility)
        #fig = addThrPtAssistTrace(fig,dfs['sho_r'],ORData,pointLabel,year,traceVisibility)
    fig.show()

def uniqueYears(seasonYearsColumns):
    found = set()
    keep = []
    for year in seasonYearsColumns:
        if year not in found:
            found.add(year)
            keep.append(year)
    return keep

#start of 2PA vs ORtg delta 
def addTwoPtAttemptTrace(fig,shootingDF,ORData,label, year, traceVis):
    filteredDFshooting = shootingDF.loc[shootingDF['Season Year'] == year]
    filteredDFortg = ORData.loc[shootingDF['Season Year'] == year]
    fig.add_trace(
        go.Scatter(
            x = filteredDFshooting['2P.2'].tolist(),
            y = filteredDFortg['ortgD_scaler'].tolist(),
            name = "2PT Attempt Frequency vs ORtg Delta",
            #text = label, EDIT - need to fix pointLable such that it works with looping through all the different years 
            mode = 'markers',
            visible = traceVis
        ), row = 1,col =1
    )
    return fig

def addTwoPtAssistTrace(fig,shootingDF,ORData,label,traceVis):
    fig.add_trace(
        go.Scatter(
            x = shootingDF['2P.2'].tolist(),
            y = ORData['ortgD_ratio'].tolist(),
            name = "2PTs Assisted Frequency vs ORtg Delta",
            text = label,
            mode = 'markers',
            visible = traceVis
        ), row = 1,col =2
    )
    return fig

def addThrPtAttemptTrace(fig,shootingDF,ORData,label,traceVis):
    fig.add_trace(
        go.Scatter(
            x = shootingDF['3P'].tolist(),
            y = ORData['ortgD_ratio'].tolist(),
            name = "3PT Attempt Frequency vs ORtg Delta",
            text = label,
            mode = 'markers',
            visible = traceVis
        ), row = 2,col =1
    )
    return fig

def addThrPtAssistTrace(fig,shootingDF,ORData,label,traceVis):
    fig.add_trace(
        go.Scatter(
            x = shootingDF['3P.2'].tolist(),
            y = ORData['ortgD_ratio'].tolist(),
            name = "3PT Assist Frequency vs ORtg Delta",
            text = label,
            mode = 'markers',
            visible = traceVis
        ), row = 2,col =2
    )
    return fig



def assignYearButtons(SeasonYears):
    buttonChoices = []
    for year in range(len(SeasonYears)):
        visibilitySet = [False for i in range(len(SeasonYears))]
        visibilitySet[year] = True
        buttonOption = dict(
            label = SeasonYears[year],
            method = 'update',
            args = [{'visibile':visibilitySet},
                    {"Title":SeasonYears}]
        )
        buttonChoices.append(buttonOption)
    return buttonChoices



folders = ['C:\\Users\\Yaser\\OneDrive\\Documents\\Projects\\NBAData\\NBADataSets\\2002+\\Playoff','C:\\Users\\Yaser\\OneDrive\\Documents\\Projects\\NBAData\\NBADataSets\\2002+\\Regular']
dfs = readAllCSVs(folders)
#ORCompPlots(dfs)
ORFactorsPlots(dfs)