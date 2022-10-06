import csv
import os.path
import re
import time

import pandas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


data = pandas.read_csv('artemis_dataset_release_v0.csv', sep=',')


driver = webdriver.Chrome('chromedriver.exe')
driver.maximize_window()


def checkCopyRight(query):
    try:
        try:
            box = driver.find_element_by_xpath('/html/body/div[2]/header/nav/form/a[3]')
            box.click()
            box = driver.find_element_by_xpath('/html/body/div[2]/header/nav/form/a[1]/input')
            box.send_keys(query)
            time.sleep(1)
            box = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/header/nav/form/a[1]/ul/li[1]'))
            )
            box.click()
            time.sleep(1.5)
            copyrightStamp = driver.find_element_by_xpath('/html/body/div[2]/div[1]/section[1]/'
                                                          'main/div[2]/aside/div[2]/div[1]/div[1]/a')
            fairuseStamp = ''
            try:
                fairuseStamp = driver.find_element_by_xpath('/html/body/div[2]/div[1]/section[1]/main/div[2]/aside/'
                                                            'div[2]/div[1]/div[1]/a[2]')
            except:
                print("couldn't find fair use stamp")
            if 'public domain' in copyrightStamp.text.lower() or 'fair use' in fairuseStamp.text.lower():
                safeList.append(query)
            else:
                badList.append(query)

        except:
            unsureList.append(query)
    except:
        print("oops")

files = []
listOfDir = os.listdir('C:\\Users\\danie\\PycharmProjects\\PaintingPlayground\\ArtSamples-300 each')
for dir in listOfDir:
    files.append(os.listdir('C:\\Users\\danie\\PycharmProjects\\PaintingPlayground\\ArtSamples-300 each\\' + dir))

safeList = []
badList = []
unsureList = []
driver.get('https://www.wikiart.org/')
for file in files:
    for subfile in file:
        test = subfile
        test = re.sub('(_|-)', ' ', test)
        test = re.sub('([0-9])', '', test)
        test = re.sub('(.png)', '', test)
        checkCopyRight(test)

safeCSV = open('safeList.csv', 'w+', newline ='')
with safeCSV:
    write = csv.writer(safeCSV)
    write.writerows(safeList)
badCSV = open('badList.csv', 'w+', newline ='')
with badCSV:
    write = csv.writer(badCSV)
    write.writerows(badList)
unsureCSV = open('unsureList.csv', 'w+', newline ='')
with unsureCSV:
    write = csv.writer(unsureCSV)
    write.writerows(unsureList)
driver.close()
