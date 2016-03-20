from django.shortcuts import *
from django.template import RequestContext
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from stockplot.models import Stock
from stockplot.forms import StockForm

import datetime, json
from .models import Stock
from dal import autocomplete
import stockplot.FinApp.stock as stockclass

def index(request):
    context = {}
    return render(request, 'stockplot/index.html', context)



def stockapp(request):
    if request.method == "POST":
        dates = ['2016-01-01', '2016-01-02','2016-01-03','2016-01-04','2016-01-05',
                '2016-01-06','2016-01-07','2016-01-08','2016-01-09','2016-01-10',]
        data = [3, 4, 5, 4, 5, 6, 4, 3, 2, 6]
        if request.is_ajax():
            method = request.POST.get('method')
            stockid = request.POST.get('stock') # stockid from html form
            stocks = Stock.objects.all() # get all stocks from database
            stocksymbol = stocks.filter(id=stockid) # filter for stockid
            stocksymbol = stocksymbol[0].QuandlSymbol # get symbol for Quandl
            stock1 = stockclass.Stock(stocksymbol) # create stock object
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            if method == 'plot':
                #dates, data = stock1.getStockHistory('1900-01-01', today)
                stock1.getStockHistoryQuandl('1900-01-01', today)
                buff = 1
            elif method == 'mvgAvg':
                days = int(request.POST.get('days'))
                dates, data = stock1.movingAverage('1900-01-01', today, days)
                buff = 1
            elif method == 'expmvgAvg':
                days = int(request.POST.get('days'))
                dates, data = stock1.ExpAverage('1900-01-01', today, days)
                buff = 1
    else:
        dates = []
        data = []

    stockData = [];
    for i in range(0, len(dates)-1):
        stockData.append({'date': dates[i], 'price': data[i]})

    if request.method == "POST":
        return JsonResponse({'stockData': stockData})
    else:
        stockData = json.dumps(stockData)
        context = {
            'stockData': stockData,
            'form': StockForm(),
            }
        return render(request, 'stockplot/stockplot.html', context)


class StockAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        stock = Stock.objects.all()
        if self.q:
            stock = stock.filter(symbol__istartswith=self.q)
        return stock
