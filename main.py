# selenium library used to click buttons
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

from bs4 import BeautifulSoup
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
# TODO ADD HEADLESS STATE
#Install Driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
stores_url = "https://emap.pcsc.com.tw/emap.aspx#"
driver.get(stores_url)

keelung_button = driver.find_element(by=By.XPATH, value='//*[@id="maplink_keelung"]')
keelung_button.click()
time.sleep(2)
zhongzheng_button = driver.find_element(by=By.XPATH, value='//*[@id="town_中正區"]')
zhongzheng_button.click()
time.sleep(2)  # sleep for two second in the beginning of page and then scroll to the bottom of the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(4) #sleep to get all the items loaded

#on zhongzheng page
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')
# print('soup:')
# print(soup)
# search_resultsXPath = '//*[@id="seardh_bar_list"]'

storesList = soup.find(id='seardh_bar_list', title='storeslist')
table = storesList.tbody

# tr is a table row, represents one store entry
for tr in table:
    for td in tr:
        storeInfo = td.find_all('tr')
        # text = storeInfo.td.text
        for tr in storeInfo:
            # storeAddress = tr.find('地址')
            if tr.td:
                print(tr.td.text)
                print('\n')
    # addresses = tr.find('地址')
    # print(addresses)
    # if table row has data we are looking for
    # tableData = tr.td
    # print(tr)
    # print('\n')

    # first_td = tr.find('td')
    # text = first_td.renderContents()
    # print(text)
    # print('\n')

# TODO: for some reason full html not being read so can't scrape, close!!!
# storeName = stores.find('td', align_="center").text
# storeElements = soup.find_all(string='門市店名：')
# print(storeElements)
# for store in storeElements:
# # a for append, add to file 'w' will overwrite existing info
#     with open(f'addresses.txt', 'a') as f:
#         storeName = store.find('td', align_='center').text
#         print(storeName)
#         f.write(f"name: {storeName} \n")
# driver.implicitly_wait(10)
# ActionChains(driver).move_to_element(button).click(button).perform()
# while True:
#     # do whatever you want
#     try:
#         driver.find_element_by_xpath('//*[@id="maplink_keelung"]').click()
#     except NoSuchElementException:
#         break
# btn = driver.find_element("maplink_keelung")
# print(btn)
# btn.click()
# print(driver.get(stores_url))

# returns list of County buttons
def getCountyButtons():
    buttonElements = []
    driver.find_element_by_id("a")
    return buttonElements

def find_stores():
    html_text = requests.get(stores_url).text
    # simulate click for keelung
    # <a href="#" class="n_1" id="maplink_keelung">基隆市</a>
    soup = BeautifulSoup(html_text, 'lxml')
    # find(htmlTag, )
    stores = soup.find_all('a', class_="n_1", string="地址")
    for store in stores:
    # a for append, add to file 'w' will overwrite existing info
        with open(f'addresses.txt', 'a') as f:
            county = store.text
            print(county)
            f.write(f"name: {county} \n")
        # if '地址' in store:
        #     store_name = store.find()
        #     store_address = store.text
        #     # more_info = store.header.h2.a['href']
        #     with open(f'addresses.txt', 'w') as f:
        #         f.write(f"Store Name: {store_name.strip()}") #strip removes spaces/indents
        #         f.write(f"Address: {store_address.strip()}")
        # county.text.replace(' ','')
    # print(county_name)
    # open file and read
    # with open('home.html', 'r') as html_file:
    #     content = html_file.read() #replace w/ 711 website
    #     soup = BeautifulSoup(content, 'lxml')
    #     # use web inspect to find tag
    #     # addresses = soup.find_all('td', '地址')
    #     course_tags = soup.find_all('div', class_='card')
    #     for course in course_tags:
    #         course_name = course.h5.text
    #         course_price = course.a.text

# if __name__ == '__main__':
#     find_stores()
