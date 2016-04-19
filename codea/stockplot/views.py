# general imports
import datetime, json, sys
from dal import autocomplete

# django imports
from django.shortcuts import *
from django.template import RequestContext
from django.http import JsonResponse
from django.db.models import Q
from django.core import serializers
from django.utils import timezone

from django_tables2   import RequestConfig

# own django imports
from .models import Stock, Depot, DepotContent
from .forms import StockForm, DepotForm, BuyStockForm, SellStockForm, UserProfileForm
from .tables import DepotTable

# own modules
from modules.FinApp.stockDatabase import StockDatabase


################################################################################
# home page, just render html.
def index(request):
    context = {}
    return render(request, 'stockplot/index.html', context)
################################################################################

################################################################################
# news page, just render html.
def news(request):
    context = {}
    return render(request, 'stockplot/news.html', context)
################################################################################


################################################################################
# main view for stockapp:
def stockapp(request):
    stockData = []; # initialize stockdata

    # in case of post data for stockplot has been requested:
    ##################### POST##################################################
    if request.method == 'POST':
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        stockid= request.POST.get('select_stock') # stockid from html form
        stockQuery = Stock.objects.get(id=stockid)

        ##### stock datatype can be selected here.##############################
        stockSymbol = stockQuery.sourceSymbol
        stockName = stockQuery.name
        stock1 = StockDatabase(stockSymbol)
        datatype = 'close' # close, open, close_adj, etc.
        ########################################################################

        # get historical new Date close prices here:
        step = 1 # every step'th value is returned only
        datesource, data = stock1.getStockHistory(datatype, '1900-01-01', today, step)
        dates = [date * 1000 for date in datesource] # python date to js

        # for method plot just return dates, data. Else:
        if request.POST.get('select_method') == 'movingAverage': # moving average
            days = int(request.POST.get('days'))
            data = stock1.movingAverage(dates, data, days)
            stockName += str(days) + 'DaysMvgAvg'
        elif request.POST.get('select_method') == 'exponentialAverage': # exponential moving average
            days = int(request.POST.get('days'))
            data = stock1.ExpAverage(dates, data, days)
            stockName += str(days) + 'DaysExpMvgAvg'

        # put data into stockdata dict:
        for i in range(0, len(dates)-1):
            stockData.append({'dates': dates[i], 'data': data[i]})

        try: # to get plotData from session ####################################
            plotData =  request.session['plotData']
            stocknames = request.session['stocknames']
        except KeyError: # no plotData selected yet:############################
            plotData = []
            stocknames = []

        plotData.append(stockData)
        request.session['plotData'] = plotData
        stocknames.append(stockName)
        request.session['stocknames'] = stocknames

        return JsonResponse({'plotData': plotData,
                             'names': stocknames,})

    ######### GET ##############################################################
    else:
        stockData.append({'dates': [], 'data': []})
        # clear session:
        request.session.pop('plotData', None)
        request.session.pop('stocknames', None)

        if (request.GET.get('action') == 'clear'): # clear button:
            return JsonResponse({'plotData': stockData,
                                 'names': ['Plot'],})
        else: # first loading of page
            context = {
                'plotData': json.dumps([stockData]),
                'names': ['Plot'],
                'stockform': StockForm(),
                }
            return render(request, 'stockplot/stockplot.html', context)
################################################################################



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


