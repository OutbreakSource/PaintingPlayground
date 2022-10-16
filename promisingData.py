import pandas
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import os, os.path
import fnmatch
import re
import csv



data = pandas.read_csv('artemis_dataset_release_v0.csv', sep=',')

count = 0
driver = webdriver.Chrome('chromedriver.exe')
driver.maximize_window()


def getImages(i, row, occurence):
    try:
        query = row[1]
        driver.get('https://images.google.com/')
        try:
            box = driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
            box.send_keys(query)
            box.send_keys(Keys.ENTER)
            # XPath of each image
            img = driver.find_element_by_xpath(
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
    with open("C:\\Users\\danie\\PycharmProjects\\PaintingPlayground\\fixedLists\\badList.csv", "r") as f:
        reader = csv.reader(f)
        if any(title in item for item in reader):
            return True
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
        os.chdir('C:\\Users\\danie\\PycharmProjects\\PaintingPlayground\\ArtSamples-300 each\\' + emotion)
        cwd = os.getcwd()
        title = str(occur) + '--' + row[1] + '.png'
        if title not in fnmatch.filter(os.listdir(cwd), '*.*') and not refactorTitle(title):
            if len(fnmatch.filter(os.listdir(cwd), '*.*')) < 300:
                getImages(1, row, occur)
                print(os.getcwd())



driver.close()
