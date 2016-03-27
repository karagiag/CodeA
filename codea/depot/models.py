from django.db import models
from django.contrib.auth.models import User

from stockplot import models as stockplot_models

# Create your models here.
class Depot(models.Model):
    user = models.ForeignKey(User)
    stock = models.ForeignKey(stockplot_models.Stock)
    amount = models.IntegerField()
    bought_at = models.FloatField()

    class Meta:
        unique_together = ('user', 'stock',)
