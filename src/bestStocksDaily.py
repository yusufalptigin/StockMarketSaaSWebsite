import datetime
import statistics as stat
from operator import itemgetter
import csv
import os
from pathlib import Path
from Days_Each_Month_O import daysEachMonth as daysEachMonthO  # For each day in each month: Total, Pos, Neg, Same / Day to day list[12, 5, 4]
from Specific_Day_Of_Month_O import \
    specificDayOfMonth as specificDayOfMonthO  # For a specific date: Total, Pos, Neg, Same, Null / Intra day list[5]
from Days_Each_Month_DD import daysEachMonth as daysEachMonthI
from Specific_Day_Of_Month_DD import specificDayOfMonth as specificDayOfMonthI


def bestStocksCalculator(listOfBestStocks):
    temporaryList = []
    listToReturn = []

    stdOfList = stat.stdev([pair[0] for pair in listOfBestStocks])
    medianOfList = stat.median([pair[0] for pair in listOfBestStocks])
    plusSD = medianOfList + stdOfList

    for i in range(len(listOfBestStocks)):
        stockNegPercentage = listOfBestStocks[i][0]
        if stockNegPercentage <= medianOfList:
            temporaryList.append(listOfBestStocks[i])

    sortedTemporaryList = sorted(temporaryList, key=itemgetter(0))

    for i in range(len(sortedTemporaryList)):
        listToReturn.append([sortedTemporaryList[i][1], (medianOfList - sortedTemporaryList[i][0]) / medianOfList])
    return listToReturn


def bestStocksDaily(stocksList):
    sumPercentages = 0
    sumCount = 0
    dayStart = datetime.datetime.today()
    totalPositives = 0
    totalNegatives = 0
    totalSame = 0
    rangeLst = []
    for i in range(1):
        tempDayStart = dayStart
        if tempDayStart.weekday() == 6:
            tempDayStart = tempDayStart - datetime.timedelta(days=2)
        dayStart = dayStart + datetime.timedelta(days=1)
        tomorrowDay = dayStart.day
        tomorrowMonth = dayStart.month
        tomorrowWeekday = dayStart.weekday()

        if tomorrowWeekday == 5 or tomorrowWeekday == 6:
            continue

        weekdayOfMonthOpen = []
        weekdayOfMonthIntraDay = []
        specificDayOfMonthOpen = []
        specificDayOfMonthIntraDay = []

        try:
            for stock in stocksList:
                csvString = stock + '.csv'

                listDaysEachMonthOpen = daysEachMonthO(csvString)
                weekdayOfMonthOpen.append(
                    [listDaysEachMonthOpen[tomorrowMonth - 1, tomorrowWeekday, 2] / listDaysEachMonthOpen[tomorrowMonth - 1, tomorrowWeekday, 0], stock])

                listDaysEachMonthIntraDay = daysEachMonthI(csvString)
                weekdayOfMonthIntraDay.append(
                    [listDaysEachMonthIntraDay[tomorrowMonth - 1, tomorrowWeekday, 2] / listDaysEachMonthIntraDay[tomorrowMonth - 1, tomorrowWeekday, 0],
                     stock])

                listSpecificDayOfMonthOpen = specificDayOfMonthO(csvString, month=tomorrowMonth, day=tomorrowDay)
                specificDayOfMonthOpen.append([listSpecificDayOfMonthOpen[2] / listSpecificDayOfMonthOpen[0], stock])

                listSpecificDayOfMonthIntraDay = specificDayOfMonthI(csvString, month=tomorrowMonth, day=tomorrowDay)
                specificDayOfMonthIntraDay.append([listSpecificDayOfMonthIntraDay[2] / listSpecificDayOfMonthIntraDay[0], stock])
        except ZeroDivisionError:
            continue

        weekdayOfMonthListOpen = bestStocksCalculator(weekdayOfMonthOpen)
        weekdayOfMonthListIntraDay = bestStocksCalculator(weekdayOfMonthIntraDay)
        specificDayOfMonthListOpen = bestStocksCalculator(specificDayOfMonthOpen)
        specificDayOfMonthListIntraDay = bestStocksCalculator(specificDayOfMonthIntraDay)

        lst = [{pair[0] for pair in weekdayOfMonthListOpen}, {pair[0] for pair in weekdayOfMonthListIntraDay},
               {pair[0] for pair in specificDayOfMonthListOpen}, {pair[0] for pair in specificDayOfMonthListIntraDay}]
        lstTemp = list(lst[0].intersection(*lst))

        rangeLst.append(lstTemp)
    return rangeLst
