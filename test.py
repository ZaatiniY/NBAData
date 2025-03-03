import util
import urllib.request
from urllib.error import HTTPError
import time
import pandas as pd 
import numpy as np
import re


startLink = 'https://www.basketball-reference.com/leagues/'
htmlStart = util.readWebPageHTML(startLink)
soupStart= util.transformToSoupHP(htmlStart)

class Scrape():
    def __init__(self,website):
        self.startLink = website
        self.lag = 1
        self.counter = 0
        self.state = "START"
        self.siteTableIDs = ["per_poss-team","advanced-team","shooting-team"]
    
    def simRun(self):
        htmlStart = util.readWebPageHTML(startLink)
        soupStart= util.transformToSoupHP(htmlStart)
        seasons = soupStart.find_all(attrs = {"data-stat":"season"})
        links = self.getSeasonLinks(seasons)
        correctedLinks = self.editSeasonLinks(links) 
        self.goThroughSeasonLinks(correctedLinks,index = 0, test = 2)


#remove test variable once you're done 
    def goThroughSeasonLinks(self,seasonLinks,index,test):
        regSeasonDFs = []
        playoffDFs = []
        while index < len(seasonLinks) and index< test:
            try:
                input(f"This is the current season {seasonLinks[index]}")
                time.sleep(3)
                htmlSeason = util.readWebPageHTML(seasonLinks[index])
                seasonSoup = util.transformToSoupHP(htmlSeason)
                regSeasonDFs = self.createDFs(seasonSoup,regSeasonDFs,seasonLinks[index])

                playoffDFs = self.runPlayoffDFSequence(seasonSoup,playoffDFs,seasonLinks[0])
                self.printAllDFs(playoffDFs)
                self.adjustSiteCountPass(index)
                index += 1
    
            except HTTPError as e:
                if e == 429:
                    print("fail")

    def printAllDFs(self,dfList):
        for x in dfList:
            print(x)

    def playoffsDataPull(self,index):
        pass

    def adjustSiteCountPass(self,index):
        pass

#CHANGE - getSeasonLinks should be in util 
    def getSeasonLinks(self,treeSearch):
        treeSearch.pop(0) #removing misc search result grabbed from search; second search is to pop 2025 lol
        links = [searchResult.a.get("href") for searchResult in treeSearch]
        return links

    def editSeasonLinks(self,baseLinks):
        newLinks = [('https://www.basketball-reference.com' + x) for x in baseLinks]
        return newLinks 



    def createDFs(self,seasonSoup,allDFs,seasonLink):
        if len(allDFs) == 0: #giving the case that your assessment period (whether it's regular season or playoffs) haven't been populated yet with data frames for analysis
            perPosDF = util.regTableSearch(seasonSoup,"per_poss-team",seasonLink) #CHANGE - change the variable name from seasonSoup to "soup", because you can use this function for playoff searches as well 
            advStatDF = util.regTableSearch(seasonSoup,"advanced-team",seasonLink)
            shootDF = util.regTableSearch(seasonSoup,"shooting-team",seasonLink)
            allDFs = [perPosDF,advStatDF,shootDF]
        else:
            for df in range(len(allDFs)):
                currSeasonDF = util.regTableSearch(seasonSoup,self.siteTableIDs[df],seasonLink)
                allDFs[df] = pd.concat([allDFs[df],currSeasonDF],ignore_index = True)
        return allDFs

#runPlayoffDFSequence is the main method that returns the DF for playoffs; it contains the if/else statement that checks there even is s playoff link; then it runs getPlayoffDFs that contains the error exception for potential HTTP issues
#Parameters:
#   regSeasonSoup (BS Object) - this is the soup that will be searched for your playoff link
#   allDFs (list) - list containing your playoff DFs
#   regSeasonLink (string) - URL for the regular season link that the code is currently working through
# Returns:
#   allDFs (list) - contains the DF specified in createDFs
    def runPlayoffDFSequence(self,regSeasonSoup,allDFs,regSeasonLink):
        referenceLink = 'https://www.basketball-reference.com/'
        year = util.getYearFromURL(regSeasonLink)
        playoffLinkSearchResults = util.findPlayoffURLLink(regSeasonSoup,year)  
        if len(playoffLinkSearchResults) > 0:
            playoffURL = util.extractPlayoffURL(playoffLinkSearchResults[0])#index 0 of the search result SHOULD be the playoff season we're looking for 
            allDFs = self.getPlayoffDFs(referenceLink,playoffURL,allDFs)
        return allDFs



    def getPlayoffDFs(self,referenceLink,playoffURL,allDFs):
        playoffSearchComplete = False
        while playoffSearchComplete is False:
            try:
                time.sleep(3)
                #ADD - sleep function to prevent HTTP errors
                playoffSoup = self.getPlayoffSoup(referenceLink + playoffURL)
                allDFs = self.createDFs(playoffSoup,allDFs,playoffURL)
            except HTTPError as e:
                if e == 429:
                    #ADD - need to add code that handles an HTTP error if it occurs 
                    pass
        return allDFs


#RIGHT NOW THIS IS WHERE YOU LEFT OFF - make sure to build the HTML search and stuff
    def getPlayoffSoup(url):
        htmlPlayoff = util.readWebPageHTML(url)
        playoffSoup = util.transformToSoupHP(htmlPlayoff)
        return playoffSoup

sim = Scrape(startLink)
sim.simRun()



        

