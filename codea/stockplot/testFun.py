# test function for depot and stocks
import depot
import stock
import stockMath
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates

money = 1000
test = stock.Stock('PAH3.DE')
boughtTesla = stock.BoughtStock('TSLA', 10)

print boughtTesla

test.plotHistory('2005-01-01', '2016-02-23')
plt.hold(True)
test.plotExpAverage('2005-01-01', '2016-02-23', 50)
test.plotExpAverage('2005-01-01', '2016-02-23', 15)
plt.show()
