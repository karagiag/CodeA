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

# own django imports
from .models import Stock, StockData
from .forms import StockForm
from .FinApp.stockQuandl import StockQuandl

# home page
def index(request):
    context = {}
    return render(request, 'stockplot/index.html', context)

# main view for stockapp:
def stockapp(request):
    if request.method == "POST":
        method = request.POST.get('method')
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        if method == 'plot':
            stocksymbol= request.POST.get('select_stock') # stockid from html form
            stockDatabase = Stock.objects.get(symbol=stocksymbol) # get all stocks from database
            stockname = stockDatabase.name
            # get data from different sources here. Must be json serialized!
            stockData = serializers.serialize("json", stockDatabase.stockdata_set.all(), fields=('date', 'close'))
            #date = stockDatabase.stockdata_set.values_list('date')
            #close = stockDatabase.stockdata_set.values_list('close')
            #print(date)
            #date = date.astimezone(timezone.get_current_timezone()).replace(tzinfo=None)
            #print(date)
            #print(timezone.is_aware(data['date']))
            #data = pd.DataFrame.from_records(close, index=date)
            #print(data)
            # Quandl:
            #stocksymbol = stockDatabase.QuandlSymbol # get symbol for Quandl
            #stock1 = StockQuandl(stocksymbol) # create stock object
            #data = stock1.getStockHistory('1900-01-01', today)
            #print(timezone.is_aware(data.index.values[0]))
        else:
            stocksymbol = request.POST.get('stocksymbol')
            stockname = '';
            stock1 = StockQuandl(stocksymbol) # create stock object
            if method == 'mvgAvg':
                days = int(request.POST.get('days'))
                data = stock1.movingAverage('1900-01-01', today, days)
            elif method == 'expmvgAvg':
                days = int(request.POST.get('days'))
                data = stock1.ExpAverage('1900-01-01', today, days)
        #stockData = data.reset_index().to_json(orient='records')
        #print(stockData)
        #stockData = serializers.serialize("json", stockData)
        #json.dumps(stockData, cls=DjangoJSONEncoder)
    else:
        stockData = []
        stockData.append({'Date': [], 'Close': []})

    if request.method == "POST":
        return JsonResponse({'stockData': stockData,
                             'stockSymbol': stocksymbol,
                             'stockName': stockname,})
    else:
        stockData = json.dumps(stockData)
        context = {
            'stockData': stockData,
            'form': StockForm(),
            }
        return render(request, 'stockplot/stockplot.html', context)


# autocomplete for stock selection:
class StockAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        stock = Stock.objects.all()
        if self.q:
            stock = stock.filter(Q(name__icontains=self.q)
                                 |Q(symbol__icontains=self.q))
        return stock
