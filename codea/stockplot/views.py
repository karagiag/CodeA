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
                depotcontent.bought_at = 60 # UPDATE
                depotcontent.date = datetime.datetime.now()
                depotcontent.save()
                # logTransaction()

            # render depot table and stockform: ################################
            depotcontent = depotAnalysis(depot)
            depotcontent = DepotTable(depotcontent)
            RequestConfig(request).configure(depotcontent)
            stockform = BuyStockForm()

        else: # GET:
            try: # to get depotname from session ###############################
                depotname =  request.session['depotname']
                depot = Depot.objects.get(depotname = depotname)
                depotcontent = depotAnalysis(depot)
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
################################################################################


################################################################################
# analyses contents of depot and calculates money stuff...
def depotAnalysis(depot):
    depotcontent = list(depot.depotcontent_set.all())
    for element in depotcontent:
        element.bought_total = element.amount * element.bought_at
        element.current = 40 # UPDATE
        element.current_total = element.amount * element.current
        element.change = element.current_total - element.bought_total
    return depotcontent
################################################################################


################################################################################
# profile page
def profile(request):
    context = {'form': UserProfileForm(),}
    return render(request, 'stockplot/profile.html', context)
################################################################################
