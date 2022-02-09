import csv
import os
from pathlib import Path


def specificDayOfMonth(csvString, day, month):
    dictionary = csv.DictReader(open(str(Path(__file__).resolve().parent) + "/../All Csv Data/" + csvString, mode='r'))
    listSpecificDayOfMonth = []
    rows = list(dictionary)
    count_Null = 0
    count_Total = 0
    count_Zero = 0
    count_Positive = 0
    count_Negative = 0
    trailingIndex = -1

    for row in rows:
        if int(row['datetime'][5:7]) == month and int(row['datetime'][8:10]) == day:
            count_Total = count_Total + 1
            if row['open'] != '' and trailingIndex != -1:
                difference = float(row['open']) - float(rows[trailingIndex]['close'])
                if difference == 0:
                    count_Zero = count_Zero + 1
                elif difference < 0:
                    count_Negative = count_Negative + 1
                else:
                    count_Positive = count_Positive + 1
            else:
                count_Null = count_Null + 1
        trailingIndex += 1

    listSpecificDayOfMonth.append(count_Total)
    listSpecificDayOfMonth.append(count_Positive)
    listSpecificDayOfMonth.append(count_Negative)
    listSpecificDayOfMonth.append(count_Zero)
    listSpecificDayOfMonth.append(count_Null)

    """print("Total Entries: " + str(count_Total))
    print(
        "Total Positive Closes: " + str(count_Positive) + " (%" + "{:.2f}".format(100 * count_Positive / count_Total) + ")")
    print(
        "Total Negative Closes: " + str(count_Negative) + " (%" + "{:.2f}".format(100 * count_Negative / count_Total) + ")")
    print("Total Same CLoses: " + str(count_Zero) + " (%" + "{:.2f}".format(100 * count_Zero / count_Total) + ")")
    print("Total Null Entries: " + str(count_Null))"""

    return listSpecificDayOfMonth
