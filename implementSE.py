from selenium import webdriver 
import time 
from bs4 import BeautifulSoup 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def startSelBrowser(url,currID):
    chromeOptions = Options()
    chromeOptions.add_argument('--headless=new')
    driver = webdriver.Chrome(options = chromeOptions)
    driver.get(url)
    #driver.implicitly_wait(0.5) #DELETE - building buffer time to let the dynamic content show up before searching    
    element = EC.presence_of_element_located((By.ID,currID))
    wait = WebDriverWait(driver,2)
    wait.until(element)
    return driver 

def soupFromSelBrowser(driver,url):
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content,'html.parser')
    return soup

def endcurrentDriver(driver):
    driver.quit()

#------------------------------------------------------------------------------------------------------------------------------------------------------

def testStartSelBrowser(url):
    chromeOptions = Options()
    chromeOptions.add_argument('--headless=new')
    driver = webdriver.Chrome(options = chromeOptions)
    driver.get(url)
    driver.implicitly_wait(0.5) #EDIT - building buffer time to let the dynamic content show up before searching    
    return driver 

def testSoupFromSelBrowser(driver,url):
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content,'html.parser')