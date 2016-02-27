from django.shortcuts import render

from .models import Stock

def index(request):
    stocks = Stock.objects.all()
    context = {'stocks': stocks}
    return render(request, 'stockplot/index.html', context)

