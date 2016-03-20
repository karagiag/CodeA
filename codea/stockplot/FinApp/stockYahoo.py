# class for stocks
#from stockplot.ystockquote import *
import ystockquote
from stock import Stock
import datetime as dt
import pandas as pd

class StockYahoo(Stock):

    # get current stock price
    def getStockPrice(self):
        price = ystockquote.get_price(self.symbol)
        return float(price)

    # get historical stock prices from yahoo. Date format for start and end: "YYYY-MM-DD"
    def getStockHistory(self, start, end):
        history = ystockquote.get_historical_prices(self.symbol, start, end)
        dates = []
        data = []
        for i in sorted(history):
            dates.append(dt.datetime.strptime(i, '%Y-%m-%d').date())
            #dates.append(i)
            data.append(float(history[i]['Close'])) # returns price at close of day
        return dates, data
