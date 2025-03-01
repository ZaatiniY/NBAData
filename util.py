from bs4 import BeautifulSoup
import time 
from urllib.request import urlopen
import numpy as np
import pandas as pd

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
# Return --->   tableDF - pandas DF with dimension that match those of "Per 100 Pos" for the analyzed season; removing unnecessary components  
def regTableSearch(soup,specifiedID):
    columnHeaders = getRegColumnHeaders(soup,specifiedID)  
    tableRows = getRegDataRows(soup,specifiedID)
    headerIndexExcess = len(columnHeaders) - len(tableRows[0]) #tableRows is a list of lists, therefore to get how many items are in an individual table row, you need to look at an individual index (in this case zero)
    input(f"This is the base results of the table headers - {columnHeaders}")
    columnHeadersCorrected = columnHeaders[headerIndexExcess:] #this should remove the nonrelavant column search results from basketball reference tables
    input(f"This is the corrected results of the table headers - {columnHeadersCorrected}")
    perPosDF = pd.DataFrame(tableRows,columns=columnHeadersCorrected)
    return perPosDF   

def getRegColumnHeaders(soup,specifiedID):
    tableColumnsTag = 'th'
    table = soup.find_all(id=specifiedID)
    rawTableColumns = table[0].thead.find_all(tableColumnsTag)
    columnHeaders = [columnName.string for columnName in rawTableColumns] 
    #columnHeaders = removeNoneValues(columnHeaders)
    return columnHeaders

def getRegDataRows(soup,specifiedID):
    tableRowTag = 'tr'
    table = soup.find_all(id=specifiedID)
    rawTableRows = table[0].tbody.find_all(tableRowTag)
    #input(f"This is the length of rawTableRows: {len(rawTableRows)} - hit enter to continue ")
    dataRows = buildDataRows(rawTableRows)
    return dataRows

def buildDataRows(soupResults):
    relevantDataTag = 'td'
    compiledData = []
    for index in range(len(soupResults)):
        #input(f"This is your soup results for your index item - {soupResults[index]}")
        newRow = [rowElement.string for rowElement in soupResults[index].find_all(relevantDataTag)]
        #newRow = removeNoneValues(newRow)
        #input(f"This is before a new row gets added to the compiled data list of list {newRow}")
        compiledData.append(newRow)
    return compiledData  

