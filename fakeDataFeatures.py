import csv
import os
import random

header = ['emotion', 'harmony', 'variety', 'emphasis', 'symmetry']


def produce(emotion, writer, rank):
    for x in range(300):
        if rank >= 4:
            data = [emotion, random.randint(50, 100) / 100, random.randint(60, 100) / 100,
                    random.randint(70, 100) / 100, random.randint(50, 100) / 100]
            writer.writerow(data)
        else:
            data = [emotion, random.randint(10, 100) / 100, random.randint(20, 80) / 100,
                    random.randint(0, 80) / 100, random.randint(0, 60) / 100]
            writer.writerow(data)


with open('fakeDataSet.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    produce('amusement', writer, 2)
    produce('awe', writer, 2)
    produce('contentment', writer, 2)
    produce('excitement', writer, 2)
    produce('anger', writer, 6)
    produce('disgust', writer, 6)
    produce('fear', writer, 6)
    produce('sadness', writer, 6)
