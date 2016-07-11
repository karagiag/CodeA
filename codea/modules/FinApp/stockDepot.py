# class for stock data from Database

# general imports
import os, sys, time, h5py, pytz
import datetime as datetime
import pandas as pd
import numpy as np

# own modules
from stockDatabase import StockDatabase

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
# start a depot for user with given value:
def createDepot(user, depotname, value):
    depot = Depot()
    depot.user = user
    depot.depotname = depotname
    depot.value = int(value)
    depot.available = float(value)
    depot.save()
    return depot
################################################################################

################################################################################
# delete a depot
def deleteDepot(user, depotname):
    depot = Depot.objects.get(depotname = depotname)
    if depot != None:
        depot.delete()
################################################################################

################################################################################
# analyses contents of depot and calculates money stuff...
def depotAnalysis(depot):
    depotcontent = list(depot.depotcontent_set.all())
    depotcontent_total = [] # list for output
    total = 0 # total value of stocks

    for content in depotcontent: # go through each depotcontent element
        found = False
        if depotcontent_total != []: # look if already in list, then add
            for content_total in depotcontent_total:
                if content_total.stock == content.stock:
                    content_total.amount += content.amount
                    content_total.bought_total += round(content.amount * content.price, 2)
                    content_total.fee += round(content.fee,2)
                    found = True
                    break
        if not found: # else add to list
            content.bought_total = round(content.amount * content.price, 2)
            content.fee = round(content.fee, 2)
            depotcontent_total.append(content)

    if depotcontent_total != []:
        for content_total in depotcontent_total: # go through list and do analysis
            stockid = content_total.stock.id
            content_total.current = getStockPrice(stockid, 'close')
            content_total.current_total  = round(content_total.amount * content_total.current, 2)
            content_total.change = round(content_total.current_total - content_total.bought_total,2)
            total += content_total.current_total

    depotvalue = depot.value
    available = depot.available
    balance = round(total+available, 2)
    change = round(total+available-depotvalue,2)
    return depotcontent_total, balance, depotvalue, available, change
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
# gets stock price for specific date from database:
def getStockPriceDate(stockid, datatype, date):
    stockQuery = Stock.objects.get(id=stockid)
    stockSymbol = stockQuery.sourceSymbol
    stock1 = StockDatabase(stockSymbol)
    date, data = stock1.getStockPriceDate(datatype, date)
    return data
################################################################################


################################################################################
def buyStock(depot, stockid, amount, datatype, fee):
    price = getStockPrice(stockid,datatype)
    buyStockBase(depot, stockid, amount, datatype, fee, price)

def buyStockDate(depot, stockid, amount, datatype, fee, date):
    price = getStockPriceDate(stockid, 'close', date)
    buyStockBase(depot, stockid, amount, datatype, fee, price)

def buyStockBase(depot, stockid, amount, datatype, fee, price):
    stock = Stock.objects.get(id=stockid)
    # check if enough money in depot:
    if (depot.available < float(amount) * price + fee):
        amount = int((depot.available-fee) / price)
    # if stock already there:
    if (amount > 0):
        depotcontent = DepotContent()
        depotcontent.depotname = depot
        depotcontent.stock = Stock.objects.get(id=stockid)
        depotcontent.price = price
        depotcontent.amount = abs(amount)
        localtz = pytz.timezone('Europe/Berlin')
        depotcontent.date = localtz.localize(datetime.datetime.now())
        depotcontent.fee = fee
        depotcontent.save()
        # change available money in depot:
        depot.available = round(depot.available - float(amount) * price - fee,2)
        depot.save()
################################################################################

################################################################################
def sellStock(depot, stockid, amount, datatype, fee):
    price = getStockPrice(stockid, datatype)
    sellStockBase(depot, stockid, amount, datatype, fee, price)

def sellStockDate(depot, stockid, amount, datatype, fee, date):
    price = getStockPriceDate(stockid, 'close', date)
    sellStockBase(depot, stockid, amount, datatype, fee, price)

def sellStockBase(depot, stockid, amount, datatype, fee, price):
    stock = Stock.objects.get(id=stockid)
    depotcontent, total, depotvalue, available, change = depotAnalysis(depot)
    # check how many stocks are available:
    for content in depotcontent:
        if content.stock == stock:
            max_amount = content.amount
            break
    if (amount > max_amount):
        amount = max_amount

    depotcontent = DepotContent()
    depotcontent.depotname = depot
    depotcontent.stock = Stock.objects.get(id=stockid)
    depotcontent.price = price
    depotcontent.amount = -abs(amount)
    localtz = pytz.timezone('Europe/Berlin')
    depotcontent.date = localtz.localize(datetime.datetime.now())
    depotcontent.fee = fee
    depotcontent.save()

    # change available money in depot:
    depot.available = round(depot.available + price * float(amount) - float(fee),2)
    depot.save()
################################################################################




### following methods duplicated...IMPROVE UPDATE

################################################################################
def depotAnalysisDate(depot, date):
    depotcontent = list(depot.depotcontent_set.all())
    depotcontent_total = [] # list for output
    total = 0 # total value of stocks

    for content in depotcontent: # go through each depotcontent element
        found = False
        if depotcontent_total != []: # look if already in list, then add
            for content_total in depotcontent_total:
                if content_total.stock == content.stock:
                    content_total.amount += content.amount
                    content_total.bought_total += round(content.amount * content.price, 2)
                    content_total.fee += round(content.fee,2)
                    found = True
                    break
        if not found: # else add to list
            content.bought_total = round(content.amount * content.price, 2)
            content.fee = round(content.fee, 2)
            depotcontent_total.append(content)

    if depotcontent_total != []:
        for content_total in depotcontent_total: # go through list and do analysis
            stockid = content_total.stock.id
            content_total.current = getStockPriceDate(stockid, 'close', date)
            content_total.current_total  = round(content_total.amount * content_total.current, 2)
            content_total.change = round(content_total.current_total - content_total.bought_total,2)
            total += content_total.current_total

    depotvalue = depot.value
    available = depot.available
    balance = round(total+available, 2)
    change = round(total+available-depotvalue,2)
    return depotcontent_total, balance, depotvalue, available, change
################################################################################
