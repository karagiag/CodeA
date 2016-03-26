from django.contrib import admin

from .models import Stock, StockData

admin.site.register(Stock)
admin.site.register(StockData)
