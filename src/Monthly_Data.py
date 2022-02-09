import csv
import os
import numpy as np
from pathlib import Path


def monthlyData(csvString):
    valuesArray = np.zeros((12, 4))

    dictionary = csv.DictReader(open(str(Path(__file__).resolve().parent) + "/../All Csv Data/" + csvString, mode='r'))
    count_Null = 0
    count_Total = 0
    flag = True
    trailingClosePrice = None

    for row in dictionary:
        if row['open'] != '':
            if flag:
                trailingClosePrice = float(row['close'])
                flag = False
            else:
                valuesArray[int(row['datetime'][5:7]) - 1][0] = valuesArray[int(row['datetime'][5:7]) - 1][0] + 1
                closePrice = float(row['close'])
                difference = closePrice - trailingClosePrice
                if difference == 0:
                    valuesArray[int(row['datetime'][5:7]) - 1][3] = valuesArray[int(row['datetime'][5:7]) - 1][3] + 1
                elif difference < 0:
                    valuesArray[int(row['datetime'][5:7]) - 1][2] = valuesArray[int(row['datetime'][5:7]) - 1][2] + 1
                else:
                    valuesArray[int(row['datetime'][5:7]) - 1][1] = valuesArray[int(row['datetime'][5:7]) - 1][1] + 1
                trailingClosePrice = closePrice
        else:
            count_Null = count_Null + 1

    for i in range(12):
        count_Total = count_Total + valuesArray[i][0]
    count_Total = count_Total + count_Null

    """print("Total Closes Per Month, Positive Closes, Negative Closes, Same Closes")

    for i in range(12):
        print("Month " + str(i + 1) + ":", end='')
        for j in range(4):
            if j == 0:
                print(" " + str(valuesArray[i][j]), end='')
            else:
                print(" "
                      + str(valuesArray[i][j]) + " (%"
                      + "{:.2f}".format(100 * valuesArray[i][j] / valuesArray[i][0]) + ")", end='')
        print()
    print("Total Closes: " + str(count_Total) + ", Null Data Count: " + str(count_Null))"""

    return valuesArray
