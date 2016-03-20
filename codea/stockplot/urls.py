from django.conf.urls import url
from django.conf.urls import include
from stockplot.views import StockAutocomplete

from . import views

app_name = 'stockplot'

urlpatterns = [ url(r'^$', views.index, name = 'index'),
                url(r'^stockapp/$', views.stockapp, name = 'stockapp'),
                url(
                    r'^stockapp/stock-autocomplete/$',
                    StockAutocomplete.as_view(),
                    name='stock-autocomplete',
                ),]
