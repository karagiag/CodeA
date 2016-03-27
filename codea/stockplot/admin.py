from django.contrib import admin

from .models import Stock, StockData, Depot

admin.site.register(Stock)
admin.site.register(StockData)
admin.site.register(Depot)
