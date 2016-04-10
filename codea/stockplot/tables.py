import django_tables2 as tables
from .models import DepotContent

class DepotTable(tables.Table):
    class Meta:
        model = DepotContent
        attrs = {"class":"paleblue"}
        fields = {"stock", "amount", "bought_at", "date"}
