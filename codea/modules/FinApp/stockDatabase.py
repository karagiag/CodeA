# class for stock data from Database

# general imports
import os, sys, time, h5py
import datetime as datetime
import pandas as pd
import numpy as np

# own modules
try:
    from .stock import StockObj
except Exception: #ImportError
    from stock import StockObj

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
    # get last available stock price
    def getStockPrice(self, datatype):
        stockDatabase = Stock.objects.get(sourceSymbol=self.symbol) # get stock from database
        stockid = stockDatabase.id
        dataquery = "SELECT date, %s FROM stockplot_stockdata WHERE stockid = %i ORDER BY date DESC LIMIT 1;" % (datatype, stockid)
        #dataquery = "SELECT date, %s FROM stockplot_stockdata WHERE stockid = %i AND date = %f LIMIT 1;" % (datatype, stockid, date)
        dates, data = self.access_database(dataquery)
        return dates[0], data[0]


    # get stock price for specific date
    def getStockPriceDate(self, datatype, date):
        stockDatabase = Stock.objects.get(sourceSymbol=self.symbol) # get stock from database
        stockid = stockDatabase.id
        dataquery = "SELECT date, %s FROM stockplot_stockdata WHERE stockid = %i AND date = %f LIMIT 1;" % (datatype, stockid, date)
        dates, data = self.access_database(dataquery)
        if len(dates) == 0:
            return 0, 0
        else:
            return dates[0], data[0]


    # get historical stock prices from Database
    def getStockHistoryAll(self, start, end):
        stockDatabase = Stock.objects.get(symbol=self.symbol) # get stock from database
        # get data from Database:
        data = stockDatabase.stockdata_set.all()
        return data # return close price for each day


    # get historical stock prices from Database
    def getStockHistory(self, datatype, start, end, step):
        # start and end not implemented yet !!!

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


    # get historical stock prices from Database
    def getStockHistoryDate(self, datatype, start, end, step):
        # start and end not implemented yet !!!

        stockDatabase = Stock.objects.get(sourceSymbol=self.symbol) # get stock from database
        stockid = stockDatabase.id
        # get data from Database:

        if (step == 1):
            dataquery = "SELECT date, %s FROM stockplot_stockdata WHERE stockid = %i AND date > %f AND date < %f;" % (datatype, stockid, start, end)
        else:
            dataquery = "SELECT date, %s FROM stockplot_stockdata WHERE stockid = %i AND date > %f AND date < %f AND MOD(id,%i) = 0;" % (datatype, stockid, start, end, step)
        dates, data = self.access_database(dataquery)

        # alternative:
        #dates = stockDatabase.stockdata_set.values_list('date', flat = True)
        #data = stockDatabase.stockdata_set.values_list(datatype, flat = True)
        # sort data with respect to dates:
        datasorted = [y for (x, y) in sorted(zip(dates, data))]
        datessorted = sorted(dates)

        # returns price at close of day
        return datessorted, datasorted

    # executes query in database:
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

    # calculates Money Flow Index
    def MFI(self, start, end):
        # calculate typical price for each day
        high = self.getStockHistoryDate('high', start, end, 1)[1] #[1] for data, [0] would be dates
        low = self.getStockHistoryDate('low', start, end, 1)[1]
        close = self.getStockHistoryDate('close', start, end, 1)[1]

        # typical is average of high, low and close. Unless low or high are not
        # available. Then just take the close price
        typical = [(x + y + z) / 3 if y == y and z == z else z for (x, y, z) in zip(high, low, close)]
        # get traded volume for each day
        volume = self.getStockHistoryDate('traded_volume', start, end, 1)[1]

        # replace nan's by mean volume
        meanVolume = np.nanmean(volume)
        for i in range(0, len(volume)):
            if volume[i] != volume[i]:
                volume[i] = meanVolume

        # calculate positive and negative money flow
        pos_MF = [0]
        neg_MF = [0]
        for i in range(1, len(typical)):
            if typical[i] >= typical[i-1]:
                pos_MF.append(typical[i] * volume[i])
                neg_MF.append(0)
            else:
                pos_MF.append(0)
                neg_MF.append(typical[i] * volume[i])

        # calculate 14 day Money Flow Ratio
        MFR14 = [0]*len(typical)
        pos_MF14 = [0]*len(typical)
        neg_MF14 = [0]*len(typical)
        if (14 > len(typical)):
            print ("Error. Too many days!")
        else:
            for i in range(14, len(typical)):
                pos_MF14[i] = sum(pos_MF[i-14:i])
                neg_MF14[i] = sum(neg_MF[i-14:i])
                if neg_MF14[i] > 0:
                    MFR14[i] = pos_MF14[i]/neg_MF14[i]
                else:
                    MFR14[i] = pos_MF14[i]/1

        # caluclate Money Flow Index:
        MFI = [100-(100/(1+MFR)) for MFR in MFR14]

        return typical, volume, pos_MF, neg_MF, pos_MF14, neg_MF14, MFR14, MFI
