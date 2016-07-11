# Python script for filling database from csv file
import datetime, sys, os, Quandl

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

# last n-days of stockdata:
n = 100;

# Get available stocks from database:
stocks = Stock.objects.filter(source = 'Quandl')
for stock in stocks:
    print(stock.name)
    stockid = stock.id
    print(stockid)
    history = Quandl.get(stock.sourceSymbol, rows = n, authtoken= token)
    for index, row in history.iterrows():
        data = stock.stockdata_set.update_or_create(
            stock = stock,
            stockid = stockid,
            date = index.timestamp(),
            defaults = {'open_price' : float(row['Open']),
                'high' : float(row['High']),
                'low' : float(row['Low']),
                'close' : float(row['Close']),
                'change' : float(row['Change']),
                'traded_volume' : float(row['Traded Volume']),
                'turnover' : float(row['Turnover']),
                'last_price_of_the_day' : float(row['Last Price of the Day']),
                'daily_traded_units' : float(row['Daily Traded Units']),
                'daily_turnover' : float(row['Daily Turnover']),
            }
        )
