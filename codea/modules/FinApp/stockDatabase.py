# class for stock data from Database

# general imports
import Quandl, os, sys
import datetime as datetime
import pandas as pd

# own modules
from .stock import StockObj

# Django imports
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from django.core import serializers


##################################### Settings import ##########################
# Full path to django project directory
# MAKE THIS RELATIVE!!! ###############  UPDATE  ##############################
djangoproject_home="/home/oliver/Repositories/CodeA/codea/"
sys.path.append(djangoproject_home)
# get settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codea.settings")
stockplot = get_wsgi_application() # load application
################################################################################


# import stock model from database
from stockplot.models import Stock

class StockDatabase(StockObj):
    # get current stock price
    def getStockPrice(self):
        pass

    # get historical stock prices from Database
    def getStockHistoryAll(self, start, end):
        stockDatabase = Stock.objects.get(symbol=self.symbol) # get stock from database
        # get data from Database:
        data = stockDatabase.stockdata_set.all()
        return data # return close price for each day


    # get historical stock prices from Database
    def getStockHistory(self, datatype, start, end):
        stockDatabase = Stock.objects.get(symbol=self.symbol) # get stock from database
        # get data from Database:
        dates = list(stockDatabase.stockdata_set.values_list('date', flat=True))
        data = list(stockDatabase.stockdata_set.values_list(datatype, flat=True))

        ############# UPDATE ############ Imporve database query + sorting #####
        # sort data with respect to dates:
        datasorted = [y for (x, y) in sorted(zip(dates, data))]
        datessorted = sorted(dates)

            # returns price at close of day
        return datessorted, datasorted
