# class for stock data from Quandl

# general imports
import quandl, sys, os
import datetime as datetime
import pandas as pd

# own modules
from .stock import StockObj

# django modules
from django.conf import settings
from django.core.wsgi import get_wsgi_application

##################################### Settings import ##########################
# Full path to django project directory
# MAKE THIS RELATIVE!!! ###############  UPDATE  ###############################
djangoproject_home="/home/oliver/Repositories/CodeA/codea/"
sys.path.append(djangoproject_home)
# get settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codea.settings")
stockplot = get_wsgi_application() # load application
################################################################################



# class for a stock from Quandl
class StockQuandl(StockObj):

    # get current stock price
    def getStockPrice(self):
        pass

    # get historical stock prices from Quandl
    def getStockHistoryAll(self, start, end):
        token = getattr(settings, "QUANDL_TOKEN", 'NO')
        data = quandl.get(self.symbol, trim_start=start, trim_end=end, authtoken= token)
        return data

    # get historical stock prices from Quandl for type.
    # type can be 'Open', 'High', 'Low', 'Close'
    def getStockHistory(self, datatype, start, end, step):
        token = getattr(settings, "QUANDL_TOKEN", 'NO')
        data = quandl.get(self.symbol, trim_start=start, trim_end=end, authtoken= token)
        # convert to date and 'type' list
        dates = [index.timestamp() for index, row in data.iterrows()]
        # convert dates to python datetime from numpy.datetime64 in LIST COMPREHENSION:!!!
        #dates = [datetime.datetime.utcfromtimestamp(date.astype('O')/1e9) for date in dates]
        # convert data to list:
        data = data[datatype].tolist()
        return dates, data # return close price for each day
