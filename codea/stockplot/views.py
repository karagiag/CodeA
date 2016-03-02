from django.shortcuts import *
from django.template import RequestContext
from django.http import JsonResponse
from datetime import *

from .models import Stock
import stockplot.FinApp.stock as stock
import json

def index(request):
    if request.method == "POST":
       if request.is_ajax():
            stocksymbol = request.POST.get('stocksymbol')
            stock1 = stock.Stock(stocksymbol)
            dates, data = stock1.getStockHistory('2005-01-01', '2016-02-28')
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
        return render(request, 'stockplot/index.html', context)