################################################################################
# main view for depot ##########################################################
def depot(request):
    ##### UPDATE ##### fix if structure here...#################################
    if request.user.is_authenticated():
        if request.method == "POST":

            # sell selected amount of stock ####################################
            if (request.POST.get('stock') != None):
                stockid = int(request.POST.get('stock')) # returns stock ID
                stock = Stock.objects.get(id = stockid)
                # logTransaction()
                return JsonResponse({'text': 'sell',})

            # select depot and display contents:################################
            elif request.POST.get('select_depot') != None:
                depotname= request.POST.get('select_depot')
                request.session['depotname'] = depotname
                depot = Depot.objects.get(depotname = depotname)

            # create depot:#####################################################
            elif request.POST.get('depot_name') != '':
                depotname = request.POST.get('depot_name')
                request.session['depotname'] = depotname
                depot = Depot()
                depot.user = request.user
                depot.depotname = depotname
                depot.value = request.POST.get('depot_value')
                depot.save()

            else:
                # error
                context = {
                    'depotform': DepotForm(),
                    'depotcontent': '',
                }
                return render(request, 'stockplot/depot.html', context)

            # render depot table and stockform: ################################
            stockform = BuyStockForm()
            depotcontent, spent, total = depotAnalysis(depot)
            depotcontent = DepotTable(depotcontent)
            RequestConfig(request).configure(depotcontent)
            depotvalue = depot.value
            available = depot.available

        else: # GET:
            try: # to get depotname from session ###############################
                depotname =  request.session['depotname']
                depot = Depot.objects.get(depotname = depotname)
                depotcontent, spent, total = depotAnalysis(depot)
                depotcontent = DepotTable(depotcontent)
                depotvalue = depot.value
                available = depot.available
                RequestConfig(request).configure(depotcontent)
                stockform =  BuyStockForm()

            except KeyError: # no depot selected yet:###########################
                stockform = ''
                depotcontent = ''
                depotname = ''
                depotvalue = 0
                available = 0
                total = 0

        # context contains forms, table and names for html template ############
        context = {
            'depotform': DepotForm(),
            'stockform': stockform,
            'depotcontent': depotcontent,
            'depotname': depotname,
            'depotvalue': depotvalue,
            'available': available,
            'total': total+available,
            'change': round(total+available-depotvalue,2),
        }
    else: # user is not logged in. Render nothing ##############################
        context = {
            'depotform': '',
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
################################################################################


################################################################################
# analyses contents of depot and calculates money stuff...
def depotAnalysis(depot):
    depotcontent = list(depot.depotcontent_set.all())
    spent = 0 # money spent on stocks
    total = 0 # total value of stocks
    for element in depotcontent:
        stockid = element.stock.id
        element.bought_total = round(element.amount * element.bought_at,2)
        spent += element.bought_total
        element.current = getStockPrice(stockid)
        element.current_total = round(element.amount * element.current, 2)
        total += element.current_total
        element.change = element.current_total - element.bought_total
    return depotcontent, spent, total
################################################################################


################################################################################
# gets last stock price from database:
def getStockPrice(stockid):
    stockQuery = Stock.objects.get(id=stockid)
    stockSymbol = stockQuery.sourceSymbol
    stock1 = StockDatabase(stockSymbol)
    datatype = 'close' # close, open, close_adj, etc.
    date, data = stock1.getStockPrice(datatype)
    return data
################################################################################



################################################################################
# page for buying stock
def buystock(request):
    if request.method == "POST":
        depotname =  request.session['depotname']
        depot1 = Depot.objects.get(depotname = depotname)
        stockid= request.POST.get('select_stock')
        depotcontent = DepotContent()
        depotcontent.depotname = depot1
        depotcontent.stock = Stock.objects.get(id=stockid)
        depotcontent.amount = request.POST.get('amount')
        depotcontent.bought_at = getStockPrice(stockid)
        depotcontent.date = datetime.datetime.now()
        depotcontent.save()
        # change available money in depot:
        fee = request.POST.get('fees')
        depot1.available = depot1.available - float(depotcontent.amount) * depotcontent.bought_at - float(fee)
        depot1.save()
        # log
        return HttpResponseRedirect('/depot/')

    context = {'form': BuyStockForm(),}
    return render(request, 'stockplot/buystock.html', context)
################################################################################


################################################################################
# profile page
def profile(request):
    context = {'form': UserProfileForm(),}
    return render(request, 'stockplot/profile.html', context)
################################################################################
