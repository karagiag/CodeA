import django_tables2 as tables
from .models import DepotContent

class DepotTable(tables.Table):
    # add data from model + custom data
    stock = tables.Column(verbose_name="Stock")
    date = tables.Column(verbose_name="Date bought")
    amount = tables.Column(verbose_name="Amount")
    bought_at = tables.Column(verbose_name="Buy price")
    bought_total = tables.Column()
    current = tables.Column()
    current_total = tables.Column()
    change = tables.Column()
    buttonCol = tables.TemplateColumn(verbose_name='Sell',
                                      template_name='stockplot/buttoncolumn.html',
                                      orderable = False,)

    class Meta:
        model = DepotContent
        attrs = {"class":"paleblue"}
        fields = {"stock", "amount", "bought_at", "date"}
        sequence = ("stock", "date", "amount", "bought_at", "bought_total",
                    "current", "current_total", "change", "buttonCol")
        # change column headings
