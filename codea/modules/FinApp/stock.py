# class for stocks

#general imports
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime as datetime

# base class for a stock object
class StockObj(object):

    def __init__(self, symbol):
        self.symbol = symbol

    # get current stock price
    def getStockPrice(self):
        pass

    # get historical stock prices with all info.
    def getStockHistoryAll(self, start, end):
        pass

    # get historical stock prices only with type info, e.g. 'Open', 'Close'
    def getStockHistory(self, datatype, start, end, step):
        pass

    # plot function for historical prices:
    def plotHistory(self, dates, data):
        plotname = 'History'
        self.plotStock(dates, data, plotname)

    # actual plot function
    def plotStock(self, datestamps, data, plotname):
        dates = [datetime.datetime.fromtimestamp(date) for date in datestamps]
        plt.plot(dates, data, label = plotname)
        plt.ylabel(self.symbol + ' price ($)')
        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.legend(loc = 'lower right')
        plt.draw()

    # calculates "days"-moving average for stock from start to end
    def movingAverage(self, dates, data, days):
        average = [float('NaN')] * len(data)
        if (days > len(data)):
            print ("Error. Too many days!")
        else:
            for i in range(days,len(data)):
                average[i] = sum(data[i-days:i])/days
        return average

    # plot moving average
    def plotMovingAverage(self, dates, data, days):
        average = self.movingAverage(dates, data, days)
        plotname = 'Moving Average ' + str(days) + ' days'
        self.plotStock(dates, average, plotname)

    # calculates "days"-exponential moving average for stock from start to end
    def ExpAverage(self, dates, data, days):
        average = [float('NaN')] * len(data)
        if (days > len(data)):
            print ("Error. Too many days!")
        else:
            # first average is regular average:
            average[days] = sum(data[0:days])/days
            alpha = 2.0/(1+days) # smoothing factor
            for i in range(days + 1, len(data)):
                average[i] = data[i] * alpha + average[i-1] * (1-alpha)
        return average

    # plot exponential moving average
    def plotExpAverage(self, dates, data, days):
        average = self.ExpAverage(dates, data, days)
        plotname = 'Exponential Moving Average ' + str(days) + ' days'
        self.plotStock(dates, average, plotname)


    # calculates MACD: Moving Average Convergence Divergence
    def MACD(self, dates, data):
        ema26 = self.ExpAverage(dates, data, 26)
        ema12 = self.ExpAverage(dates, data, 12)
        MACD = [x-y for (x, y) in zip(ema12, ema26)]
        return MACD

    # calculates PPO: Percentage Price Oscillator
    def PPO(self, dates, data):
        ema26 = self.ExpAverage(dates, data, 26)
        ema9 = self.ExpAverage(dates, data, 12)
        PPO = [(x-y)*100/y if y != 0 else 0 for (x, y) in zip(ema9, ema26)]
        return PPO

    # calculates Bollinger Band
    def Bollinger(self, dates, data, days, factor):
        average = np.array(self.movingAverage(dates, data, days)) # get days moving average
        low = [float('NaN')] * len(data)
        high = [float('NaN')] * len(data)
        for i in range(days, len(data)):
            standardDev = np.std(data[i-days:i]) # get days standard deviation
            low[i] = average[i] - factor * standardDev
            high[i] = average[i] + factor * standardDev
        return list(low), list(average), list(high)
