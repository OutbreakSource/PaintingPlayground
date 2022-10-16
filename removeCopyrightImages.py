import csv
import os.path
import re
import time

files = []
listOfDir = os.listdir('C:\\Users\\danie\\PycharmProjects\\PaintingPlayground\\ArtSamples-300 each')
for emotion in listOfDir:
    files.append(os.listdir('C:\\Users\\danie\\PycharmProjects\\PaintingPlayground\\ArtSamples-300 each\\' + emotion))


def badManChecker(name):
    flag = False
    with open("C:\\Users\\danie\\PycharmProjects\\PaintingPlayground\\fixedLists\\badList.csv", "r") as f:
        reader = csv.reader(f)
        if any(name in item for item in reader):
            flag = True
    return flag


count = 0
for file in files:
    for currentImage in file:
        imageName = currentImage
        imageName = re.sub('(_|-)', ' ', imageName)
        imageName = re.sub('([0-9])', '', imageName)
        imageName = re.sub('(.png)', '', imageName)
        if badManChecker(imageName):
            try:
                os.remove("C:\\Users\\danie\\PycharmProjects\\PaintingPlayground\\ArtSamples-300 each\\anger\\"
                          + currentImage)
            except:
                print("not in anger")
            try:
                os.remove("C:\\Users\\danie\\PycharmProjects\\PaintingPlayground\\ArtSamples-300 each\\awe\\"
                          + currentImage)
            except:
                print("not in awe")
            try:
                os.remove("C:\\Users\\danie\\PycharmProjects\\PaintingPlayground\\ArtSamples-300 each\\contentment\\"
                          + currentImage)
            except:
                print("not in contentment")
            try:
                os.remove("C:\\Users\\danie\\PycharmProjects\\PaintingPlayground\\ArtSamples-300 each\\disgust\\"
                          + currentImage)
            except:
                print("not in disgust")
            try:
                os.remove("C:\\Users\\danie\\PycharmProjects\\PaintingPlayground\\ArtSamples-300 each\\amusement\\"
                          + currentImage)
            except:
                print("not in amusement")
            try:
                os.remove("C:\\Users\\danie\\PycharmProjects\\PaintingPlayground\\ArtSamples-300 each\\fear\\"
                          + currentImage)
            except:
                print("not in fear")
            try:
                os.remove("C:\\Users\\danie\\PycharmProjects\\PaintingPlayground\\ArtSamples-300 each\\sadness\\"
                          + currentImage)
            except:
                print("not in sadness")
            try:
                os.remove("C:\\Users\\danie\\PycharmProjects\\PaintingPlayground\\ArtSamples-300 each\\excitement\\"
                          + currentImage)
            except:
                print("not in excitement")




print(count)
