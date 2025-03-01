import util
import urllib.request
from urllib.error import HTTPError
import time
import pandas as pd 
import numpy as np


startLink = 'https://www.basketball-reference.com/leagues/'
htmlStart = util.readWebPageHTML(startLink)
soupStart= util.transformToSoupHP(htmlStart)

class Scrape():
    def __init__(self,website):
        self.startLink = website
        self.lag = 1
        self.counter = 0
        self.state = "START"
    
    def simRun(self):
        htmlStart = util.readWebPageHTML(startLink)
        soupStart= util.transformToSoupHP(htmlStart)
        seasons = soupStart.find_all(attrs = {"data-stat":"season"})
        links = self.getSeasonLinks(seasons)
        print(links)
        correctedLinks = self.editSeasonLinks(links) 
        self.goThroughSeasonLinks(correctedLinks,test = 1)


#remove test variable once you're done 
    def goThroughSeasonLinks(self,seasonLinks,test):
        index = 0
        while index < len(seasonLinks) and index< test:
            try:
                input(f"This is the current season {seasonLinks[index]}")
                print(index)
                time.sleep(3)
                htmlSeason = util.readWebPageHTML(seasonLinks[index])
                seasonSoup = util.transformToSoupHP(htmlSeason)
                statRows = util.posRegTableSearch(seasonSoup)
                print(statRows)
                #print(statRows[0].find_all('td')[4].string) #just testing how to use .string to get the value in the table 
                
                self.adjustSiteCount(index)
                index += 1
                

            except HTTPError as e:
                if e == 429:
                    print("fail")

    def playoffsDataPull(self,index):
        pass

    def adjustSiteCount(self,index):
        pass

# go back and try this one again once you have more time with it 
    def getSeasonLinks(self,treeSearch):
        treeSearch.pop(0) #removing misc search result grabbed from search; second search is to pop 2025 lol
        links = [searchResult.a.get("href") for searchResult in treeSearch]
        return links

    def editSeasonLinks(self,baseLinks):
        newLinks = [('https://www.basketball-reference.com' + x) for x in baseLinks]
        return newLinks 

sim = Scrape(startLink)
sim.simRun()



        

