# class for stock data from yahoo

# general imports
import ystockquote
import datetime as dt
import pandas as pd

# own modules
from .stock import StockObj



############################  UPDATE  ##########################################
### YAHOO YSTOCKQUOTE NOT WORKING---###
class StockYahoo(StockObj):

    # get current stock price
    def getStockPrice(self):
        price = ystockquote.get_price(self.symbol)
        return float(price)

    # get historical stock prices from yahoo.
    # Date format for start and end: "YYYY-MM-DD"
    def getStockHistoryClose(self, start, end):
        history = ystockquote.get_historical_prices(self.symbol, start, end)
        dates = []
        data = []
        for i in sorted(history):
            dates.append(dt.datetime.strptime(i, '%Y-%m-%d').date())
            data.append(float(history[i]['Close']))
            # returns price at close of day
        return dates, data


    # get historical stock prices from yahoo.
    # Date format for start and end: "YYYY-MM-DD"
    def getStockHistoryAll(self, start, end):
        history = ystockquote.get_historical_prices(self.symbol, start, end)
        return history
###########################FIXFIXFIX############################################
