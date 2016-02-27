from django.db import models

class Stock(models.Model):
    name = models.CharField(max_length = 50)
    symbol = models.CharField(max_length = 20)
    stockExchange = models.CharField(max_length = 100)

    def __str__(self):
        return self.name + ', ' + self.symbol
