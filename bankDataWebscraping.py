import re
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

class BankingWebdataScrapper:
    # Global WebDriver instance
    driver = None

    #hoteldf=pd.DataFrame(columns=['HotelName','HotelAreaName','Price','Discount','NumberOfAmenities'])
    def __init__(self):
        self.driver=None
        #creating pandas dataframe to collect data 
        self.savingRatedf=pd.DataFrame(columns=['BankName','Rating','ServiceCharge','APY','MinBalance','EstEarnfor50000'])
        self.cdRatedf=pd.DataFrame(columns=['BankName','Rating','EarlyWithDrawalPenalty','APY','MinEarn','MinDeposit'])
        self.checkingRatedf=pd.DataFrame(columns=['BankName','Rating','ServiceCharge','APY','MinEarn','MinDeposit'])
        self.moneyMarketRatedf=pd.DataFrame(columns=['BankName','Rating','ServiceCharge','APY','MinEarn','MinDeposit'])
        #xpath_declaration
        self.xpath_bankname="//div[@class='bankName']"
        self.xpath_rating="//div[@class='ratingReviews']"
        self.xpath_APY="//div[@class='flexCol apyCol secCol section']"
        self.xpath_col2="//div[@class='flexCol secCol section'][1]"
        self.xpath_col3="//div[@class='flexCol secCol section'][2]"
        self.xpath_col4="//div[@class='flexCol secCol section'][3]"
        self.xpath_next="//div[contains(text(),'Next')]"
    
    def setup_driver(self):
        options = Options()
     
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
    
        return webdriver.Chrome(service=service, options=options)
        
    def openurl(self,url):
        self.driver=self.setup_driver()
        self.driver.get(url)
        self.driver.set_window_size(1920, 1080)
    
    def scrapeDataFromTable(self):
        webelement_banknames=self.driver.find_elements(By.XPATH,self.xpath_bankname)
        webelement_rating=self.driver.find_elements(By.XPATH,self.xpath_rating)
        webelement_APY=self.driver.find_elements(By.XPATH,self.xpath_APY)
        webelement_col2=self.driver.find_elements(By.XPATH,self.xpath_col2)
        webelement_col3=self.driver.find_elements(By.XPATH,self.xpath_col3)
        webelement_col4=self.driver.find_elements(By.XPATH,self.xpath_col4)

        return webelement_banknames,webelement_rating,webelement_APY,webelement_col2,webelement_col3,webelement_col4
    

    def closeBrowser(self):
        if self.driver:
            self.driver.quit()
            self.driver=None

    
    def savingsAccountRates(self):
        #open browser
        self.openurl("https://www.depositaccounts.com/savings/")
        wait=WebDriverWait(self.driver,10)
        i=0
        for j in range(0,10):
            time.sleep(5)  
            try: 
                for bankname,rating,apy,servicechg,minbal,estearn in zip(*self.scrapeDataFromTable()):
                    self.savingRatedf.loc[i,'BankName']=bankname.text
                    #print("Bankname is",bankname.text)
                    self.savingRatedf.loc[i,'Rating']=rating.text.split("\n")[0]
                    #print("Rating is",rating.text)
                    self.savingRatedf.loc[i,'APY']=apy.text
                    self.savingRatedf.loc[i,'ServiceCharge']=servicechg.text
                    self.savingRatedf.loc[i,'MinBalance']=minbal.text
                    self.savingRatedf.loc[i,'EstEarnfor50000']=estearn.text
                    i=i+1    
                self.driver.find_element(By.XPATH,self.xpath_next).click()
            

            except Exception as e:
                
                print("the error is",str(e))   
        #print(len(webelement_banknames))
        print(self.savingRatedf)
        self.closeBrowser()


    def cdRates(self):
    
        #open browser
        self.openurl("https://www.depositaccounts.com/cd/")
        i=0
        for j in range(0,10):
            time.sleep(5)  
            try:
                for bankname,rating,apy,withdrw,minearn,mindep in zip(*self.scrapeDataFromTable()):
                    self.cdRatedf.loc[i,'BankName']=bankname.text
                    self.cdRatedf.loc[i,'Rating']=rating.text.split("\n")[0]
                    self.cdRatedf.loc[i,'APY']=apy.text
                    self.cdRatedf.loc[i,'EarlyWithDrawalPenalty']=withdrw.text
                    self.cdRatedf.loc[i,'MinEarn']=minearn.text
                    self.cdRatedf.loc[i,'MinDeposit']=mindep.text
                    i=i+1
                self.driver.find_element(By.XPATH,self.xpath_next).click()
            except Exception as e:
                print("the error is",str(e))       
        #print(len(webelement_banknames))
        print(self.cdRatedf)
        self.closeBrowser()

    def checkingAccountRates(self):
    
        #open browser
        self.openurl("https://www.depositaccounts.com/checking/")

        i=0
        for j in range(0,6):
            time.sleep(5)  
            try:
                for bankname,rating,apy,servicecharge,minearn,mindep in zip(*self.scrapeDataFromTable()):
                    self.checkingRatedf.loc[i,'BankName']=bankname.text
                    self.checkingRatedf.loc[i,'Rating']=rating.text.split("\n")[0]
                    self.checkingRatedf.loc[i,'APY']=apy.text
                    self.checkingRatedf.loc[i,'ServiceCharge']=servicecharge.text
                    self.checkingRatedf.loc[i,'MinEarn']=minearn.text
                    self.checkingRatedf.loc[i,'MinDeposit']=mindep.text
                    i=i+1
                self.driver.find_element(By.XPATH,self.xpath_next).click()
            except Exception as e:
                print("the error is",str(e))       
        #print(len(webelement_banknames))
        print(self.checkingRatedf)
        self.closeBrowser()
    
    def moneyMarketRates(self):
    
        #open browser
        self.openurl("https://www.depositaccounts.com/moneymarket/")
        i=0
        for j in range(0,9):
            time.sleep(5)  
            try:
                for bankname,rating,apy,servicecharge,minearn,mindep in zip(*self.scrapeDataFromTable()):
                    self.moneyMarketRatedf.loc[i,'BankName']=bankname.text
                    self.moneyMarketRatedf.loc[i,'Rating']=rating.text.split("\n")[0]
                    self.moneyMarketRatedf.loc[i,'APY']=apy.text
                    self.moneyMarketRatedf.loc[i,'ServiceCharge']=servicecharge.text
                    self.moneyMarketRatedf.loc[i,'MinEarn']=minearn.text
                    self.moneyMarketRatedf.loc[i,'MinDeposit']=mindep.text
                    i=i+1
                self.driver.find_element(By.XPATH,self.xpath_next).click()
            except Exception as e:
                print("the error is",str(e))      
        #print(len(webelement_banknames))
        print(self.checkingRatedf)
        self.closeBrowser()

if __name__ == "__main__":
    scraper = BankingWebdataScrapper()       # Create an object of the class
    scraper.savingsAccountRates()
    scraper.cdRates()
    scraper.checkingAccountRates()
    scraper.moneyMarketRates()
    

        
