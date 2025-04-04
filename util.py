from bs4 import BeautifulSoup
import time 
from urllib.request import urlopen
import numpy as np
import pandas as pd
import re 

#readWebPageHTML will give you the HTML version of a website
#   parameters:
#       - link - string; website link 
#   return->    htmlTree - interpretted website link as the proper html format

def readWebPageHTML(link):
    with urlopen(link) as response:
        htmlTree = response.read()
        #print(f"{htmlTree}")
    return htmlTree

def transformToSoupHP(html):
    soup = BeautifulSoup(html,"html.parser")
    return soup

def searchTreeTagAll(soup,tag):
    results = soup.find_all(tag)
    return results

def searchTreeClassAll(soup,c):
    results = soup.find_all(class_ = c)
    return results

#posRegTableSearch is taking the Soup Object for each individual season being looped through in test.py
# From there, we will search the soup for all the data rows and columns
# Return --->   tableDF - pandas DF with dimension that match those of the scraped website for the analyzed season
def regTableSearch(soup,specifiedID,seasonLink):
    columnHeaders = getRegColumnHeaders(soup,specifiedID)  
    tableRows = getRegDataRows(soup,specifiedID,seasonLink)
    headerIndexExcess = len(columnHeaders) - len(tableRows[0]) #tableRows is a list of lists, therefore to get how many items are in an individual table row, you need to look at an individual index (in this case zero)
    columnHeadersCorrected = columnHeaders[headerIndexExcess:] #this should remove the nonrelavant column search results from basketball reference tables
    columnHeadersCorrected = adjustColumnsForRepeats(soup,specifiedID,columnHeadersCorrected)
    #input(f"This is your overheader check; see the list of colspan returned - {columnHeadersCorrected}")
    perPosDF = pd.DataFrame(tableRows,columns=columnHeadersCorrected)
    return perPosDF   


def getRegColumnHeaders(soup,specifiedID):
    tableColumnsTag = 'th'
    #input(f"Current column header grab - {specifiedID}")#DELETE - Testing playoff link returns correct value
    table = soup.find_all(id=specifiedID)
    #input(f"This is the returned table from your find_all result - {table}")
    rawTableColumns = table[0].thead.find_all(tableColumnsTag)
    columnHeaders = [columnName.string for columnName in rawTableColumns] 
    columnHeaders.append("Season Year")
    #columnHeaders = removeNoneValues(columnHeaders)
    return columnHeaders

#grabs the data rows from the target table in the website from seasonLink
#   soup - BS subject for your current season website [BS Object]
#   specificID - what ID to search to target your specific table [string]
#   seasonLink - the URL for your current season website [string]
# return --> dataRows - rows from your current table being assessed per specifiedID [list of lists]
def getRegDataRows(soup,specifiedID,seasonLink):
    tableRowTag = 'tr'
    table = soup.find_all(id=specifiedID)
    if len(table)>0:
        rawTableRows = table[0].tbody.find_all(tableRowTag)
        #input(f"This is the length of rawTableRows: {len(rawTableRows)} - hit enter to continue ")
        dataRows = buildDataRows(rawTableRows,seasonLink)
    else:
        dataRows = []
    return dataRows

def buildDataRows(soupResults,seasonLink):
    relevantDataTag = 'td'
    compiledData = []
    for index in range(len(soupResults)):
        #input(f"This is your soup results for your index item - {soupResults[index]}")
        newRow = [rowElement.string for rowElement in soupResults[index].find_all(relevantDataTag)]
        if newRow[0] is None:
            newRow[0] = soupResults[index].td.a.string #this is to make sure that the asterisk for playoffs team isn't returning None for the team name
        #input(f"This is the link where we will pull the year for the DF - {seasonLink}")
        addYearToRow(newRow,seasonLink)
        #input(f"This is before a new row gets added to the compiled data list of list {newRow}")
        compiledData.append(newRow)
    return compiledData  

def addYearToRow(row,seasonLink):
    year = getYearFromURL(seasonLink) #regex returns the string subset in the from of a list, so selecting index 0
    row.append(year)

def getYearFromURL(seasonLink):
    year = re.findall(r'\d+',seasonLink)
    return year[0] #returning only index at 0 since regex returns string subset as a list

# def playoff_link(href,seasonLink):
#     year = re.findall(r'\d+',seasonLink)[0]
#     return href and re.compile("playoffs/NBA_"+year).search(href)

def findPlayoffURLLink(soup,year):
    playoffExtension = soup.find_all(href = re.compile("playoffs/NBA_"+year))
    return playoffExtension

def extractPlayoffURL(playoffSearch):
    return playoffSearch.get("href")


#adjustColumnsForRepeats is the process of making sure all your columns have unique names, as DF concat doesn't work unless this is held true. Necessary since earlier NBA season data tables are different than modern day nba data tables
def adjustColumnsForRepeats(soup,specifiedID,columnTitles):
    if checkColumnHeadersRepeat(columnTitles) is True:
        overheadSoupTree = findOverHeadSoupSegments(soup,specifiedID,columnTitles)
        overHeadSpan = grabOverHeadSpan(overheadSoupTree)
        overheadTitles = grabOverHeadTitles(overheadSoupTree)
        columnTitles = applyUniqueColumnNames(columnTitles, overheadTitles,overHeadSpan)
    return columnTitles 

def checkColumnHeadersRepeat(columnTitles):
    check  = False 
    indX = 0 
    while check is False and indX < len(columnTitles)-1:
        for indY in range(indX+1,len(columnTitles)):
            if columnTitles[indX] == columnTitles[indY]:
                check = True
        indX += 1    
    return check

def findOverHeadSoupSegments(soup,specifiedID, columnTitles):
    table = soup.find_all(id=specifiedID)
    rawTableColumns = table[0].thead.find_all(class_='over_header')
    searchResults = rawTableColumns[0].find_all('th')
    return searchResults

def grabOverHeadSpan(overheadSearchResults):
    colspanList = []
    for x in overheadSearchResults:
        colspanList.append(int(x.get('colspan',1)))
    return colspanList

def grabOverHeadTitles(overheadSearchResults):
    overheadTitles = []
    for x in overheadSearchResults:
        overheadTitles.append(x.text)
    return overheadTitles 

def applyUniqueColumnNames(columnTitles,OHtitles,OHspan):
    OHindex = 0
    OHcounter = 0
    newColumnHeaders = []
    for column in columnTitles:
        if OHcounter>=OHspan[OHindex]:
            OHindex += 1 
            OHcounter =0 
        OHExtension = OHtitles[OHindex]
        if OHExtension == '':
            newColumnHeaders.append(column)
        else:
            newColumnHeaders.append(OHExtension + ' ' + column)
        OHcounter += 1
    return newColumnHeaders



