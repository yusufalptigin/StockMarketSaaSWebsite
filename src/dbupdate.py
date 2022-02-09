import os
import sys
import csv

import psycopg2 as dbapi2

XU30 = ['AKBNK', 'ARCLK', 'ASELS', 'BIMAS', 'DOHOL', 'EKGYO', 'EREGL', 'FROTO', 'GARAN', 'GUBRF',
        'HALKB', 'ISCTR', 'KCHOL', 'KOZAA', 'KOZAL', 'KRDMD', 'PETKM', 'PGSUS', 'SAHOL', 'SASA',
        'SISE', 'TAVHL', 'TCELL', 'THYAO', 'TKFEN', 'TOASO', 'TTKOM', 'TUPRS', 'VESTL', 'YKBNK']
xu30_data = list()

cryptos = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT', 'XRPUSDT', 'LUNAUSDT', 'DOTUSDT', 'AVAXUSDT', 'DOGEUSDT',
           'SHIBUSDT', 'MATICUSDT', 'EOSUSDT', 'LINKUSDT', 'UNIUSDT', 'ALGOUSDT', 'LTCUSDT', 'NEARUSDT', 'ATOMUSDT', 'TRXUSDT',
           'FTMUSDT', 'XLMUSDT', 'ICPUSDT', 'VETUSDT', 'FTTUSDT', 'MANAUSDT', 'HBARUSDT', 'FILUSDT', 'AXSUSDT', 'SANDUSDT']
crypto_data = list()

nasdaq = ['AAPL', 'MSFT', 'AMZN', 'FB', 'TSLA', 'NVDA', 'GOOG', 'GOOGL', 'AVGO', 'ADBE',
          'NFLX', 'CSCO', 'COST', 'PEP', 'CMCSA', 'PYPL', 'INTC', 'QCOM', 'TXN', 'INTU',
          'AMD', 'HON', 'AMAT', 'TMUS', 'SBUX', 'AMGN', 'ISRG', 'CHTR', 'MU', 'ADP']
nasdaq_data = list()

pairs = ['EURUSD', 'USDJPY', 'GBPUSD', 'AUDUSD', 'USDCAD', 'USDCHF', 'GBPAUD',
         'EURGBP', 'GBPJPY', 'GBPZAR', 'USDZAR', 'EURAUD', 'EURCAD']
pairs_data = list()


for stock in XU30:
    line1, line2 = list(csv.DictReader(open(f"All Csv Data/{stock}.csv", 'r')))[-2:]
    xu30_data.append((stock, 'XU30', float(line2['close']), (float(line2['close']) - float(line1['close'])) / float(line1['close'])))
for stock in pairs:
    line1, line2 = list(csv.DictReader(open(f"All Csv Data/{stock}.csv", 'r')))[-2:]
    pairs_data.append((stock, 'CURRENCY', float(line2['close']), (float(line2['close']) - float(line1['close'])) / float(line1['close'])))
for stock in nasdaq:
    line1, line2 = list(csv.DictReader(open(f"All Csv Data/{stock}.csv", 'r')))[-2:]
    nasdaq_data.append((stock, 'NASDAQ', float(line2['close']), (float(line2['close']) - float(line1['close'])) / float(line1['close'])))
for stock in cryptos:
    line1, line2 = list(csv.DictReader(open(f"All Csv Data/{stock}.csv", 'r')))[-2:]
    crypto_data.append((stock, 'CRYPTO', float(line2['close']), (float(line2['close']) - float(line1['close'])) / float(line1['close'])))


def initialize(url):
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            print(xu30_data[0])
            args_str = ','.join(cursor.mogrify("(%s,%s,%s,%s)", x).decode('utf-8') for x in xu30_data)
            cursor.execute("INSERT INTO stock (stockcode, stockname, currprice, change) VALUES " + args_str)         
            print(args_str)
            args_str = ','.join(cursor.mogrify("(%s,%s,%s,%s)", x).decode('utf-8') for x in nasdaq_data)
            cursor.execute("INSERT INTO stock (stockcode, stockname, currprice, change) VALUES " + args_str)
            args_str = ','.join(cursor.mogrify("(%s,%s,%s,%s)", x).decode('utf-8') for x in crypto_data)
            cursor.execute("INSERT INTO stock (stockcode, stockname, currprice, change) VALUES " + args_str)
            args_str = ','.join(cursor.mogrify("(%s,%s,%s,%s)", x).decode('utf-8') for x in pairs_data)
            cursor.execute("INSERT INTO stock (stockcode, stockname, currprice, change) VALUES " + args_str)
            connection.commit()
            cursor.close()
    except Exception as err:
        print("Error: ", err)


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
