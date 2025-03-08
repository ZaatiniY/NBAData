from selenium import webdriver 
import time 
from bs4 import BeautifulSoup 



def soupFromSelBrowser(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(2) #EDIT - building buffer time to let the dynamic content show up before searching
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content,'html.parser')
    return soup
