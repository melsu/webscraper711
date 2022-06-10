# selenium library used to click buttons
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

from bs4 import BeautifulSoup
import requests
import xlsxwriter

#Install Driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
stores_url = "https://emap.pcsc.com.tw/emap.aspx#"
driver.get(stores_url)

# TODO click into all counties and cities
# for scaling, have list of maplinks and towns
# click buttons for next pages
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

# Helper functions for webscraping

storeInfoList = ['county', 'district', 'name', 'address']
# all 35 services available
servicesList = ['停車場', '廁所', 'ATM', '座位區', 'ibon WiFi', 'OPEN! STORE',
    '千禧血壓站', '外送咖啡服務', '霜淇淋', '台塑有機蔬菜', '美妝', 'Mister Donut甜甜圈',
    'ibon', '現萃茶', '現蒸地瓜', '統一生機', 'OPEN!兒童閱覽室', 'K·Seren', '21TOGO',
    '烘培坊', '!+? CAFE RESERVE', '博客來', '糖果屋', '日本7-ELEVEN限定',
    '國際精品專櫃', '精品咖啡', 'CITY CAFE氮氣飲品', '天素地蔬', '嚴選素材冷凍鮮物',
    '光合帕尼尼', '冷凍交貨便', '酒BAR', '寵物生活專區', '酷聖石', '甜點專櫃']

# @arg - table data of one store
# returns [store name, address]
def getStoreInfo(td):
    storeInfo = []
    tableData = td.find_all('tr')
    storeNameKey = '門市店名：'
    storeAddressKey = '地址：'
    for tr in tableData:
        data = tr.td
        if data:
            info = data.text
            if storeNameKey in info:
                storeName = info.split(storeNameKey)[-1]
                storeInfo.append(storeName)
            elif storeAddressKey in info:
                storeAddress = info.split(storeAddressKey)[-1].split('電話：')[0]
                storeInfo.append(storeAddress)
    # print(storeInfo)
    return storeInfo

# @arg - table of services for a single store
# returns list of services offered at store
def getServices(servicesTable):
    services = []
    # access icons
    table = servicesTable.tbody.find_all("td", {"class": "icon_sps_li"})
    for td in table:
        icon_img = td.img
        if icon_img:
            # print(icon_img)
            serviceName = icon_img.get('title')
            services.append(serviceName)
    # print(services)
    return services

def initExcelSheet():
    workbook = xlsxwriter.Workbook('storeData711.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    for label in (storeInfoList):
        worksheet.write(row, col, label)
        col += 1
    for service in (servicesList):
        worksheet.write(row, col, service)
        col += 1
    workbook.close()

# @arg - storeInfo [name, address]
def inputStoreInfoExcel(storeInfo):
    return

# @arg - services [names of services offered]
def inputServicesExcel(services):
    return

initExcelSheet()
# list of stores on webPage for a city/district
storesList = soup.find(id='seardh_bar_list', title='storeslist')
table = storesList.tbody #can clean this up

for store in table:
    for td in store: # column of info in a row
        storeInfo = getStoreInfo(td)
        if storeInfo:
            inputStoreInfoExcel(storeInfo)
        servicesTable = td.find("table", {"class": "icon_sps_li"})
        if servicesTable:
            services = getServices(servicesTable)
            if services:
                inputServicesExcel(services)
        # print(services)

# put in nice spreadsheet
# scale up, click through pages and counties (next button)

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
