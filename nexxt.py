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

        for i in range(3):
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


    def parse_data(self, link):
        
        link = "https://www.nexxt-change.org/DE/Verkaufsangebot/Detailseite/detailseite_jsp.html?cms_adId=179101"

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(link, headers=headers).content
        
        soup = BeautifulSoup(response, 'lxml')
        
        content_div = soup.find('div', {'class': 'inserat-details'})

        # TITLE
        title = content_div.find('h1').text
        print(f"\nTitle:\n---------------\n  {title}")
        
        # DESCRIPTION
        description = content_div.find_all('p')[1].text
        print(f"\nDescription:\n---------------\n  {description}")

        details = content_div.find("dl", {'class':'lined'})

        dds = details.find_all('dd')
        
        # LOCATION
        location = dds[0].text.strip()

        # INDUSTRY
        industry = dds[1].text.strip()

        # NUMBER OF EMPLOYEE
        number_of_employee = dds[2].text.strip()

        # LAST ANNUAL REVANUE
        last_annual_revanue = dds[3].text.strip()

        # ASKING PRICE
        asking_price = dds[4].text.strip()

        print("----------------------------------------------------")
        print(f"{location}\n{industry}\n{number_of_employee}\n{last_annual_revanue}\n{asking_price}")
        print("----------------------------------------------------")
        # ADD DATE

        # BOX NUMBER

        # ADD TYPE

        # PARTNER CONTRACT

        # CONTRACT PERSON





if __name__ == '__main__':

    url = "https://www.nexxt-change.org/DE/Verkaufsangebot/inhalt.html"
    driver_path = "chromedriver.exe"

    scrap = Nexxt(url, driver_path)
    # scrap.get_article_list()
    scrap.parse_data('111')

