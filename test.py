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
        print(links)
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
                #regSeasonDFs = self.createDFs(seasonSoup,index,regSeasonDFs,seasonLinks[index])
                self.printAllDFs(regSeasonDFs)
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

    def createDFs(self,seasonSoup,index,allDFs,seasonLink):
        if index == 0:
            perPosDF = util.regTableSearch(seasonSoup,"per_poss-team",seasonLink)
            advStatDF = util.regTableSearch(seasonSoup,"advanced-team",seasonLink)
            shootDF = util.regTableSearch(seasonSoup,"shooting-team",seasonLink)
            allDFs = [perPosDF,advStatDF,shootDF]
        else:
            for df in range(len(allDFs)):
                currSeasonDF = util.regTableSearch(seasonSoup,self.siteTableIDs[df],seasonLink)
                allDFs[df] = pd.concat([allDFs[df],currSeasonDF],ignore_index = True)
        return allDFs

sim = Scrape(startLink)
sim.simRun()



        

