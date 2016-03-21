# class for stock data from Quandl
from .stock import Stock
import Quandl
import datetime as datetime
import pandas as pd
from django.conf import settings

class StockQuandl(Stock):

    # get current stock price
    def getStockPrice(self):
        pass

    # get historical stock prices from Quandl
    def getStockHistory(self, start, end):
        token = getattr(settings, "QUANDL_TOKEN", 'NO')
        data = Quandl.get(self.symbol, trim_start=start, trim_end=end, authtoken= token)
        return data['Close'] # return close price for each day 
