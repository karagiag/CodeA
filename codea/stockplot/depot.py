# class for stock depot - simulator
import stock
import ystockquote

class Depot(object):
    
    def __init__(self, total, stocks, maxStocks):
        self.total = total # available money in depot
        self.stocks = stocks # stocks already in depot
        self.maxStocks = maxStocks # max stocks to be held at one time

    # method for buying stock
    def buyStock(self, stock):
        pass

    # method for selling stock
    def sellStock(self, stock):
        pass

    # method for calculating worth of depot:
    def depotWorth(self):
	tot = 0
	for i in self.stocks:
	    price = i.getStockPrice()
	    tot += price * i.amount
	return tot
