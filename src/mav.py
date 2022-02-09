import numpy as np
import csv
import os
from pathlib import Path
from datetime import datetime


def movingAverages(csvString):
    
    listOfData = list(csv.DictReader(open(str(Path(__file__).resolve().parent) + "/../All Csv Data/" + csvString, mode='r')))

    mavList = []
    resultTen = None
    resultTwentyFive = None
    resultFifty = None
    resultOneHundred = None
    tenDayMav = 0
    twentyFiveDayMAV = 0
    fiftyDayMAV = 0
    oneHundredDayMAV = 0
    twoHundredDayMAV = 0

    for i in range(10):
        tenDayMav += float(listOfData[len(listOfData) - 10 + i]['close'])
    tenDayMav /= 10

    for i in range(25):
        twentyFiveDayMAV += float(listOfData[len(listOfData) - 25 + i]['close'])
    twentyFiveDayMAV /= 25

    for i in range(50):
        fiftyDayMAV += float(listOfData[len(listOfData) - 50 + i]['close'])
    fiftyDayMAV /= 50

    for i in range(100):
        oneHundredDayMAV += float(listOfData[len(listOfData) - 100 + i]['close'])
    oneHundredDayMAV /= 100

    for i in range(200):
        twoHundredDayMAV += float(listOfData[len(listOfData) - 200 + i]['close'])
    twoHundredDayMAV /= 200

    if tenDayMav > twoHundredDayMAV:
        resultTen = 'Buy'
    elif tenDayMav < twoHundredDayMAV:
        resultTen = 'Sell'

    if twentyFiveDayMAV > twoHundredDayMAV:
        resultTwentyFive = 'Buy'
    elif twentyFiveDayMAV < twoHundredDayMAV:
        resultTwentyFive = 'Sell'

    if fiftyDayMAV > twoHundredDayMAV:
        resultFifty = 'Buy'
    elif fiftyDayMAV < twoHundredDayMAV:
        resultFifty = 'Sell'

    if oneHundredDayMAV > twoHundredDayMAV:
        resultOneHundred = 'Buy'
    elif oneHundredDayMAV < twoHundredDayMAV:
        resultOneHundred = 'Sell'

    mavList.append(resultTen)
    mavList.append(resultTwentyFive)
    mavList.append(resultFifty)
    mavList.append(resultOneHundred)
    
    # print('10 Day MAV: ' + str(resultTen))
    # print('25 Day MAV: ' + str(resultTwentyFive))
    # print('50 Day MAV: ' + str(resultFifty))
    # print('100 Day MAV: ' + str(resultOneHundred))

    return mavList
