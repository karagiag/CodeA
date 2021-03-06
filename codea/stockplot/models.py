import architect # for partitioning

from django.db import models
from django.contrib.auth.models import User

################################################################################
# model for saving basic information about a stock:
class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 100)
    symbol = models.CharField(max_length = 20)
    stockExchange = models.CharField(max_length = 100)
    source = models.CharField(max_length=100)
    sourceName = models.CharField(max_length=100)
    sourceSymbol = models.CharField(max_length=20)
    fundamentalsSymbol = models.CharField(max_length=20)
    fundamentalsCompNumber = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.name + ', ' + self.symbol + ', ' + self.stockExchange



################################################################################
# model for stock scoring:
class StockScore(models.Model):
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE)
    riskClass = models.IntegerField(null=True, blank=True, default=0)
    industry = models.CharField(max_length = 100)
    companyScore = models.IntegerField(null=True, blank=True, default=0)
    balanceScore = models.IntegerField(null=True, blank=True, default=0)
    analysisScore = models.IntegerField(null=True, blank=True, default=0)
    newsScore = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.stock + ', ' + self.riskClass

    class Meta:
        unique_together = ('stock', 'riskClass',) # only one entry per symbol per



################################################################################
# model for saving data about stock, linked to Stock:
@architect.install('partition', type='range', subtype='integer', constraint='100', column='stockid')
# export DJANGO_SETTINGS_MODULE='codea.settings'
# architect partition --module stockplot.models
class StockData(models.Model):
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE)
    stockid = models.IntegerField(db_index = True)
    date = models.FloatField(db_index = True)
    open_price = models.FloatField(null=True, blank=True, default=None)
    adj_open = models.FloatField(null=True, blank=True, default=None)
    high = models.FloatField(null=True, blank=True, default=None)
    adj_high = models.FloatField(null=True, blank=True, default=None)
    low = models.FloatField(null=True, blank=True, default=None)
    adj_low = models.FloatField(null=True, blank=True, default=None)
    close  = models.FloatField(null=True, blank=True, default=None)
    adj_close = models.FloatField(null=True, blank=True, default=None)
    change = models.FloatField(null=True, blank=True, default=None)
    traded_volume = models.FloatField(null=True, blank=True, default=None)
    adj_volume = models.FloatField(null=True, blank=True, default=None)
    turnover = models.FloatField(null=True, blank=True, default=None)
    last_price_of_the_day = models.FloatField(null=True, blank=True, default=None)
    daily_traded_units = models.FloatField(null=True, blank=True, default=None)
    daily_turnover = models.FloatField(null=True, blank=True, default=None)
    ex_dividend = models.FloatField(null=True, blank=True, default=None)
    split_ratio = models.FloatField(null=True, blank=True, default=None)

    class Meta:
        unique_together = ('stockid', 'date',) # only one entry per symbol per
        '''index_together = [
            ['symbol', 'date'],
        ]'''
        # specific Date

    def __str__(self):
        return str(self.stock) + ', Date: ' + str(self.date)



################################################################################
# model for saving files for stocks (timestamp, value):
@architect.install('partition', type='range', subtype='integer', constraint='100', column='stockid')
# export DJANGO_SETTINGS_MODULE='codea.settings'
# architect partition --module stockplot.models
class StockDataFile(models.Model):
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE)
    stockid = models.IntegerField(db_index = True)
    fromDate = models.FloatField(db_index = True)
    toDate = models.FloatField()
    stockdata = models.FileField(upload_to='data/')

    class Meta:
        unique_together = ('stockid', 'fromDate',)
        '''index_together = [
            ['symbol', 'date'],
        ]'''

    def __str__(self):
        return str(self.stock) + ', Date: ' + str(self.fromDate)


################################################################################
# model for saving fundamentals about stock, linked to Stock:
@architect.install('partition', type='range', subtype='integer', constraint='100', column='stockid')
# export DJANGO_SETTINGS_MODULE='codea.settings'
# architect partition --module stockplot.models
class StockFundamentals(models.Model):
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE)
    stockid = models.IntegerField(db_index = True)
    date = models.FloatField(db_index = True)
    shares = models.FloatField(null=True, blank=True, default=None)
    capitalization = models.FloatField(null=True, blank=True, default=None)
    PCF = models.FloatField(null=True, blank=True, default=None)
    PSR = models.FloatField(null=True, blank=True, default=None)
    PB = models.FloatField(null=True, blank=True, default=None)
    EPSD = models.FloatField(null=True, blank=True, default=None)
    quick  = models.FloatField(null=True, blank=True, default=None)
    current = models.FloatField(null=True, blank=True, default=None)

    class Meta:
        unique_together = ('stockid', 'date',) # only one entry per symbol per
        '''index_together = [
            ['symbol', 'date'],
        ]'''
        # specific Date

    def __str__(self):
        return str(self.stock) + ', Date: ' + str(self.date)


################################################################################
# model for a depot:
class Depot(models.Model):
    user = models.ForeignKey(User)
    depotname = models.CharField(max_length = 100, primary_key=True)
    value = models.IntegerField()
    available = models.FloatField()

    class Meta:
        unique_together = ('user', 'depotname',)

    def __str__(self):
        return str(self.user) + ' ' + str(self.depotname)



################################################################################
# model for a depot entry:
class DepotContent(models.Model):
    depotname = models.ForeignKey(Depot, on_delete = models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE)
    amount = models.IntegerField()
    price = models.FloatField()
    maxSinceBought = models.FloatField()
    date = models.DateTimeField()
    fee = models.FloatField()

    def __str__(self):
        return str(self.depotname) + ': ' + str(self.stock)
