# class for stock data from Database

# general imports
import os, sys, time, h5py
import datetime as datetime
import pandas as pd
import numpy as np

# own modules
from .stockDatabase import StockDatabase

# Django imports
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from django.core import serializers
from django.db import connection


##################################### Settings import ##########################
# Full path to django project directory
# MAKE THIS RELATIVE!!! ###############  UPDATE  ##############################
djangoproject_home="/home/oliver/Repositories/CodeA/codea/"
sys.path.append(djangoproject_home)
# get settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codea.settings")
stockplot = get_wsgi_application() # load application
################################################################################


# import stock model from database
from stockplot.models import Stock, Depot, DepotContent


################################################################################
# analyses contents of depot and calculates money stuff...
def depotAnalysis(depot):
    depotcontent = list(depot.depotcontent_set.all())
    spent = 0 # money spent on stocks
    total = 0 # total value of stocks
    for element in depotcontent:
        stockid = element.stock.id
        element.bought_total = round(element.amount * element.bought_at, 2)
        spent += element.bought_total
        element.current = getStockPrice(stockid, 'close')
        element.current_total = round(element.amount * element.current, 2)
        total += element.current_total
        element.change = element.current_total - element.bought_total
    return depotcontent, spent, total
################################################################################


################################################################################
# gets last stock price from database:
def getStockPrice(stockid, datatype):
    stockQuery = Stock.objects.get(id=stockid)
    stockSymbol = stockQuery.sourceSymbol
    stock1 = StockDatabase(stockSymbol)
    date, data = stock1.getStockPrice(datatype)
    return data
################################################################################


################################################################################
def buyStock(depot, stockid, amount, datatype, fee):
    stock = Stock.objects.get(id=stockid)
    depotcontent = depot.depotcontent_set.filter(stock = stock)
    print(depotcontent)
    price = getStockPrice(stockid,datatype)
    # check if enough money in depot:
    if (depot.available < float(amount) * price) + fee:
        amount = int((depot.available-fee) / price)
    # if stock already there:
    if (amount > 0):
        if not depotcontent:
            depotcontent = DepotContent()
            depotcontent.depotname = depot
            depotcontent.stock = Stock.objects.get(id=stockid)
            bought_at = price
        else:
            depotcontent = depotcontent[0]
            amount_pre = float(depotcontent.amount)
            bought_at = (amount_pre*depotcontent.bought_at+float(amount)*price)/(amount_pre+amount)
            amount = depotcontent.amount+amount

        depotcontent.bought_at = bought_at
        depotcontent.amount = amount
        depotcontent.date = datetime.datetime.now()
        depotcontent.save()
        # change available money in depot:
        depot.available = round(depot.available - float(amount) * price - fee,2)
        depot.save()
################################################################################


################################################################################
def sellStock(depot, stockid, amount, datatype, fee):
    stock = Stock.objects.get(id=stockid)
    depotcontent = depot.depotcontent_set.filter(stock = stock)
    depotcontent = depotcontent[0]
    price = getStockPrice(stockid, datatype)
    if (depotcontent.amount > amount):
        depotcontent.amount = depotcontent.amount - amount
        sold = float(amount) * price
        depotcontent.save()
    else:
        sold = float(depotcontent.amount) * price
        depotcontent.delete()

    # change available money in depot:
    depot.available = round(depot.available + sold - float(fee),2)
    depot.save()
################################################################################
