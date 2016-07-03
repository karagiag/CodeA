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
from .tables import DepotTable, DepotContentTable

# own modules
from modules.FinApp.stockDatabase import StockDatabase
import modules.FinApp.stockDepot as stockDepot


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
    # in case of post data for stockplot has been requested:
    stockData = []
    ##################### POST##################################################
    if request.method == 'POST':
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        stockid= request.POST.get('select_stock') # stockid from html form
        stockQuery = Stock.objects.get(id=stockid)

        ##### stock datatype can be selected here.##############################
        stockSymbol = stockQuery.sourceSymbol
        stockName = [stockQuery.name]
        stock1 = StockDatabase(stockSymbol)
        datatype = 'close' # close, open, close_adj, etc.
        ########################################################################

        # get historical new Date close prices here:
        step = 1 # every step'th value is returned only
        data = [[]]
        datesource, data[0] = stock1.getStockHistory(datatype, '1900-01-01', today, step)
        dates = [date * 1000 for date in datesource] # python date to js

        # for method plot just return dates, data. Else:
        if request.POST.get('select_method') == 'movingAverage': # moving average
            days = int(request.POST.get('days'))
            data[0] = stock1.movingAverage(dates, data[0], days)
            stockName[0] += str(days) + 'DaysMvgAvg'
        elif request.POST.get('select_method') == 'exponentialAverage': # exponential moving average
            days = int(request.POST.get('days'))
            data[0] = stock1.ExpAverage(dates, data[0], days)
            stockName[0] += str(days) + 'DaysExpMvgAvg'
        elif request.POST.get('select_method') == 'macd': # moving average convergence Divergence
            data[0] = stock1.MACD(dates, data[0])
            stockName[0] += 'MACD'
            print (request.POST.get('days'))
            if request.POST.get('days') != '':
                days = int(request.POST.get('days'))
                data[0] = stock1.ExpAverage(dates, data[0], days)
                stockName[0] += str(days) + 'DaysExpMvgAvg'
        elif request.POST.get('select_method') == 'ppo': # percentage price Oscillator
            data[0] = stock1.PPO(dates, data[0])
            stockName[0] += 'PPO'
            if request.POST.get('days') != '':
                days = int(request.POST.get('days'))
                data[0] = stock1.ExpAverage(dates, data[0], days)
                stockName[0] += str(days) + 'DaysExpMvgAvg'
        elif request.POST.get('select_method') == 'bollinger': # Bollinger Band
            days = 20
            factor = 2
            data[0], average, high = stock1.Bollinger(dates, data[0], days,
                                                      factor)
            data.append(average)
            data.append(high)
            stockName[0] += 'Bollinger Band'
            stockName.append(stockName[0] + 'Bollinger Band')
            stockName.append(stockName[0] + 'Bollinger Band')

        # put data into stockdata dict:
        # create empty stockdata list:
        stockData = [[] for x in range(len(data))]
        for i in range(0, len(data)):
            for j in range(0, len(dates)-1):
                stockData[i].append({'dates': dates[j], 'data': data[i][j]})

        try: # to get plotData from session ####################################
            plotData =  request.session['plotData']
            stocknames = request.session['stocknames']
        except KeyError: # no plotData selected yet:############################
            plotData = []
            stocknames = []

        for data in stockData:
            plotData.append(data)
        request.session['plotData'] = plotData
        for name in stockName:
            stocknames.append(name)
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
                print("here")
                stockid = int(request.POST.get('stock')) # returns stock ID
                depotname =  request.session['depotname']
                depot = Depot.objects.get(depotname = depotname)
                amount = int(request.POST.get('amount'))
                fee = float(request.POST.get('fee'))
                datatype = 'close'
                stockDepot.sellStock(depot, stockid, amount, datatype, fee)
                # logTransaction()

            # select depot and display contents:################################
            elif request.POST.get('select_depot') != None:
                depotname= request.POST.get('select_depot')
                request.session['depotname'] = depotname
                depot = Depot.objects.get(depotname = depotname)

            # create depot:#####################################################
            elif request.POST.get('depot_name') != '' and request.POST.get('depot_name') != None:
                depotname = request.POST.get('depot_name')
                request.session['depotname'] = depotname
                user = request.user
                value = request.POST.get('depot_value')
                depot = stockDepot.createDepot(user, depotname, value)

            else:
                # error
                context = {
                    'depotform': DepotForm(),
                    'depotcontent': '',
                }
                return render(request, 'stockplot/depot.html', context)

            # render depot table and stockform: ################################
            stockform = BuyStockForm()
            depotcontent, total, depotvalue, available, change = stockDepot.depotAnalysis(depot)
            depotcontent = DepotTable(depotcontent)
            RequestConfig(request).configure(depotcontent)

        else: # GET:
            try: # to get depotname from session ###############################
                depotname =  request.session['depotname']
                depot = Depot.objects.get(depotname = depotname)
                depotcontent, total, depotvalue, available, change = stockDepot.depotAnalysis(depot)
                depotcontent = DepotTable(depotcontent)
                RequestConfig(request).configure(depotcontent)
                stockform =  BuyStockForm()

            except: # no depot selected yet:###########################
                stockform = ''
                depotcontent = ''
                depotname = ''
                depotvalue = 0
                available = 0
                total = 0
                change = 0

        # context contains forms, table and names for html template ############
        context = {
            'depotform': DepotForm(),
            'stockform': stockform,
            'depotcontent': depotcontent,
            'depotname': depotname,
            'depotvalue': depotvalue,
            'available': available,
            'total': total,
            'change': change,
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
# page for buying stock
def buystock(request):
    if request.method == "POST":
        depotname =  request.session['depotname']
        depot = Depot.objects.get(depotname = depotname)
        stockid= request.POST.get('select_stock')
        amount = int(request.POST.get('amount'))
        datatype = 'close'
        fee = float(request.POST.get('fees'))
        stockDepot.buyStock(depot, stockid, amount, datatype, fee)
        # log
        return HttpResponseRedirect('/depot/')

    context = {'form': BuyStockForm(),}
    return render(request, 'stockplot/buystock.html', context)
################################################################################


################################################################################
# page for selling stock
def depotlog(request):
    try: # to get depotname from session ###############################
        depotname =  request.session['depotname']
        depot = Depot.objects.get(depotname = depotname)
        depotcontent = depot.depotcontent_set.all()
        depotlog = DepotContentTable(depotcontent)
        RequestConfig(request).configure(depotlog)
        context = {'depotname': depotname,
                   'depotlog': depotlog,}
    except:
        context = {'depotname': '',
                   'depotlog': '',}
    return render(request, 'stockplot/depotlog.html', context)
################################################################################


################################################################################
# profile page
def profile(request):
    context = {'form': UserProfileForm(),}
    return render(request, 'stockplot/profile.html', context)
################################################################################
