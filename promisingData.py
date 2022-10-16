import pandas
import pandas
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import os, os.path
import fnmatch
import re
import csv

from selenium.webdriver.support.wait import WebDriverWait

data = pandas.read_csv('artemis_dataset_release_v0.csv', sep=',')

count = 0
driver = webdriver.Chrome('chromedriver.exe')
driver.maximize_window()


def getImages(i, row, occurence):
    try:
        query = row[1]
        driver.get('https://images.google.com/')
        try:
            box = driver.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
            box.send_keys(query)
            box.send_keys(Keys.ENTER)
            # XPath of each image
            img = driver.find_element('xpath',
                                      '//*[@id="islrg"]/div[1]/div[' +
                                      str(i) + ']/a[1]/div[1]/img')
            time.sleep(.5)
            score = str(occurence) + "-"
            img.screenshot(score + "-" + row[1] + '.png')
            time.sleep(.5)
        except:
            print("fight captcha")
            time.sleep(60)
    except:
        print("oops")


def refactorTitle(title):
    title = re.sub('(_|-)', ' ', title)
    title = re.sub('([0-9])', '', title)
    title = re.sub('(.png)', '', title)
    return title

def checkInBadList(title):
    with open("fixedLists\\badList.csv", "r") as f:
        reader = csv.reader(f)
        if any(title in item for item in reader):
            return True
    return False
def checkCopyRight(query):
    """
    I rather die than write doc-strings
    :param query: it's the query
    """
    driver.get('https://www.wikiart.org/')
    try:
        box = driver.find_element('xpath', '/html/body/div[2]/header/nav/form/a[3]')
        box.click()
        box = driver.find_element('xpath', '/html/body/div[2]/header/nav/form/a[1]/input')
        box.send_keys(query)
        time.sleep(1)
        box = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/header/nav/form/a[1]/ul/li[1]'))
        )
        box.click()
        time.sleep(1.5)
        try:
            notFound = driver.find_element('xpath', '/html/body/div[2]/div[1]/section/main/div/h5')

            if notFound.text == 'sorry, nothing found':
                with open('unsureList.csv', 'a') as fd:
                    writer = csv.writer(fd)
                    writer.writerow([query])
        except:
            print("found object")
        copyrightStamp = driver.find_element('xpath', '/html/body/div[2]/div[1]/section[1]/'
                                                      'main/div[2]/aside/div[2]/div[1]/div[1]/a')
        try:
            fairsStamp = driver.find_element('xpath', '/html/body/div[2]/div[1]/section[1]/main/div[2]/aside/'
                                                      'div[2]/div[1]/div[1]/a[2]')
        except:
            fairsStamp = ''

        if 'public domain' in copyrightStamp.text.lower() or 'fair use' in fairsStamp.text.lower():
            return True
    except:
        return False


for index, row in data.iterrows():
    if (row[0] == 'Impressionism' or
        row[0] == 'Expressionism' or
        row[0] == 'Abstract Art' or
        row[0] == 'Abstract_Expressionism' or
        row[0] == 'Post-Impressionism' or
        row[0] == 'Neo-Expressionism' or
        row[0] == 'Lyrical Abstraction' or
        row[0] == 'Color_Field_Painting') and not row[2] == 'something else':
        art = row[1]
        emotion = row[2]
        occur = row[4]
        os.chdir('ArtSamples-300 each\\' + emotion)
        cwd = os.getcwd()
        title = str(occur) + '--' + row[1] + '.png'
        copyrightName = refactorTitle(title)
        if title not in fnmatch.filter(os.listdir(cwd), '*.*') and not checkInBadList(copyrightName):
            if len(fnmatch.filter(os.listdir(cwd), '*.*')) < 300:
                if checkCopyRight(copyrightName):
                    getImages(1, row, occur)
                    print(os.getcwd())
                else:
                    with open('fixedLists\\badList.csv', 'a') as fd:
                        writer = csv.writer(fd)
                        writer.writerow([copyrightName])

driver.close()
