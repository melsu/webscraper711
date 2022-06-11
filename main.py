# selenium library used to click buttons
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time

from bs4 import BeautifulSoup
import requests
import xlsxwriter

def initDriver():
    global driver
    #Install Driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    stores_url = "https://emap.pcsc.com.tw/emap.aspx#"
    driver.get(stores_url)

def getAllServicesDict():
    global servicesDict
    servicesDict = dict()
    servicesList = soup.find(id='menu_scroll', class_='s_scroll')
    servicesNames = servicesList.find_all('div')
    # starting col in excel sheet
    col = 4
    for sN in servicesNames:
        name = sN.text.strip()
        servicesDict[name] = col
        col += 1
    return servicesDict

def initExcelSheet():
    global workbook
    global worksheet
    # keep track of next excel row
    global row
    getAllServicesDict()
    storeInfoList = ['county', 'district', 'name', 'address']
    workbook = xlsxwriter.Workbook('storeData711.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    for label in (storeInfoList):
        worksheet.write(row, col, label)
        col += 1
    for service in (servicesDict):
        worksheet.write(row, col, service)
        col += 1
    row = 1

# @arg - storeInfo [name, address]
def inputStoreInfoExcel(storeInfo):
    print(storeInfo)
    print(row)
    worksheet.write(row, 2, storeInfo[0])
    worksheet.write(row, 3, storeInfo[1])

# @arg - services [names of services offered]
def inputServicesExcel(services):
    if services: # check not an empty list
        for s in services:
            # value of 1 indicates service is offered
            col = servicesDict[s]
            worksheet.write(row, col, 1)

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

# scrapes data from a single webpage
def scrapeStores(soup):
    global row
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
                inputServicesExcel(services)
                row += 1 #increment excel row

def main():
    global soup
    initDriver()
    # TODO click into all counties and cities
    # for scaling, have list of maplinks and towns
    # click buttons for next pages
    keelung_button = driver.find_element(by=By.XPATH, value='//*[@id="maplink_keelung"]')
    keelung_button.click()

    zhongzheng_button = driver.find_element(by=By.XPATH, value='//*[@id="town_中正區"]')
    zhongzheng_button.click()
    time.sleep(2)  # sleep for two second in the beginning of page and then scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4) #sleep to get all the items loaded
    #on zhongzheng page
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    initExcelSheet()
    scrapeStores(soup)
    try:
        nextButton = driver.find_element(by=By.XPATH, value='//*[@id="Next"]')
    except NoSuchElementException:
        nextButton = False
    while nextButton:
        nextButton.click()
        time.sleep(2)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        scrapeStores(soup)
        try:
            nextButton = driver.find_element(by=By.XPATH, value='//*[@id="Next"]')
        except NoSuchElementException:
            nextButton = False
    workbook.close()

if __name__ == "__main__":
    main()
