from django.contrib import admin

from .models import Stock, StockData, StockDataFile, Depot, DepotContent 

admin.site.register(Stock)
admin.site.register(StockData)
admin.site.register(StockDataFile)
admin.site.register(Depot)
admin.site.register(DepotContent)
