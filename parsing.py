import pandas
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import os


data = pandas.read_csv('WikiArt-Emotions-All.tsv', sep='\t')

df = pandas.DataFrame(data)
cols = [2, 3, 4, 6, 7, 30, 34, 35, 37, 43, 5]
df = df[df.columns[cols]]


def getImages(i, row):
    try:
        query = row[1] + " " + row[2] + " " + row[10]
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
            img.screenshot('Download-Location' +
                           query + ' (' + str(i) + ').png')
            time.sleep(.5)
        except:
            print("fight captcha")
            time.sleep(60)
    except:
        print("oops")


count = 0
driver = webdriver.Chrome('chromedriver.exe')
driver.maximize_window()

for index, row in df.iterrows():
    if ((row[0] == 'Impressionism' or
         row[0] == 'Expressionism' or
         row[0] == 'Abstract Art' or
         row[0] == 'Abstract Expressionism' or
         row[0] == 'Post-Impressionism') and
            row[4] == 'none' and
            row[3] == 'yes'):
        anger = row[5]
        disgust = row[6]
        fear = row[7]
        happiness = row[8]
        sadness = row[9]
        if (anger > max(disgust, fear, happiness, sadness)):
            os.chdir("C:\\Users\danie\\PycharmProjects\\PaintingPlayground\\anger")
            getImages(1, row)
            count += 1

        elif (disgust > max(anger, fear, happiness, sadness)):
            os.chdir("C:\\Users\danie\\PycharmProjects\\PaintingPlayground\\disgust")
            getImages(1, row)
            count += 1


        elif (fear > max(disgust, anger, happiness, sadness)):
            os.chdir("C:\\Users\danie\\PycharmProjects\\PaintingPlayground\\fear")
            getImages(1, row)
            count += 1


        elif (happiness > max(disgust, fear, anger, sadness)):
            os.chdir("C:\\Users\danie\\PycharmProjects\\PaintingPlayground\\happiness")
            getImages(1, row)
            count += 1


        elif (sadness > max(disgust, fear, happiness, anger) and sadness > .2):
            os.chdir("C:\\Users\danie\\PycharmProjects\\PaintingPlayground\\sadness")
            getImages(1, row)
            count += 1
        print(index)

# Finally, we close the driver
driver.close()
