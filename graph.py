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
    
    return turnDFListToDict(DFs)
#Very silly lol - taking list from readAllCSVs and making it a dictionary for readability
#EDIT - need to make it so that the dictionaries get added based on just name of the file, not order in which the function reads them from the directory
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
    relevantYears = uniqueYears(dfs['sho_r']['Season Year'].tolist())
    relevantYears.pop(0) #taking out 2025 from the years options since it's not 2025 playoffs yet 
    
    # for year in relevantYears: #back when we used a loop in the ORFactorsPlots 
         
    addTraceStyle(fig,dfs['sho_r'],ORData,pointLabel,relevantYears,columnOption = '2P',r = 1,c = 1)
    addTraceStyle(fig,dfs['sho_r'],ORData,pointLabel,relevantYears,columnOption = '2P.2',r = 2,c = 1)
    addTraceStyle(fig,dfs['sho_r'],ORData,pointLabel,relevantYears,columnOption = '3P',r = 1,c = 2)
    addTraceStyle(fig,dfs['sho_r'],ORData,pointLabel,relevantYears,columnOption = '3P.2',r = 2,c = 2)
    fig.update_xaxes(title_text="2Pt Attempt Fraction", row=1, col=1)
    fig.update_xaxes(title_text="3Pt Attempt Fraction", row=1, col=2)
    fig.update_xaxes(title_text="2Pt Assisted Fraction", row=2, col=1)
    fig.update_xaxes(title_text="3Pt Assisted Fraction", row=2, col=2)
    fig.update_yaxes(title_text = "% change in Offensive Rating")
    figButtons = assignYearButtons(relevantYears,fig)
    fig.update_layout(updatemenus = [dict(active = 0,buttons = figButtons)])
    fig.show()

def uniqueYears(seasonYearsColumns):
    found = set()
    keep = []
    for year in seasonYearsColumns:
        if year not in found:
            found.add(year)
            keep.append(year)
    return keep


#addTraceStyle will add traces to the figure based on the option selected for the column
def addTraceStyle(fig,shootingDF,ORData,label,relevantYears,columnOption,r,c):
    for year in relevantYears:
        filteredDFshooting = shootingDF.loc[shootingDF['Season Year'] == year]
        ORData['Season Year'] = ORData['Season Year'].astype(str) #changing dataframe to a string type
        filteredDFortg = ORData.loc[ORData['Season Year'] == str(year)]
        if year == relevantYears[0]:
            traceVis = True
        else:
            traceVis = False
        #input(filteredDFshooting['2P.2'])
        fig.add_trace(
            go.Scatter(
                x = filteredDFshooting[columnOption],
                y = filteredDFortg['ortgD_ratio'],
                name = year,
                text = filteredDFortg['Team'].tolist(),
                #text = relevantYears, #EDIT - need to fix pointLable such that it works with looping through all the different years 
                mode = 'markers',
                visible = traceVis,
                line = {'color':'cadetblue'}
            ), row = r,col =c
        )

def assignYearButtons(SeasonYears,fig):
    buttonChoices = list()
    for year in range(len(SeasonYears)):
        visibilitySet = [False for i in range(len(SeasonYears))]
        visibilitySet[year] = True
        buttonOption = dict(
            label = SeasonYears[year],
            method = 'update',
            args = [{'visible':visibilitySet},
                    {"Title":SeasonYears}]
        )
        buttonChoices.append(buttonOption)
    return buttonChoices


def orbTrends(dfs):
    fig = make_subplots(
        rows = 1, cols= 1
    )
    advancedStats = dfs['adv_r']
    relevantYears = uniqueYears(advancedStats['Season Year'])
    relevantYears.pop(0)
    averageYearlyORBP = calcAvgYearlyStat(advancedStats,relevantYears,columnName = 'ORB%')
    fig.add_trace(
        go.Scatter(
            y = averageYearlyORBP,
            x = relevantYears,
            mode = 'lines',
            line = {'color':'cadetblue'}
        ), row  = 1, col = 1
    )
    fig.update_xaxes(title_text = 'Regular Season Year')
    fig.update_yaxes(title_text = 'Average ORB %', showgrid = True, griddash = 'solid',gridcolor = 'black')
    fig.update_layout(title = {'text':'Regular Season ORB% Over the Years'}, plot_bgcolor = "white")
    fig.show()

    return averageYearlyORBP

    

def calcAvgYearlyStat(targetDF, years, columnName):
    averagedData = list()
    for year in years:
        currYearFiltered = targetDF.loc[targetDF['Season Year']==year]
        sumOfStat = currYearFiltered[columnName].sum()
        numberOfDataPoints = len(currYearFiltered[columnName]) 
        averageValue = round(sumOfStat/numberOfDataPoints,1)
        averagedData.append(averageValue)
    return averagedData



folders = ['C:\\Users\\Yaser\\OneDrive\\Documents\\Projects\\NBAData\\NBADataSets\\2002+\\Playoff','C:\\Users\\Yaser\\OneDrive\\Documents\\Projects\\NBAData\\NBADataSets\\2002+\\Regular']
dfs = readAllCSVs(folders)
# ORCompPlots(dfs)
# ORFactorsPlots(dfs)
orbTrends(dfs)