# test function for depot and stocks
import depot
from stockQuandl import StockQuandl
from stockYahoo import StockYahoo
import stockMath
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates

money = 1000
test = StockQuandl('FSE/AIR_X')

test.plotHistory('2005-01-01', '2016-02-23')
plt.hold(True)
test.plotMovingAverage('2005-01-01', '2016-02-23', 50)
test.plotExpAverage('2005-01-01', '2016-02-23', 15)
plt.show()
