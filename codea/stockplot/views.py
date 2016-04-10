# general imports
import datetime, json, sys, pytz
from dal import autocomplete
import pandas as pd

# django imports
from django.shortcuts import *
from django.template import RequestContext
from django.http import JsonResponse
from django.db.models import Q
from django.core import serializers
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django_tables2   import RequestConfig

# own django imports
from .models import Stock, Depot, DepotContent
from .forms import StockForm, DepotForm, BuyStockForm
from .tables import DepotTable

# own modules
from modules.FinApp.stockDatabase import StockDatabase
#from modules.FinApp.stockQuandl import StockQuandl
#from stockplot.FinApp.stockYahoo import StockYahoo


################################################################################
# home page
def index(request):
    context = {}
    return render(request, 'stockplot/index.html', context)


################################################################################
# main view for stockapp:
def stockapp(request):
    stockData = []; # initialize stockdata

    # in case of post data for stockplot has been requested:
    ##################### POST##################################################
    if request.method == "POST":
        method = request.POST.get('method')
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        stockid= request.POST.get('select_stock') # stockid from html form
        print(stockid)
        if method == 'plot':
            stockQuery = Stock.objects.get(id=stockid)
        else:
            stockQuery = Stock.objects.get(sourceSymbol = stockid)
        ##### stock datatype can be selected here.##############################
        ###  UPDATE  ###  IMPROVE THIS ############
        stockSymbol = stockQuery.sourceSymbol
        stockName = stockQuery.name
        #symbolQuandl = stockQuery.sourceSymbol
        #stock1 = StockQuandl(symbolQuandl)
        #datatype = 'Close'
        stock1 = StockDatabase(stockSymbol)
        datatype = 'close'
        ########################################################################

        # get historical new Date close prices here:
        step = 1 # every step'th value is returned only
        dates, data = stock1.getStockHistory(datatype, '1900-01-01', today, step)

        # for method plot just return dates, data. Else:
        if method == 'mvgAvg': # moving average
            days = int(request.POST.get('days')) # get days for moving average
            data = stock1.movingAverage(dates, data, days)
        elif method == 'expmvgAvg': # exponential moving average
            days = int(request.POST.get('days'))
            data = stock1.ExpAverage(dates, data, days)

        # put data into stockdata dict:
        for i in range(0, len(dates)-1):
            stockData.append({'dates': dates[i], 'data': data[i]})

        return JsonResponse({'stockData': stockData,
                             'stockSymbol': stockSymbol,
                             'stockName': stockName,})

    ######### NOT POST #########################################################
    # if method is not "plot", return an empty dict and render the
    # stockplot.html template
    else:
        stockData.append({'dates': [], 'data': []})
        stockData = json.dumps(stockData)
        context = {
            'stockData': stockData,
            'form': StockForm(),
            }
        return render(request, 'stockplot/stockplot.html', context)

################################################################################
# autocomplete for stock selection:
class StockAutocomplete(autocomplete.Select2QuerySetView):
    # uses dal for autocomplete!
    def get_queryset(self):
        stock = Stock.objects.all()
        if self.q:
            # query all stocks where name or symbol contain query "q":
            stock = stock.filter(Q(name__icontains=self.q)
                                 |Q(symbol__icontains=self.q))
        # then return stock object:
        return stock
################################################################################


# main view for depot ##########################################################
#@login_required
def depot(request):
    ##### UPDATE ##### fix if structure here...#################################
    if request.user.is_authenticated():
        if request.method == "POST":
            # select depot and display contents:################################
            if request.POST.get('select_depot') != None:
                depotname= request.POST.get('select_depot')
                request.session['depotname'] = depotname
                depot = Depot.objects.get(depotname = depotname)

            # create depot:#####################################################
            elif request.POST.get('depot_name') != None:
                depotname = request.POST.get('depot_name')
                request.session['depotname'] = depotname
                depot = Depot()
                depot.user = request.user
                depot.depotname = depotname
                depot.save()

            # buy stock: #######################################################
            elif request.POST.get('select_stock') != None:
                depotname = request.session['depotname']
                depot = Depot.objects.get(depotname = depotname)
                stockid= request.POST.get('select_stock')
                depotcontent = DepotContent()
                depotcontent.depotname = depot
                depotcontent.stock = Stock.objects.get(id=stockid)
                depotcontent.amount = request.POST.get('amount')
                depotcontent.bought_at = 60
                depotcontent.date = datetime.datetime.now()
                depotcontent.save()

            # render depot table and stockform: ################################
            depotcontent = depot.depotcontent_set.all()
            depotcontent = DepotTable(depotcontent)
            RequestConfig(request).configure(depotcontent)
            stockform = BuyStockForm()

        else: # GET:
            try: # to get depotname from session ###############################
                depotname =  request.session['depotname']
                depot = Depot.objects.get(depotname = depotname)
                depotcontent = depot.depotcontent_set.all()
                depotcontent = DepotTable(depotcontent)
                RequestConfig(request).configure(depotcontent)
                stockform =  BuyStockForm()

            except KeyError: # no depot selected yet:###########################
                depotname = ''
                depotcontent = ''
                stockform = ''

        # context contains forms, table and names for html template ############
        context = {
            'depotform': DepotForm(),
            'stockform': stockform,
            'depotcontent': depotcontent,
            'depotname': depotname,
        }
    else: # user is not logged in. Render nothing ##############################
        context = {
            'depotform': '',
            'stockform': '',
            'depotcontent': '',
            'depotname': '',
        }
    return render(request, 'stockplot/depot.html', context)
################################################################################


################################################################################
# autocomplete for depot selection: ############################################
class DepotAutocomplete(autocomplete.Select2QuerySetView):
    # uses dal for autocomplete!
    def get_queryset(self):
        # get only the depots created by the user:
        depot = Depot.objects.filter(user = self.request.user)
        if self.q:
            # query all depots where name or contains query "q":
            depot = depot.filter(Q(depotname__icontains=self.q))
        # then return depot object:
        return depot
