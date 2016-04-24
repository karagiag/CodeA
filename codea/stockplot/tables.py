import django_tables2 as tables
from .models import DepotContent

class DepotTable(tables.Table):
    # add data from model + custom data
    stock = tables.Column(verbose_name="Stock")
    amount = tables.Column(verbose_name="Amount")
    bought_total = tables.Column()
    current = tables.Column()
    current_total = tables.Column()
    change = tables.Column()
    fee = tables.Column()
    buttonCol = tables.TemplateColumn(verbose_name='Sell',
                                      template_name='stockplot/buttoncolumn.html',
                                      orderable = False,)

    class Meta:
        model = DepotContent
        attrs = {"class":"paleblue"}
        fields = {"stock", "amount"}
        sequence = ("stock", "amount", "bought_total",
                    "current", "current_total", "change", "fee", "buttonCol")
        # change column headings


class DepotContentTable(tables.Table):
    # add data from model + custom data
    stock = tables.Column(verbose_name="Stock")
    amount = tables.Column(verbose_name="Amount")
    price = tables.Column(verbose_name="Price")
    date = tables.Column(verbose_name="Date")
    fee = tables.Column(verbose_name="Fee")

    class Meta:
        model = DepotContent
        attrs = {"class":"paleblue"}
        fields = {"stock", "amount", "price", "date", "fee"}
        sequence = ("date", "stock", "amount", "price", "fee")
        # change column headings
