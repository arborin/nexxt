import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support.ui import 



class DataStore():

    def __init__(self, db_host, db_user, db_pass, db_name):
        self.db_host = db_host
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name


class Nexxt():

    def __init__(self, url, driver_path):
        self.url = url
        self.driver_path = Service(driver_path)
        
        # RUN SET BROWSER METHOD
        self.set_browser()

    
    def set_browser(self):
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--log-level=3')
        self.browser = webdriver.Chrome(service=self.driver_path, options=options)


    def get_article_list(self):
        # OPEN URL
        self.browser.get(self.url)
        self.browser.implicitly_wait(3)

        # CLICK Search 
        self.browser.find_element(By.XPATH, "//button[@value='Suchen']").click()
        
        # FIND ALL ARTICLES
        all_articles = self.browser.find_elements(By.CLASS_NAME, "card-title")
        
        print()
        for article in all_articles:
            print('-----------------------------------------------------')
            link = article.find_element(By.TAG_NAME, 'a')
            print(link.get_attribute('href'))
            # self.browser.execute_script("window.open('https://google.com')")

            # article.click()

            # self.browser.back()

            


    def parse_data(self, page_html):
        pass
        # soup = BeautifulSoup(response, 'lxml')
        print(page_html)

if __name__ == '__main__':

    url = "https://www.nexxt-change.org/DE/Verkaufsangebot/inhalt.html"
    driver_path = r"C:\Users\admin\Desktop\chromedriver.exe"

    scrap = Nexxt(url, driver_path)
    scrap.get_article_list()

