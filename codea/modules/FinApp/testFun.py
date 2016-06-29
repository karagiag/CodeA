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
teststock = StockDatabase('FSE/AIR_X')
today = datetime.datetime.now().strftime("%Y-%m-%d")

# getStockHistory with type, start, end
# datatype 'Open', 'Close', 'Low', 'High'
step = 1
dates, data = teststock.getStockHistory('close', '2000-01-01', today, step)
teststock.plotHistory(dates, data)
plt.hold(True)
datesMACD, dataMACD = teststock.MACD('close', '2001-01-01', today)
teststock.plotHistory(datesMACD, dataMACD)
datesPPO, dataPPO = teststock.PPO('close', '2000-01-01', today)
#dataPPO = [10*x for x in dataPPO]
teststock.plotHistory(datesPPO, dataPPO)
#teststock.plotMovingAverage(dates, data, 50)
#teststock.plotExpAverage(dates, data, 15)
plt.show()
