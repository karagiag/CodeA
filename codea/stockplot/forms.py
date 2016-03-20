from dal import autocomplete
from crispy_forms.bootstrap import InlineField


from django import forms
from stockplot.models import Stock

class StockForm(forms.ModelForm):
    stock = forms.ModelChoiceField(
        queryset=Stock.objects.all(),
        widget=autocomplete.ModelSelect2(url='./stock-autocomplete')
    )

    class Meta:
        model = Stock
        fields = ()
