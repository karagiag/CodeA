from dal import autocomplete
from crispy_forms.bootstrap import InlineField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Button, HTML
from crispy_forms.bootstrap import FormActions
from django import forms
from stockplot.models import Stock, Depot, DepotContent

# form for selecting stock in stockplot.
class StockForm(forms.ModelForm):
    # form for selecting stock with autocomplete from database
    select_stock = forms.ModelChoiceField(
        queryset=Stock.objects.all(),
        widget=autocomplete.ModelSelect2(url='/stockapp/stock-autocomplete')
    )

    class Meta:
        model = Stock
        fields = ()

    def __init__(self, *args, **kwargs):
        super(StockForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
            HTML('<div class="form-group"><label>Select Stock:</label></div>'),
            'select_stock',
            FormActions(
                Submit('Select Stock', 'Plot', css_class = 'btn-plot btn-sm'),
            )
        )

# form for selecting depot:
class DepotForm(forms.ModelForm):
    # form for selecting depot with autocomplete from database
    select_depot = forms.ModelChoiceField(
        queryset=Depot.objects.all(),
        widget=autocomplete.ModelSelect2(url='/depot/depot-autocomplete')
    )
    depot_name = forms.CharField(max_length = 100, help_text='Depot name')

    def __init__(self, *args, **kwargs):
        super(DepotForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
            HTML('<div class="form-group"><label>Select Depot:</label></div>'),
            'select_depot',
            FormActions(
                Submit('Select Depot', 'Select', css_class = 'btn-default btn-sm'),
            ),
            HTML('<div class="form-group"><label>or create depot:</label></div>'),
            InlineField('depot_name', css_class ='input-sm'),
            FormActions(
                Submit('Create Depot', '+', css_class = 'btn-default btn-sm')
            ),
        )

    class Meta:
        model = Depot
        fields = ()

# form for buying stock.
class BuyStockForm(forms.ModelForm):
    # form for selecting stock with autocomplete from database
    select_stock = forms.ModelChoiceField(
        queryset=Stock.objects.all(),
        widget=autocomplete.ModelSelect2(url='/stockapp/stock-autocomplete')
    )
    amount = forms.IntegerField()
    class Meta:
        model = Stock
        fields = ()

    def __init__(self, *args, **kwargs):
        super(BuyStockForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
            HTML('<div class="form-group"><label>Select Stock:</label></div>'),
            'select_stock',
            InlineField('amount', css_class = 'input-sm'),
            FormActions(
                Submit('Buy Stock', 'Buy', css_class = 'btn-plot btn-sm'),
            )
        )
