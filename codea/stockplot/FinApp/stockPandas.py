# base class for stocks
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# Stock class implements base class for stocks. Sub-classes depend on
# different data sources. All data sources deliver pandas dataframes.
class Stock(object):

    def __init__(self, symbol):
        self.symbol = symbol

    # get current stock price
    def getStockPrice(self):
        pass

    # get historical stock prices from yahoo. Date format for start and end: "YYYY-MM-DD"
    def getStockHistory(self, start, end):
        pass # depends on data source

    # plot function for historical prices:
    def plotHistory(self, start, end):
        data = self.getStockHistory(start, end)
        plotname = 'History'
        self.plotStock(data, plotname)

    # actual plot function
    def plotStock(self, data, plotname):
        plt.plot(data, label = plotname)
        plt.ylabel(self.symbol + ' price ($)')
        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.legend(loc = 'lower right')
        plt.draw()

    # calculates "days"-moving average for stock from start to end
    def movingAverage(self, start, end, days):
        data = self.getStockHistory(start, end)
        average = pd.DataFrame(data, index=data.index.copy())
        if (days > len(data)):
            print ("Error. Too many days!")
        else:
            for i in range(days,len(data)-1):
                average.ix[i] = sum(data.ix[i-days:i])/days
        return average

    # plot moving average
    def plotMovingAverage(self, start, end, days):
        average = self.movingAverage(start, end, days)
        plotname = 'Moving Average ' + str(days) + ' days'
        self.plotStock(average, plotname)

    # calculates "days"-exponential moving average for stock from star to end
    def ExpAverage(self, start, end, days):
        data = self.getStockHistory(start, end)
        average = pd.DataFrame(data, index=data.index.copy())
        if (days > len(data)):
            print ("Error. Too many days!")
        else:
            # first average is regular average:
            average.ix[days] = sum(data.ix[0:days])/days
            alpha = 2.0/(1+days) # smoothing factor
            for i in range(days + 1, len(data)-1):
                average.ix[i] = data.ix[i] * alpha + average.ix[i-1] * (1-alpha)
        return average

    # plot exponential moving average
    def plotExpAverage(self, start, end, days):
        average = self.ExpAverage(start, end, days)
        plotname = 'Exponential Moving Average ' + str(days) + ' days'
        self.plotStock(average, plotname)
