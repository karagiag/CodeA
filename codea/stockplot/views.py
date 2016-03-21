# general imports
import datetime, json
from dal import autocomplete
import pandas as pd

# django imports
from django.shortcuts import *
from django.template import RequestContext
from django.http import JsonResponse
from django.db.models import Q

# own django imports
from .models import Stock
from .forms import StockForm
from .FinApp.stockQuandl import StockQuandl

# home page
def index(request):
    context = {}
    return render(request, 'stockplot/index.html', context)

# main view for stockapp:
def stockapp(request):
    if request.method == "POST":
        #dates = ['2016-01-01', '2016-01-02','2016-01-03','2016-01-04','2016-01-05',
        #        '2016-01-06','2016-01-07','2016-01-08','2016-01-09','2016-01-10',]
        #data = [3, 4, 5, 4, 5, 6, 4, 3, 2, 6]
        #data = pd.DataFrame(data, index=dates)
        method = request.POST.get('method')
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        if method == 'plot':
            stockid = request.POST.get('select_stock') # stockid from html form
            stocks = Stock.objects.all() # get all stocks from database
            stockDatabase = stocks.filter(id=stockid) # filter for stockid
            stocksymbol = stockDatabase[0].QuandlSymbol # get symbol for Quandl
            stockname = stockDatabase[0].name
            stock1 = StockQuandl(stocksymbol) # create stock object
            # get data:
            data = stock1.getStockHistory('1900-01-01', today)
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
        stockData = data.reset_index().to_json(orient='records')
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
