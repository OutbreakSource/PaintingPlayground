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
    """
    I rather die than write doc-strings
    :param query: it's the query
    """
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
        try:
            notFound = driver.find_element_by_xpath('/html/body/div[2]/div[1]/section/main/div/h5')

            if notFound.text == 'sorry, nothing found':
                with open('unsureList.csv', 'a') as fd:
                    writer = csv.writer(fd)
                    writer.writerow([query])
        except:
            print("found object")
        copyrightStamp = driver.find_element_by_xpath('/html/body/div[2]/div[1]/section[1]/'
                                                      'main/div[2]/aside/div[2]/div[1]/div[1]/a')
        try:
            fairsStamp = driver.find_element_by_xpath('/html/body/div[2]/div[1]/section[1]/main/div[2]/aside/'
                                                      'div[2]/div[1]/div[1]/a[2]')
        except:
            fairsStamp = ''

        if 'public domain' in copyrightStamp.text.lower() or 'fair use' in fairsStamp.text.lower():
            with open('safeList.csv', 'a') as fd:
                writer = csv.writer(fd)
                writer.writerow([query])
    except:
        with open('badList.csv', 'a') as fd:
            writer = csv.writer(fd)
            writer.writerow([query])


def isItIn(name):
    flag = False
    with open("badList.csv", "r") as f:
        reader = csv.reader(f)
        if any(name in item for item in reader):
            flag = True
    with open("safeList.csv", "r") as f:
        reader = csv.reader(f)
        if any(name in item for item in reader):
            flag = True

    with open("unsureList.csv", "r") as f:
        reader = csv.reader(f)
        if any(name in item for item in reader):
            flag = True
    return flag


files = []
listOfDir = os.listdir('C:\\Users\\danie\\PycharmProjects\\PaintingPlayground\\ArtSamples-300 each')
for emotion in listOfDir:
    files.append(os.listdir('C:\\Users\\danie\\PycharmProjects\\PaintingPlayground\\ArtSamples-300 each\\' + emotion))

driver.get('https://www.wikiart.org/')
for file in files:
    for currentImage in file:
        imageName = currentImage
        imageName = re.sub('(_|-)', ' ', imageName)
        imageName = re.sub('([0-9])', '', imageName)
        imageName = re.sub('(.png)', '', imageName)
        if not isItIn(imageName):
            checkCopyRight(imageName)

driver.close()
