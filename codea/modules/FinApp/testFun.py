# test function for depot and stocks
#import depot
from stockDatabase import StockDatabase
#from stockQuandl import StockQuandl
#from stockYahoo import StockYahoo
import stockMath
import matplotlib.pyplot as plt
import datetime
#import matplotlib.dates as mdates

#money = 1000
#teststock = StockQuandl('FSE/AIR_X')
teststock = StockDatabase('FAN.DOM')
today = datetime.datetime.now().strftime("%Y-%m-%d")

# getStockHistory with type, start, end
# datatype 'Open', 'Close', 'Low', 'High'
step = 1
dates, data = teststock.getStockHistoryFile('close', '2000-01-01', today, step)
print(len(data))
#teststock.plotHistory(dates, data)
#plt.hold(True)
#teststock.plotMovingAverage(dates, data, 50)
#teststock.plotExpAverage(dates, data, 15)
#plt.show()
