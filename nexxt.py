# python -m pip install mysql-connector-python

import requests
import mysql.connector
from datetime import datetime
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

        self.db_connect()
   

    def db_connect(self):
        self.db_connect = mysql.connector.connect(
                    host=self.db_host,
                    user=self.db_user,
                    password=self.db_pass,
                    database=self.db_name
                )
        self.db_cursor = self.db_connect.cursor()


    def insert(self, table, data):
        cols = list(data.keys())
        
        vals = [data[i] for i in cols]

        cols = ','.join(cols)
        # vals = '"{0}"'.format('", "'.join(vals))
      
        sql = f"INSERT INTO {table} ({cols}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # print(sql)
    
        self.db_cursor.execute(sql, vals)

        self.db_connect.commit()


class Nexxt():

    source = "nexxt-change.org"

    def __init__(self, url, driver_path):
        self.url = url
        self.driver_path = Service(driver_path)
        
        # RUN SET BROWSER METHOD
        self.set_browser()

    def __del__(self):
        self.browser.close()

    
    def set_browser(self):
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--log-level=3')
        self.browser = webdriver.Chrome(service=self.driver_path, options=options)


    def get_article_list(self):
        # OPEN URL
        self.browser.get(self.url)
        # self.browser.implicitly_wait(5)
        sleep(5)

        # CLICK Search 
        self.browser.find_element(By.XPATH, "//button[@value='Suchen']").click()
        
        # FIND LAST PAGE
        page_count = self.browser.find_elements(By.CLASS_NAME, "pagination-item")[-2].text
        
        # COLLECT ALL LINKS IN LIST
        article_links = [] 

        for i in range(10):
            sleep(2)
            # FIND ALL ARTICLES ON PAGE
            all_articles = self.browser.find_elements(By.CLASS_NAME, "card-title")
            
            for article in all_articles:
                link = article.find_element(By.TAG_NAME, 'a')
                article_links.append(link.get_attribute('href'))
            
            next_btn = self.browser.find_elements(By.CLASS_NAME, "pagination-item")[-1]

            # GO TO NEXT PAGE
            if next_btn:
                next_btn.click()
        

        for link in article_links:
            print(link)
        
        print("----------------------------------------")
        print(f"Link Count: {len(article_links)}")
        print("----------------------------------------")

        return article_links


    def parse_data(self, link):
        
        page_data = {}

        # link = "https://www.nexxt-change.org/DE/Verkaufsangebot/Detailseite/detailseite_jsp.html?cms_adId=179101"

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(link, headers=headers).content
        
        soup = BeautifulSoup(response, 'lxml')
        
        # MAIN CONTENT SECTION
        content_div = soup.find('div', {'class': 'inserat-details'})

        # TITLE
        page_data['title'] = content_div.find('h1').text
                
        # DESCRIPTION
        page_data['description'] = content_div.find_all('p')[1].text
        
        details = content_div.find("dl", {'class':'lined'})
        dds = details.find_all('dd')
        
        # LOCATION
        page_data['location'] = dds[0].text.strip()

        # INDUSTRY
        page_data['industry'] = dds[1].text.strip()

        # NUMBER OF EMPLOYEE
        page_data['number_of_employee'] = dds[2].text.strip()

        # LAST ANNUAL REVENUE
        page_data['last_annual_revenue'] = dds[3].text.strip()

        # ASKING PRICE
        page_data['asking_price'] = dds[4].text.strip()

        # SIDEBAR SECTION
        sidebar_div = soup.find('div', {'class': 'sidebar'})
        dds = sidebar_div.find_all('dd')
        
        # ADD DATE
        ad_date = dds[0].text
        date_time_obj = datetime.strptime(ad_date, '%d.%m.%Y')
        
        page_data['ad_date'] = date_time_obj.strftime("%Y-%m-%d")

        # BOX NUMBER
        page_data['box_number'] = dds[1].text
        
        # ADD TYPE
        page_data['ad_type'] = dds[2].text

        # -------------------------------------
        contact_p = sidebar_div.find_all('p')

        # PARTNER CONTRACT
        partner_contact = contact_p[0].text.strip()
        partner_contact_link = contact_p[1].text.strip()

        page_data['partner_contact'] = '';

        for cl in partner_contact_link:
            page_data['partner_contact'] += cl.strip()
        

        # CONTRACT PERSON
        page_data['contact_person'] = contact_p[-1].text.strip()

        # URL DETAILS
        page_data['url'] = link
        page_data['source'] = self.source

        print(page_data)

        return page_data
        
        

    
    def save_in_db(self, page_data):
        pass
        # DATA STRUCTURE
        # page_data['title'] = 
        # page_data['description'] = 
        # page_data['location'] = 
        # page_data['industry'] = 
        # page_data['number_of_employee'] = 
        # page_data['last_annual_revenue'] = 
        # page_data['asking_price'] = 
        # page_data['ad_date'] = 
        # page_data['box_number'] = 
        # page_data['ad_type'] = 
        # page_data['partner_contact'] = 
        # page_data['contact_person'] = 
        # page_data['url'] = 
        # page_data['source'] = 





if __name__ == '__main__':

    # DB SETUP
    db = DataStore("localhost", "root", "", "nexxt")
    # cur = db.db_connect()

    # SCRAPPER SETUP 
    url = "https://www.nexxt-change.org/DE/Verkaufsangebot/inhalt.html"
    driver_path = "chromedriver.exe"

    scrap = Nexxt(url, driver_path)
    
    # GET ALL LINKS FROM PAGE
    article_links = scrap.get_article_list()
    
    # GET PAGE DATA FOR EACH PAGE
    for link in article_links:
        print(link)
        page_data = scrap.parse_data(link)
        sleep(1)

        db.insert('nexxt_data_tbl', page_data)
    

