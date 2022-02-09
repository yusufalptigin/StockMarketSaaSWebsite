import csv
import os
import numpy as np
from pathlib import Path
from datetime import datetime


def daysEachMonth(csvString):
    dictionary = csv.DictReader(open(str(Path(__file__).resolve().parent) + "/../All Csv Data/" + csvString, mode='r'))
    count_Null = 0
    count_Total = 0
    flag = True
    trailingClosePrice = None

    dayOfMonthArray = np.zeros((12, 5, 4))

    for row in dictionary:
        day = datetime(int(row['datetime'][0:4]), int(row['datetime'][5:7]), int(row['datetime'][8:10])).weekday()
        count_Total = count_Total + 1
        if row['open'] != '':
            if flag:
                trailingClosePrice = float(row['close'])
                flag = False
            else:
                dayOfMonthArray[int(row['datetime'][5:7]) - 1][day][0] \
                    = dayOfMonthArray[int(row['datetime'][5:7]) - 1][day][0] + 1
                closePrice = float(row['close'])
                difference = closePrice - trailingClosePrice
                if difference == 0:
                    dayOfMonthArray[int(row['datetime'][5:7]) - 1][day][3] \
                        = dayOfMonthArray[int(row['datetime'][5:7]) - 1][day][3] + 1
                elif difference < 0:
                    dayOfMonthArray[int(row['datetime'][5:7]) - 1][day][2] \
                        = dayOfMonthArray[int(row['datetime'][5:7]) - 1][day][2] + 1
                else:
                    dayOfMonthArray[int(row['datetime'][5:7]) - 1][day][1] \
                        = dayOfMonthArray[int(row['datetime'][5:7]) - 1][day][1] + 1
                trailingClosePrice = closePrice
        else:
            count_Null = count_Null + 1

    """for i in range(12):
        print("Month " + str(i + 1) + ", ", end='')
        for j in range(5):
            print("Day " + str(j + 1) + ":", end='')
            for k in range(4):
                if k == 0:
                    print(" " + str(dayOfMonthArray[i][j][k]), end='')
                else:
                    print(" " + str(dayOfMonthArray[i][j][k])
                          + " (%" + "{:.2f}".format(100 * dayOfMonthArray[i][j][k] / dayOfMonthArray[i][j][0])
                          + ")", end='')
            print()
        print()
    print("Total Closes: " + str(count_Total) + ", Null Data Count: " + str(count_Null))"""

    return dayOfMonthArray
