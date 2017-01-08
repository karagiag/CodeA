# Python script for filling database from csv file

import datetime, sys, os

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
from stockplot.models import Stock, StockFundamentals
from modules.FinApp.stockDatabase import StockDatabase
from modules.FinApp.Analyze_ValueDB import fundamentals
startdate = datetime.datetime.strptime('2000-01-01', "%Y-%m-%d")
today = datetime.datetime.now()
day_count = (today - startdate).days + 1

# Get available stocks from database:
stocks = Stock.objects.all()
StockFundamentals.objects.all().delete()

for stock in stocks:
    print(stock.name)
    teststock = StockDatabase(stock.sourceSymbol)
    stockid = stock.id
    print(stockid)
    compNumber = stock.fundamentalsCompNumber
    i = 0
    for date in (startdate + datetime.timedelta(n) for n in range(day_count)):
        date = date.timestamp()
        price = teststock.getStockPriceDate('close', date)[1]
        datestr = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d')
        i = i + 1
        if i%100 == 0:
            print(datestr)
        shares, capitalization, PCF, PSR, PB, EPSD, quick, current = fundamentals(compNumber, datestr, price)
        stockfundamentals = StockFundamentals()
        stockfundamentals.stock = stock
        stockfundamentals.stockid = stockid
        stockfundamentals.date = date
        stockfundamentals.shares = shares
        stockfundamentals.capitalization = capitalization
        stockfundamentals.PCF = PCF
        stockfundamentals.PSR = PSR
        stockfundamentals.PB = PB
        stockfundamentals.EPSD = EPSD
        stockfundamentals.quick = quick
        stockfundamentals.current = current
        stockfundamentals.save()
    print('Stock done')
print('Done')
