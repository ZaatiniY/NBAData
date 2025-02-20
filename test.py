import util
import urllib.request
from urllib.error import HTTPError
import time


startLink = 'https://www.basketball-reference.com/leagues/'
htmlStart = util.readWebPageHTML(startLink)
soupStart= util.transformToSoupHP(htmlStart)

class Scrape():
    def __init__(self,website):
        self.startLink = website
        self.lag = 1
        self.counter = 0
    
    def simRun(self):
        htmlStart = util.readWebPageHTML(startLink)
        soupStart= util.transformToSoupHP(htmlStart)
        seasons = soupStart.find_all(attrs = {"data-stat":"season"})
        links = self.getSeasonLinks(seasons)
        correctedLinks = self.editSeasonLinks(links) 
        self.goThroughSeasonLinks(correctedLinks,test = 1)


#remove test variable once you're done 
    def goThroughSeasonLinks(self,seasonLinks,test):
        index = 0
        while index < len(seasonLinks) and index< test:
            try:
                time.sleep(3)
                htmlSeason = util.readWebPageHTML(seasonLinks[index])
                seasonSoup = util.transformToSoupHP(htmlSeason)
                statRows = util.ppgRegTableSearch(seasonSoup)
                print(statRows)
                self.adjustSiteCount(index)
                index += 1

            except HTTPError as e:
                if e == 429:
                    print("HTTP ERROR LMAO ")

    def adjustSiteCount(self,index):
        pass

# go back and try this one again once you have more time with it 
    def getSeasonLinks(self,treeSearch):
        treeSearch.pop(0) #removing misc search result grabbed from search; second search is to pop 2025 lol
        links = [searchResult.a.get("href") for searchResult in treeSearch]
        return links

    def editSeasonLinks(self,baseLinks):
        newLinks = [(self.startLink + '/' + x) for x in baseLinks]
        return newLinks 

sim = Scrape(startLink)
print(sim.simRun())



        

