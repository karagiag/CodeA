from django.db import models

# model for saving basic information about a stock:
class Stock(models.Model):
    name = models.CharField(max_length = 100)
    symbol = models.CharField(max_length = 20, primary_key = True)
    stockExchange = models.CharField(max_length = 100)
    QuandlName = models.CharField(max_length=100)
    QuandlSymbol = models.CharField(max_length=20)

    def __str__(self):
        return self.name + ', ' + self.symbol + ', ' + self.stockExchange

# model for saving data about stock, linked to Stock:
class StockData(models.Model):
    symbol = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateTimeField()
    open_price = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close  = models.FloatField()
    change = models.FloatField()
    traded_volume = models.FloatField()
    turnover = models.FloatField()
    last_price_of_the_day = models.FloatField()
    daily_traded_units = models.FloatField()
    daily_turnover = models.FloatField()

    class Meta:
        unique_together = ('symbol', 'date',) # only one entry per symbol per
        # specific Date

    def __str__(self):
        return str(self.symbol) + ', Date: ' + str(self.date)
