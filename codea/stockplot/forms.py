from dal import autocomplete
from crispy_forms.bootstrap import InlineField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Button
from crispy_forms.bootstrap import FormActions
from django import forms
from stockplot.models import Stock

# form for selecting stock in stockplot.
class StockForm(forms.ModelForm):
    # form for selecting stock with autocomplete from database
    select_stock = forms.ModelChoiceField(
        queryset=Stock.objects.all(),
        widget=autocomplete.ModelSelect2(url='./stock-autocomplete')
    )

    class Meta:
        model = Stock
        fields = ()

##### UPDATE ###### Introduce helper? ##########################################
