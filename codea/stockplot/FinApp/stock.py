# class for stocks
#from stockplot.ystockquote import *
import ystockquote
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import Quandl
from django.conf import settings

class Stock(object):

    def __init__(self, symbol):
        self.symbol = symbol

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

    # get historical stock prices from Quandl
    def getStockHistoryQuandl(self, start, end):
        token = getattr(settings, "QUANDL_TOKEN", 'NO')
        print(token)

    # plot function for historical prices:
    def plotHistory(self, start, end):
        dates, data = self.getStockHistory(start, end)
        plotname = 'History'
        self.plotStock(dates, data, plotname)

    # actual plot function
    def plotStock(self, dates, data, plotname):
        plt.plot(dates, data, label = plotname)
        plt.ylabel(self.symbol + ' price ($)')
        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.legend(loc = 'lower right')
        #plt.show()
        plt.draw()

    # calculates "days"-moving average for stock from start to end
    def movingAverage(self, start, end, days):
        dates, data = self.getStockHistory(start, end)
        average = [0] * len(dates)
        if (days > len(dates)):
            print ("Error. Too many days!")
        else:
            for i in range(days,len(dates)-1):
                average[i] = sum(data[i-days:i])/days
        return dates, average

    # plot moving average
    def plotMovingAverage(self, start, end, days):
        dates, average = self.movingAverage(start, end, days)
        plotname = 'Moving Average ' + str(days) + ' days'
        self.plotStock(dates, average, plotname)

    # calculates "days"-exponential moving average for stock from star to end
    def ExpAverage(self, start, end, days):
        dates, data = self.getStockHistory(start, end)
        average = [0] * len(dates)
        if (days > len(dates)):
            print ("Error. Too many days!")
        else:
            # first average is regular average:
            average[days] = sum(data[0:days])/days
            alpha = 2.0/(1+days) # smoothing factor
            for i in range(days + 1, len(dates)-1):
                average[i] = data[i] * alpha + average[i-1] * (1-alpha)
        return dates, average

    # plot exponential moving average
    def plotExpAverage(self, start, end, days):
        dates, average = self.ExpAverage(start, end, days)
        plotname = 'Exponential Moving Average ' + str(days) + ' days'
        self.plotStock(dates, average, plotname)
