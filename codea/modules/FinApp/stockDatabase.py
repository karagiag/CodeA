# class for stock data from Database

# general imports
import os, sys, time, h5py
import datetime as datetime
import pandas as pd
import numpy as np

# own modules
from .stock import StockObj

# Django imports
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from django.core import serializers
from django.db import connection


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
from stockplot.models import Stock, StockData, StockDataFile

class StockDatabase(StockObj):
    # get current stock price
    def getStockPrice(self, datatype):
        stockDatabase = Stock.objects.get(sourceSymbol=self.symbol) # get stock from database
        stockid = stockDatabase.id
        dataquery = "SELECT date, %s FROM stockplot_stockdata WHERE stockid = %i LIMIT 1;" % (datatype, stockid)
        dates, data = self.access_database(dataquery)
        return dates[0], data[0]


    # get historical stock prices from Database
    def getStockHistoryAll(self, start, end):
        stockDatabase = Stock.objects.get(symbol=self.symbol) # get stock from database
        # get data from Database:
        data = stockDatabase.stockdata_set.all()
        return data # return close price for each day


    # get historical stock prices from Database
    def getStockHistory(self, datatype, start, end, step):
        stockDatabase = Stock.objects.get(sourceSymbol=self.symbol) # get stock from database
        stockid = stockDatabase.id
        # get data from Database:

        if (step == 1):
            dataquery = "SELECT date, %s FROM stockplot_stockdata WHERE stockid = %i;" % (datatype, stockid)
        else:
            dataquery = "SELECT date, %s FROM stockplot_stockdata WHERE stockid = %i AND MOD(id,%i) = 0;" % (datatype, stockid, step)
        dates, data = self.access_database(dataquery)

        # alternative:
        #dates = stockDatabase.stockdata_set.values_list('date', flat = True)
        #data = stockDatabase.stockdata_set.values_list(datatype, flat = True)
        # sort data with respect to dates:
        datasorted = [y for (x, y) in sorted(zip(dates, data))]
        datessorted = sorted(dates)

        # returns price at close of day
        return datessorted, datasorted


    def access_database(self, querytext):
        cursor = connection.cursor()
        cursor.execute(querytext)
        alldata = cursor.fetchall()
        dates = [item[0] for item in alldata]
        data = [item[1] for item in alldata]
        return dates, data

    # get historical stock prices from Database
    def getStockHistoryFile(self, datatype, start, end, step):
        stockDatabase = Stock.objects.get(sourceSymbol=self.symbol) # get stock from database
        # get data from Database:
        stockfiles = stockDatabase.stockdatafile_set.filter(stockid = stockDatabase.id)

        time1 = time.time()
        #### UPDATE #### append files to each other...
        for stock in stockfiles:
            # choose file here and open:
            h5f_url = settings.BASE_DIR + stock.stockdata.url
            h5f = h5py.File(h5f_url,'r')
            dates = np.ndarray.tolist(h5f['dates'][:])
            data = np.ndarray.tolist(h5f['data'][:])

        #data = stockDatabase.stockdata_set.values_list(datatype, flat = True)
        # sort data with respect to dates:
        datasorted = [y for (x, y) in sorted(zip(dates, data))]
        datessorted = sorted(dates)
        time2 = time.time()
        print(time2-time1)
        # returns price at close of day
        return datessorted, datasorted
