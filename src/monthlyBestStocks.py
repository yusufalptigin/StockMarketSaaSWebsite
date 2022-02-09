import statistics as stat
from operator import itemgetter
from Monthly_Data import monthlyData as monthlyDataD


def monthlyBestPerformingStocks(stocksList, month):
    monthlyDataDPercentNegative = []
    foundStocksListBest = []
    foundStocksListAverage = []
    foundStocksWorst = []

    for stock in stocksList:
        csvString = stock + '.csv'
        monthlyDataDList = monthlyDataD(csvString)
        monthlyDataDPercentNegative.append([monthlyDataDList[month - 1][2] / monthlyDataDList[month - 1][0], stock])

    stdOfList = stat.stdev([pair[0] for pair in monthlyDataDPercentNegative])
    medianOfList = stat.median([pair[0] for pair in monthlyDataDPercentNegative])
    minusSD = medianOfList - stdOfList

    for i in range(len(monthlyDataDPercentNegative)):
        stockNegPercentage = monthlyDataDPercentNegative[i][0]
        if stockNegPercentage <= minusSD:
            foundStocksListBest.append(monthlyDataDPercentNegative[i])
        elif minusSD < stockNegPercentage <= medianOfList:
            foundStocksListAverage.append(monthlyDataDPercentNegative[i])
        else:
            foundStocksWorst.append(monthlyDataDPercentNegative[i])

    sortedBest = sorted(foundStocksListBest, key=itemgetter(0))
    sortedAverage = sorted(foundStocksListAverage, key=itemgetter(0))
    sortedWorst = sorted(foundStocksWorst, key=itemgetter(0))

    resultBest = [(medianOfList - item[0], item[1]) for item in sortedBest]
    resultAverage = [(medianOfList - item[0], item[1]) for item in sortedAverage]
    resultWorst = [(medianOfList - item[0], item[1]) for item in sortedWorst]
    return resultBest, resultAverage, resultWorst