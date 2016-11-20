# Python script for filling database from csv file

import datetime, sys, os, quandl

# Full path to django project directory
djangoproject_home="/home/oliver/Repositories/CodeA/codea/"
# Full path to python FinApp directory

sys.path.append(djangoproject_home)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codea.settings")

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
from django.utils import timezone
from django.conf import settings
stockplot = get_wsgi_application()
from stockplot.models import Stock, StockData
from modules.FinApp.stockQuandl import StockQuandl
today = datetime.datetime.now().strftime("%Y-%m-%d")

# get Quandl token from settings
token = getattr(settings, "QUANDL_TOKEN", 'NO')
print(token)

# Get available stocks from database:
stocks = Stock.objects.filter(source = 'Quandl')

def convertfloat(data):
    if data is None:
        return None
    return float(data)

for stock in stocks:
    print(stock.name)
    stockid = stock.id
    print(stockid)
    history = quandl.get(stock.sourceSymbol, trim_start='1900-01-01', trim_end=today, authtoken= token)
    stockdata = [
        StockData(
            stock = stock,
            stockid = stockid,
            date = index.timestamp(),
            open_price = convertfloat(row['Open']),
            high = convertfloat(row['High']),
            low = convertfloat(row['Low']),
            close = convertfloat(row['Close']),
            change = convertfloat(row['Change']),
            traded_volume = convertfloat(row['Traded Volume']),
            turnover = convertfloat(row['Turnover']),
            last_price_of_the_day = convertfloat(row['Last Price of the Day']),
            daily_traded_units = convertfloat(row['Daily Traded Units']),
            daily_turnover = convertfloat(row['Daily Turnover']),
        ) for index, row in history.iterrows()
    ]
    print('Objects done')
    try:
        StockData.objects.bulk_create(stockdata)
    except:
        print('Already there')
    print('Done')

############ UPDATE ##### way too slow #########################################
