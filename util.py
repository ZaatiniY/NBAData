from bs4 import BeautifulSoup
import time 
from urllib.request import urlopen

#readWebPageHTML will give you the HTML version of a website
#   parameters:
#       - link - string; website link 
#   return->    htmlTree - interpretted website link as the proper html format
def readWebPageHTML(link):
    with urlopen(link) as response:
        htmlTree = response.read()
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



def ppgRegTableSearch(soup):
    table = soup.find_all(id="per_game-team")
    tableRows = table[0].tbody.find_all("tr")
    return tableRows    


      