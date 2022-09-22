import pandas
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import os


data = pandas.read_csv('WikiArt-Emotions-All.tsv', sep='\t')

df = pandas.DataFrame(data)
cols = [2, 3, 4, 6, 7, 30, 34, 35, 37, 43, 5, 40, 39, 29]
df = df[df.columns[cols]]


def getImages(i, row, anger, disgust, fear, sadness, happiness, optimism, love, agreebleness):
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
            score = str(anger) + "-" + str(disgust) + "-" + str(fear) + "-" + str(sadness) \
                    + "-" + str(happiness) \
                    + "-" + str(optimism) + "-" + str(love) + "-" + str(agreebleness)
            img.screenshot(score + "-" + row[1] + '.png')
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
         row[0] == 'Post-Impressionism' or
         row[0] == 'Neo-Expressionism' or
         row[0] == 'Lyrical Abstraction') and
            row[3] == 'yes'):
        anger = row[5]
        disgust = row[6]
        fear = row[7]
        happiness = row[8]
        sadness = row[9]
        optimism = row[11]
        love = row[12]
        agreeableness = row[13]
        if (anger > max(disgust, fear, sadness, happiness, optimism, love, agreeableness)):
            os.chdir("C:\\Users\danie\\PycharmProjects\\PaintingPlayground\\anger")
            getImages(1, row, anger, disgust, fear, sadness, happiness, optimism, love, agreeableness)
            count += 1
        elif (disgust >max(anger, fear, sadness, happiness, optimism, love, agreeableness)):
            os.chdir("C:\\Users\danie\\PycharmProjects\\PaintingPlayground\\disgust")
            getImages(1, row, anger, disgust, fear, sadness, happiness, optimism, love, agreeableness)
            count += 1


        elif (fear > max(disgust, anger, sadness, happiness, optimism, love, agreeableness)):
            os.chdir("C:\\Users\danie\\PycharmProjects\\PaintingPlayground\\fear")
            getImages(1, row, anger, disgust, fear, sadness, happiness, optimism, love, agreeableness)
            count += 1

        elif (happiness > max(disgust, fear, sadness, anger, optimism, love, agreeableness)):
            os.chdir("C:\\Users\danie\\PycharmProjects\\PaintingPlayground\\happiness")
            getImages(1, row, anger, disgust, fear, sadness, happiness, optimism, love, agreeableness)
            count += 1


        elif (sadness > max(disgust, fear, anger, happiness, optimism, love, agreeableness)):
            os.chdir("C:\\Users\danie\\PycharmProjects\\PaintingPlayground\\sadness")
            getImages(1, row, anger, disgust, fear, sadness, happiness, optimism, love, agreeableness)
            count += 1
        elif (optimism > max(disgust, fear, anger, happiness, sadness, love, agreeableness)):
            os.chdir("C:\\Users\danie\\PycharmProjects\\PaintingPlayground\\optimism")
            getImages(1, row, anger, disgust, fear, sadness, happiness, optimism, love, agreeableness)
            count += 1
        elif (love > max(disgust, fear, sadness, happiness, optimism, anger, agreeableness)):
            os.chdir("C:\\Users\danie\\PycharmProjects\\PaintingPlayground\\love")
            getImages(1, row, anger, disgust, fear, sadness, happiness, optimism, love, agreeableness)
            count += 1
        elif (agreeableness > max(disgust, fear, sadness, happiness, optimism, love, anger)):
            os.chdir("C:\\Users\danie\\PycharmProjects\\PaintingPlayground\\agreeableness")
            getImages(1, row, anger, disgust, fear, sadness, happiness, optimism, love, agreeableness)
            count += 1
        print(index)

# Finally, we close the driver
driver.close()
