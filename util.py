from bs4 import BeautifulSoup
import time 
from urllib.request import urlopen
import numpy as np

#readWebPageHTML will give you the HTML version of a website
#   parameters:
#       - link - string; website link 
#   return->    htmlTree - interpretted website link as the proper html format
def printState(state):
    print("WHY ARENOT YOU PRINTING")
    input(f"You are currently in {state} state; hit enter to continue")

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
def posRegTableSearch(soup):
    tableRows = getPosDataRows(soup)
    #columnHeaders = getPosColumnHeaders(soup)
    return tableRows   

def getPosColumnHeaders():
    pass

def getPosDataRows(soup):
    tableRowTag = 'tr'
    table = soup.find_all(id="per_poss-team")
    rawTableRows = table[0].tbody.find_all(tableRowTag)
    input(f"This is the length of rawTableRows: {len(rawTableRows)} - hit enter to continue ")
    dataRows = makeSoupSearchNP(rawTableRows)
    return dataRows

def makeSoupSearchNP(soupResults):
    relevantDataTag = 'td'
    compiledData = np.zeros(createZerosNPArray(soupResults))
    for index in range(len(soupResults)):
        newRow = [rowElement.string for rowElement in soupResults[index].find_all(relevantDataTag)]
        compiledData[index] = newRow
    return compiledData  

def createZerosNPArray(soupResults):
    relevantDataTag = 'td'
    rowNumber = len(soupResults)
    columnNumber= len([columnElement for columnElement in soupResults[0].find_all(soupResults)]) #CHANGE - find a way that this can make legible; seems silly this is the best way to get column count
    return [rowNumber,columnNumber]

def makePandasDF(columnNames, rowData):
    pass

      