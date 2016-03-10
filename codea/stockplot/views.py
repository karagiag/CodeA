from django.shortcuts import *
from django.template import RequestContext
from django.http import JsonResponse
import datetime

from .models import Stock
import stockplot.FinApp.stock as stock
import json

def index(request):
    context = {}
    return render(request, 'stockplot/index.html', context)



def stockapp(request):
    if request.method == "POST":
       if request.is_ajax():
            method = request.POST.get('method')
            stocksymbol = request.POST.get('stocksymbol')
            stock1 = stock.Stock(stocksymbol)
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            dates = ['2016-01-01', '2016-01-02','2016-01-03','2016-01-04','2016-01-05',
                '2016-01-06','2016-01-07','2016-01-08','2016-01-09','2016-01-10',]
            data = [3, 4, 5, 4, 5, 6, 4, 3, 2, 6]
            if method == 'plot':
                dates, data = stock1.getStockHistory('1900-01-01', today)
                buff = 1;
            elif method == 'mvgAvg':
                days = int(request.POST.get('days'))
                dates, data = stock1.movingAverage('1900-01-01', today, days)
                buff = 1;
            elif method == 'expmvgAvg':
                days = int(request.POST.get('days'))
                dates, data = stock1.ExpAverage('1900-01-01', today, days)
                buff = 1;
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
            }
        return render(request, 'stockplot/stockplot.html', context)



def registration(request):
    context = {}
    return render(request, 'stockplot/registration.html', context)
